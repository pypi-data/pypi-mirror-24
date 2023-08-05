"""Implementation of the StyleGuide used by Flake8."""
import collections
import contextlib
import enum
import functools
import linecache
import logging

from flake8 import defaults
from flake8 import statistics
from flake8 import utils

__all__ = (
    'StyleGuide',
)

LOG = logging.getLogger(__name__)


try:
    lru_cache = functools.lru_cache
except AttributeError:
    def lru_cache(maxsize=128, typed=False):
        """Stub for missing lru_cache."""
        def fake_decorator(func):
            return func

        return fake_decorator


# TODO(sigmavirus24): Determine if we need to use enum/enum34
class Selected(enum.Enum):
    """Enum representing an explicitly or implicitly selected code."""

    Explicitly = 'explicitly selected'
    Implicitly = 'implicitly selected'


class Ignored(enum.Enum):
    """Enum representing an explicitly or implicitly ignored code."""

    Explicitly = 'explicitly ignored'
    Implicitly = 'implicitly ignored'


class Decision(enum.Enum):
    """Enum representing whether a code should be ignored or selected."""

    Ignored = 'ignored error'
    Selected = 'selected error'


@lru_cache(maxsize=512)
def find_noqa(physical_line):
    return defaults.NOQA_INLINE_REGEXP.search(physical_line)


_Violation = collections.namedtuple(
    'Violation',
    [
        'code',
        'filename',
        'line_number',
        'column_number',
        'text',
        'physical_line',
    ],
)


class Violation(_Violation):
    """Class representing a violation reported by Flake8."""

    def is_inline_ignored(self, disable_noqa):
        # type: (Violation) -> bool
        """Determine if an comment has been added to ignore this line.

        :param bool disable_noqa:
            Whether or not users have provided ``--disable-noqa``.
        :returns:
            True if error is ignored in-line, False otherwise.
        :rtype:
            bool
        """
        physical_line = self.physical_line
        # TODO(sigmavirus24): Determine how to handle stdin with linecache
        if disable_noqa:
            return False

        if physical_line is None:
            physical_line = linecache.getline(self.filename,
                                              self.line_number)
        noqa_match = find_noqa(physical_line)
        if noqa_match is None:
            LOG.debug('%r is not inline ignored', self)
            return False

        codes_str = noqa_match.groupdict()['codes']
        if codes_str is None:
            LOG.debug('%r is ignored by a blanket ``# noqa``', self)
            return True

        codes = set(utils.parse_comma_separated_list(codes_str))
        if self.code in codes or self.code.startswith(tuple(codes)):
            LOG.debug('%r is ignored specifically inline with ``# noqa: %s``',
                      self, codes_str)
            return True

        LOG.debug('%r is not ignored inline with ``# noqa: %s``',
                  self, codes_str)
        return False

    def is_in(self, diff):
        """Determine if the violation is included in a diff's line ranges.

        This function relies on the parsed data added via
        :meth:`~StyleGuide.add_diff_ranges`. If that has not been called and
        we are not evaluating files in a diff, then this will always return
        True. If there are diff ranges, then this will return True if the
        line number in the error falls inside one of the ranges for the file
        (and assuming the file is part of the diff data). If there are diff
        ranges, this will return False if the file is not part of the diff
        data or the line number of the error is not in any of the ranges of
        the diff.

        :returns:
            True if there is no diff or if the error is in the diff's line
            number ranges. False if the error's line number falls outside
            the diff's line number ranges.
        :rtype:
            bool
        """
        if not diff:
            return True

        # NOTE(sigmavirus24): The parsed diff will be a defaultdict with
        # a set as the default value (if we have received it from
        # flake8.utils.parse_unified_diff). In that case ranges below
        # could be an empty set (which is False-y) or if someone else
        # is using this API, it could be None. If we could guarantee one
        # or the other, we would check for it more explicitly.
        line_numbers = diff.get(self.filename)
        if not line_numbers:
            return False

        return self.line_number in line_numbers


