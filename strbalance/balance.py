from .unbalanced import Unbalanced


class Balance:
    u"""Balance checker for strings with given balancing parameters.

    Class exports method is_balanced() which takes string as a parameter. The method returns None if the string is
    balanced or an Unbalanced object otherwise (see help(Unbalanced) for more details).

    The pairs of characters matched by default (listed in BRACKETS and FRENCH_QUOTES):
    (…)  parentheses
    […]  brackets
    {…}  braces
    “…”  double quotes
    ‘…’  single quotes
    «…»  double angle quotes
    ‹…›  single angle quotes

    Constructor takes the following optional parameters.
        pairs and symmetrical default to None:
            pairs           A list containing pairs of strings in the following format:
                            [['a-opening'], ['a-closing'], ['b-opening', 'b-closing'] ...]
            symmetrical     A list of strings representing characters (or their sequences) which have identical opening
                            and closing forms.

        All other parameters are boolean and default to False:
            tags            Match HTML (XML) paired tags (case sensitive), except those in UNPAIRED_TAGS, which are
                            normally not closed in HTML.
            ignore_case     Ignore case in tags.
            cjk             Include CJK brackets and quotation signs listed in CJK_PUNCTUATION: ｢…｣, 「…」, 〈…〉, 《…》,
                            『…』, （…）, ［…］, ＜…＞, ｛…｝, ｟…｠, 【…】, 〔…〕, 〖…〗, 〘…〙, 〚…〛.
            straight        Include straight quotation marks (single and double) (listed in STRAIGHT).
            custom          Balance only custom characters and character sequences.
            german          Use German quoting convention: „…“, ‚…‘, »…«, ›…‹ (GERMAN_QUOTES)
                            instead of “…”, ‘…’, «…», ‹…› (FRENCH_QUOTES).
            math            Match parentheses with brackets in order to include mathematical [a,c) notation (additional
                            pairs to match are listed in ADDITIONAL_MATH_PAIRS).
    """

    BRACKETS = [['(', ')'], ['[', ']'], ['{', '}']]
    FRENCH_QUOTES = [['“', '”'], ['‘', '’'], ['«', '»'], ['‹', '›']]
    GERMAN_QUOTES = [['„', '“'], ['‚', '‘'], ['»', '«'], ['›', '‹']]
    CJK_PUNCTUATION = [['｢', '｣'], ['「', '」'], ['〈', '〉'], ['《', '》'], ['『', '』'], ['（', '）'], ['［', '］'],
                       ['＜', '＞'], ['｛', '｝'], ['｟', '｠'], ['【', '】'], ['〔', '〕'], ['〖', '〗'], ['〘', '〙'],
                       ['〚', '〛']]
    STRAIGHT = ['"', "'"]
    ADDITIONAL_MATH_PAIRS = [['(', ']'], ['[', ')']]
    UNPAIRED_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link',
                     'menuitem', 'meta', 'param', 'source', 'track', 'wbr']

    LATIN_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    TAG_BEGIN = '<'
    TAG_END = '>'
    TAG_CLOSE = '/'

    PUNCTUATION_TYPES = {'non-tag': 0, 'incomplete-tag': 1, 'opened-tag': 2}

    def __init__(self, pairs=None, symmetrical=None, tags=False, ignore_case=False, cjk=False, straight=False,
                 custom=False, german=False, math=False):
        """Initialize Balance object with given balancing parameters (see help(Balance) for more details)."""
        if pairs:
            if not isinstance(pairs, list):
                raise TypeError("pairs argument must be a list")
        if symmetrical:
            if not isinstance(symmetrical, list):
                raise TypeError("symmetrical argument must be a list")

        self._compile_punctuation_lists(pairs, symmetrical, cjk, straight, custom, german, math)
        self._tags = tags
        self._ignore_case = ignore_case

        if tags and (self.TAG_BEGIN in self._openings + self._closings + self._symmetrical or
                     self.TAG_END in self._openings + self._closings + self._symmetrical):
            raise Exception("can't process tags and angle brackets simultaneously")

        self._punctuation_stack = []  # [line, position, type]
        self._string = None

    def _closing_tag_processing(self, position):
        if self._string[position + 2] not in self.LATIN_LETTERS:
            return Unbalanced(self._string, 1, position)  # Incomplete tag (not tag name)
        for i in range(position + 3, len(self._string)):  # Iterating through the tag name
            if self._string[i] not in self.LATIN_LETTERS:
                if self._string[i] == self.TAG_END:
                    if not self._punctuation_stack:
                        return Unbalanced(self._string, 0, 0, i - position + 1, position)
                    if self._punctuation_stack[-1][2] != self.PUNCTUATION_TYPES['opened-tag']:
                        return Unbalanced(self._string,
                                          len(self._punctuation_stack[-1][0]), self._punctuation_stack[-1][1],
                                          i - position + 1, position)

                    tag_opening = self._punctuation_stack[-1][0][1:-1]
                    tag_closing = self._string[position + 2:i]
                    if self._ignore_case:
                        tag_opening = tag_opening.lower()
                        tag_closing = tag_closing.lower()
                    if tag_opening == tag_closing:
                        self._punctuation_stack = self._punctuation_stack[:-1]
                        return self._iteration_on_string(i + 1)
                    else:
                        return Unbalanced(self._string,
                                          len(self._punctuation_stack[-1][0]), self._punctuation_stack[-1][1],
                                          i - position + 1, position)
                else:
                    return Unbalanced(self._string, 1, position)  # Incomplete tag

        return Unbalanced(self._string, len(self._string) - position, position)  # Incomplete tag (no TAG_END)

    def _tags_iteration(self, position):
        if self._string[position] == self.TAG_BEGIN:
            if self._punctuation_stack and self._punctuation_stack[-1][-1] == self.PUNCTUATION_TYPES['incomplete-tag']:
                return Unbalanced(self._string, len(self._punctuation_stack[-1][0]), self._punctuation_stack[-1][1])
            if self._string[position + 1] == self.TAG_CLOSE:
                return self._closing_tag_processing(position)
            elif self._string[position + 1] not in self.LATIN_LETTERS:
                return Unbalanced(self._string, 1, position)  # Incomplete tag
            else:
                for i in range(position + 2, len(self._string)):  # Iterating through the tag name
                    if self._string[i] not in self.LATIN_LETTERS:
                        self._punctuation_stack.append([self._string[position:i], position,
                                                        self.PUNCTUATION_TYPES['incomplete-tag']])
                        return self._iteration_on_string(i)
                return Unbalanced(self._string, 1, position)  # Incomplete tag

        elif self._string[position] == self.TAG_END:
            if not self._punctuation_stack:
                return Unbalanced(self._string, 0, 0, 1, position)

            last_punctuation = self._punctuation_stack[-1]
            if last_punctuation[2] == self.PUNCTUATION_TYPES['incomplete-tag']:
                if self._string[position - 1] == self.TAG_CLOSE:  # Self-closing tag, e.g. <something/>
                    self._punctuation_stack = self._punctuation_stack[:-1]
                    return self._iteration_on_string(position + 1)
                else:
                    if last_punctuation[0][1:].lower() in self.UNPAIRED_TAGS:
                        self._punctuation_stack = self._punctuation_stack[:-1]
                        return self._iteration_on_string(position + 1)
                    else:
                        self._punctuation_stack[-1] = [last_punctuation[0] + self.TAG_END, last_punctuation[1],
                                                       self.PUNCTUATION_TYPES['opened-tag']]
                        return self._iteration_on_string(position + 1)
            else:
                return Unbalanced(self._string, len(self._punctuation_stack[-1][0]), self._punctuation_stack[-1][1],
                                  1, position)

        return self._iteration_on_string(position + 1)  # Not tags found

    def _iteration_on_string(self, position):
        if position >= len(self._string):  # String ended
            if not self._punctuation_stack:
                return None
            else:
                return Unbalanced(self._string, len(self._punctuation_stack[-1][0]), self._punctuation_stack[-1][1])

        for closing in self._closings:
            if self._string[position:position + len(closing)] == closing:
                if self._punctuation_stack:
                    if [self._punctuation_stack[-1][0], closing] in self._pairs:
                        self._punctuation_stack = self._punctuation_stack[:-1]
                        return self._iteration_on_string(position + len(closing))
                    else:
                        return Unbalanced(self._string, len(self._punctuation_stack[-1][0]),
                                          self._punctuation_stack[-1][1], len(closing), position)
                return Unbalanced(self._string, 0, 0, len(closing), position)   # empty stack

        for symmetrical in self._symmetrical:
            if self._string[position:position + len(symmetrical)] == symmetrical:
                if len(self._punctuation_stack) and self._punctuation_stack[-1][0] == symmetrical:
                    self._punctuation_stack = self._punctuation_stack[:-1]
                else:
                    self._punctuation_stack.append([symmetrical, position, self.PUNCTUATION_TYPES['non-tag']])
                return self._iteration_on_string(position + len(symmetrical))

        for opening in self._openings:
            if self._string[position:position + len(opening)] == opening:
                self._punctuation_stack.append([opening, position, self.PUNCTUATION_TYPES['non-tag']])
                return self._iteration_on_string(position + len(opening))

        if self._tags:
            return self._tags_iteration(position)

        return self._iteration_on_string(position + 1)

    def is_unbalanced(self, string):
        """Check if the string is balanced and return None or an Unbalanced object."""
        if not isinstance(string, str):
            raise TypeError("first argument must be string")

        self._string = string
        self._punctuation_stack = []

        return self._iteration_on_string(0)

    def _compile_punctuation_lists(self, pairs, symmetrical, cjk, straight, custom, german, math):
        self._pairs = []
        self._symmetrical = []

        if pairs:
            for pair in pairs:
                if len(pair) != 2:
                    raise ValueError('pairs must contain two elements each')
                if len(pair[0]) > 1 or len(pair[1]) > 1:
                    self._pairs.append(pair)
                else:
                    self._pairs.append(pair)

        if symmetrical:
            for element in symmetrical:
                if len(element) > 1:
                    self._symmetrical.append(element)
                else:
                    self._symmetrical.append(element)

        if cjk:
            self._pairs.extend(self.CJK_PUNCTUATION)

        if german:
            self._pairs.extend(self.GERMAN_QUOTES)
        elif not custom:
            self._pairs.extend(self.FRENCH_QUOTES)

        if not custom:
            self._pairs.extend(self.BRACKETS)

        if math:
            self._pairs.extend(self.ADDITIONAL_MATH_PAIRS)

        if straight:
            self._symmetrical.extend(self.STRAIGHT)

        self._closings = sorted(list(set([pair[1] for pair in self._pairs])), key=len, reverse=True)
        self._openings = sorted(list(set([pair[0] for pair in self._pairs])), key=len, reverse=True)
        self._symmetrical = sorted(list(set(self._symmetrical)), key=len, reverse=True)

        for symmetrical in self._symmetrical:
            if symmetrical in self._openings or symmetrical in self._closings:
                raise ValueError('{} found both in symmetrical and in pairs'.format(symmetrical))

        for opening in self._openings:
            if opening in self._closings:
                raise ValueError('{} found both as opening and as closing sequence'.format(opening))


if __name__ == '__main__':
    import strbalance

    balance = strbalance.Balance()
    unbalanced = balance.is_unbalanced('abcdefgh(ijkl]mnopqrst')
    print(unbalanced.unclosed, unbalanced.short_summary,
          unbalanced.long_summary)  # outputs ( ...{}}(()[... ...{}}(()[]]""[...
    print(unbalanced.opening_position, unbalanced.opening_length,
          unbalanced.closing_position, unbalanced.closing_length)  # outputs 7 1 12 1
