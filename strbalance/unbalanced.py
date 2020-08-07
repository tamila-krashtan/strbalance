class Unbalanced:
    """The left-most unbalanced part of the string, obtained from Balance check.

    Attributes:
        string                  The whole string found out to be unbalanced.
        opening_length          The length of the opening element which was not closed.
        opening_position        The position of the opening element which was not closed.
        closing_length          The length of the closing element which was not opened.
        closing_position        The position of the closing element which was not opened.
        short_summary           The unclosed opening element and the context around it as a string.
        long_summary            The unmatched elements and the context between and around them as a string.
        unclosed                The opening element which was not closed or empty string.

    Class constants:
        SUMMARY_TAIL_LENGTH     Standard length of the context around opening and closing elements.
        SUMMARY_MAX_TAIL_LENGTH Maximum length of the context around opening and closing elements.
    """

    SUMMARY_TAIL_LENGTH = 3
    SUMMARY_MAX_TAIL_LENGTH = 5

    def __init__(self, string, opening_length, opening_position, closing_length=0, closing_position=0):
        """Initialize Unbalanced with opening length and position, and optional closing length and position."""
        self._string = string
        self._opening_length = opening_length
        self._opening_position = opening_position
        self._closing_length = closing_length
        self._closing_position = closing_position
        self._short_summary = None
        self._long_summary = None
        self._unclosed = self._string[self._opening_position:self._opening_position + self._opening_length]

    def _generate_short_summary(self):
        if self._opening_length == 0:
            self._short_summary = self.long_summary
            return

        if self._opening_position <= self.SUMMARY_MAX_TAIL_LENGTH:
            self._short_summary = self._string[:self._opening_position]
        else:
            self._short_summary = '...' + self._string[self._opening_position - self.SUMMARY_TAIL_LENGTH:
                                                       self._opening_position]

        if len(self._string) - (self._opening_position + self._opening_length) <= self.SUMMARY_MAX_TAIL_LENGTH:
            self._short_summary = self._short_summary + self._string[self._opening_position:]
        else:
            self._short_summary = self._short_summary + self._string[self._opening_position:
                                                                     self._opening_position + self._opening_length +
                                                                     self.SUMMARY_TAIL_LENGTH] + '...'

    def _generate_long_summary(self):
        closing = self._closing_position or len(self._string)

        if self._opening_position <= self.SUMMARY_MAX_TAIL_LENGTH:
            self._long_summary = self._string[:closing]
        else:
            self._long_summary = '...' + self._string[self._opening_position - self.SUMMARY_TAIL_LENGTH:closing]

        if len(self._string) - (closing + self._closing_length) <= self.SUMMARY_MAX_TAIL_LENGTH:
            self._long_summary = self._long_summary + self._string[closing:]
        else:
            self._long_summary = self._long_summary + self._string[closing: closing + self._closing_length +
                                                                   self.SUMMARY_TAIL_LENGTH] + '...'

    @property
    def short_summary(self):
        """Return the unclosed opening element and the context around it as a string."""
        if not self._short_summary:
            self._generate_short_summary()
        return self._short_summary

    @property
    def long_summary(self):
        """Return the unmatched elements and the context between and around them as a string."""
        if not self._long_summary:
            self._generate_long_summary()
        return self._long_summary

    @property
    def opening_position(self):
        """Return the position of the opening element which was not closed."""
        return self._opening_position

    @property
    def closing_position(self):
        """Return the position of the closing element which was not opened."""
        return self._closing_position

    @property
    def opening_length(self):
        """Return the length of the opening element which was not closed."""
        return self._opening_length

    @property
    def closing_length(self):
        """Return the length of the closing element which was not opened."""
        return self._closing_length

    @property
    def unclosed(self):
        """Return the opening element which was not closed as a string or an empty string."""
        return self._unclosed