class DecisionEngine(object):
    """A class for managing the decision process around violations.

    This contains the logic for whether a violation should be reported or
    ignored.
    """

    def __init__(self, options):
        """Initialize the engine."""
        self.cache = {}
        self.selected = tuple(options.select)
        self.extended_selected = tuple(sorted(
            options.extended_default_select,
            reverse=True,
        ))
        self.enabled_extensions = tuple(options.enable_extensions)
        self.all_selected = tuple(sorted(
            self.selected + self.enabled_extensions,
            reverse=True,
        ))
        self.ignored = tuple(sorted(options.ignore, reverse=True))
        self.using_default_ignore = set(self.ignored) == set(defaults.IGNORE)
        self.using_default_select = (
            set(self.selected) == set(defaults.SELECT)
        )

    def _in_all_selected(self, code):
        return self.all_selected and code.startswith(self.all_selected)

    def _in_extended_selected(self, code):
        return (self.extended_selected and
                code.startswith(self.extended_selected))

    def was_selected(self, code):
        # type: (str) -> Union[Selected, Ignored]
        """Determine if the code has been selected by the user.

        :param str code:
            The code for the check that has been run.
        :returns:
            Selected.Implicitly if the selected list is empty,
            Selected.Explicitly if the selected list is not empty and a match
            was found,
            Ignored.Implicitly if the selected list is not empty but no match
            was found.
        """
        if self._in_all_selected(code):
            return Selected.Explicitly

        if not self.all_selected and self._in_extended_selected(code):
            # If it was not explicitly selected, it may have been implicitly
            # selected because the check comes from a plugin that is enabled by
            # default
            return Selected.Implicitly

        return Ignored.Implicitly

    def was_ignored(self, code):
        # type: (str) -> Union[Selected, Ignored]
        """Determine if the code has been ignored by the user.

        :param str code:
            The code for the check that has been run.
        :returns:
            Selected.Implicitly if the ignored list is empty,
            Ignored.Explicitly if the ignored list is not empty and a match was
            found,
            Selected.Implicitly if the ignored list is not empty but no match
            was found.
        """
        if self.ignored and code.startswith(self.ignored):
            return Ignored.Explicitly

        return Selected.Implicitly

    def more_specific_decision_for(self, code):
        # type: (Violation) -> Decision
        select = find_first_match(code, self.all_selected)
        extra_select = find_first_match(code, self.extended_selected)
        ignore = find_first_match(code, self.ignored)

        if select and ignore:
            # If the violation code appears in both the select and ignore
            # lists (in some fashion) then if we're using the default ignore
            # list and a custom select list we should select the code. An
            # example usage looks like this:
            #   A user has a code that would generate an E126 violation which
            #   is in our default ignore list and they specify select=E.
            # We should be reporting that violation. This logic changes,
            # however, if they specify select and ignore such that both match.
            # In that case we fall through to our find_more_specific call.
            # If, however, the user hasn't specified a custom select, and
            # we're using the defaults for both select and ignore then the
            # more specific rule must win. In most cases, that will be to
            # ignore the violation since our default select list is very
            # high-level and our ignore list is highly specific.
            if self.using_default_ignore and not self.using_default_select:
                return Decision.Selected
            return find_more_specific(select, ignore)
        if extra_select and ignore:
            # At this point, select is false-y. Now we need to check if the
            # code is in our extended select list and our ignore list. This is
            # a *rare* case as we see little usage of the extended select list
            # that plugins can use, so I suspect this section may change to
            # look a little like the block above in which we check if we're
            # using our default ignore list.
            return find_more_specific(extra_select, ignore)
        if select or (extra_select and self.using_default_select):
            # Here, ignore was false-y and the user has either selected
            # explicitly the violation or the violation is covered by
            # something in the extended select list and we're using the
            # default select list. In either case, we want the violation to be
            # selected.
            return Decision.Selected
        if (select is None and
                (extra_select is None or not self.using_default_ignore)):
            return Decision.Ignored
        if ((select is None and not self.using_default_select) and
                (ignore is None and self.using_default_ignore)):
            return Decision.Ignored
        return Decision.Selected

    def make_decision(self, code):
        """Decide if code should be ignored or selected."""
        LOG.debug('Deciding if "%s" should be reported', code)
        selected = self.was_selected(code)
        ignored = self.was_ignored(code)
        LOG.debug('The user configured "%s" to be "%s", "%s"',
                  code, selected, ignored)

        if ((selected is Selected.Explicitly or
             selected is Selected.Implicitly) and
                ignored is Selected.Implicitly):
            decision = Decision.Selected
        elif ((selected is Selected.Explicitly and
              ignored is Ignored.Explicitly) or
              (selected is Ignored.Implicitly and
               ignored is Selected.Implicitly)):
            decision = self.more_specific_decision_for(code)
        elif (selected is Ignored.Implicitly or
              ignored is Ignored.Explicitly):
            decision = Decision.Ignored  # pylint: disable=R0204
        return decision

    def decision_for(self, code):
        # type: (str) -> Decision
        """Return the decision for a specific code.

        This method caches the decisions for codes to avoid retracing the same
        logic over and over again. We only care about the select and ignore
        rules as specified by the user in their configuration files and
        command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param str code:
            The code for the check that has been run.
        """
        decision = self.cache.get(code)
        if decision is None:
            decision = self.make_decision(code)
            self.cache[code] = decision
            LOG.debug('"%s" will be "%s"', code, decision)
        return decision


class StyleGuide(object):
    """Manage a Flake8 user's style guide."""

    def __init__(self, options, listener_trie, formatter, decider=None):
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """
        self.options = options
        self.listener = listener_trie
        self.formatter = formatter
        self.stats = statistics.Statistics()
        self.decider = decider or DecisionEngine(options)
        self._parsed_diff = {}

    @contextlib.contextmanager
    def processing_file(self, filename):
        """Record the fact that we're processing the file's results."""
        self.formatter.beginning(filename)
        yield self
        self.formatter.finished(filename)

    def should_report_error(self, code):
        # type: (str) -> Decision
        """Determine if the error code should be reported or ignored.

        This method only cares about the select and ignore rules as specified
        by the user in their configuration files and command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param str code:
            The code for the check that has been run.
        """
        return self.decider.decision_for(code)

    def handle_error(self, code, filename, line_number, column_number, text,
                     physical_line=None):
        # type: (str, str, int, int, str) -> int
        """Handle an error reported by a check.

        :param str code:
            The error code found, e.g., E123.
        :param str filename:
            The file in which the error was found.
        :param int line_number:
            The line number (where counting starts at 1) at which the error
            occurs.
        :param int column_number:
            The column number (where counting starts at 1) at which the error
            occurs.
        :param str text:
            The text of the error message.
        :param str physical_line:
            The actual physical line causing the error.
        :returns:
            1 if the error was reported. 0 if it was ignored. This is to allow
            for counting of the number of errors found that were not ignored.
        :rtype:
            int
        """
        disable_noqa = self.options.disable_noqa
        # NOTE(sigmavirus24): Apparently we're provided with 0-indexed column
        # numbers so we have to offset that here. Also, if a SyntaxError is
        # caught, column_number may be None.
        if not column_number:
            column_number = 0
        error = Violation(code, filename, line_number, column_number + 1,
                          text, physical_line)
        error_is_selected = (self.should_report_error(error.code) is
                             Decision.Selected)
        is_not_inline_ignored = error.is_inline_ignored(disable_noqa) is False
        is_included_in_diff = error.is_in(self._parsed_diff)
        if (error_is_selected and is_not_inline_ignored and
                is_included_in_diff):
            self.formatter.handle(error)
            self.stats.record(error)
            self.listener.notify(error.code, error)
            return 1
        return 0

    def add_diff_ranges(self, diffinfo):
        """Update the StyleGuide to filter out information not in the diff.

        This provides information to the StyleGuide so that only the errors
        in the line number ranges are reported.

        :param dict diffinfo:
            Dictionary mapping filenames to sets of line number ranges.
        """
        self._parsed_diff = diffinfo


def find_more_specific(selected, ignored):
    if selected.startswith(ignored) and selected != ignored:
        return Decision.Selected
    return Decision.Ignored


def find_first_match(error_code, code_list):
    startswith = error_code.startswith
    for code in code_list:
        if startswith(code):
            break
    else:
        return None
    return code
