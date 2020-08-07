import unittest
from unbalanced import Unbalanced


class TestSummaries(unittest.TestCase):
    unbalanced_lines_chars = [['(]', 0, 1, '(]', '(]'],
                              ['a(b]', 1, 3, 'a(b]', 'a(b]'],
                              ['(abcde]', 0, 3, '(abc...', '(abcde]'],
                              ['abc(defghij]', 3, 11, 'abc(def...', 'abc(defghij]'],
                              ['abcde(fgh]ij', 5, 9, 'abcde(fgh...', 'abcde(fgh]ij'],
                              ['abcdef(gh]ij', 6, 9, '...def(gh]ij', '...def(gh]ij'],
                              ['abcdef(ghijkl]mno', 6, 13, '...def(ghi...', '...def(ghijkl]mno'],
                              ['abcdef(ghijkl]mnopq', 6, 13, '...def(ghi...', '...def(ghijkl]mnopq'],
                              ['abcdef(ghijkl]mnopqr', 6, 13, '...def(ghi...', '...def(ghijkl]mno...'],
                              ['abcdefgh(ijkl]mnopqrst', 8, 13, '...fgh(ijk...', '...fgh(ijkl]mno...']]

    unbalanced_lines_long = [['<i>]', 3, 0, 1, 3, '<i>]', '<i>]', '<i>'],
                             ['a<i>b</b>', 3, 1, 4, 5, 'a<i>b</b>', 'a<i>b</b>', '<i>'],
                             ['abcde<h1>fgh</h2>ij', 4, 5, 5, 12, 'abcde<h1>fgh...', 'abcde<h1>fgh</h2>ij', '<h1>'],
                             ['abcdef<i>gh</blah>ij', 3, 6, 6, 11, '...def<i>gh<...', '...def<i>gh</blah>ij', '<i>'],
                             ['abcdef(ghijkl</i>mnopq', 1, 6, 4, 13, '...def(ghi...', '...def(ghijkl</i>mnopq', '('],
                             ['abcdef<p>ghijkl]mnopqr', 3, 6, 1, 15, '...def<p>ghi...',
                              '...def<p>ghijkl]mno...', '<p>']]

    unbalanced_lines_without_ending = [['(', 0, 1, '(', '(', '('],
                                       ['a(b', 1, 1, 'a(b', 'a(b', '('],
                                       ['(abcde', 0, 1, '(abcde', '(abcde', '('],
                                       ['abc(defghij', 3, 1, 'abc(def...', 'abc(defghij', '('],
                                       ['abcde<i>fghij', 5, 3, 'abcde<i>fghij', 'abcde<i>fghij', '<i>'],
                                       ['abcde<i>fghijk', 5, 3, 'abcde<i>fgh...', 'abcde<i>fghijk', '<i>'],
                                       ['abcdef(ghijklmnopq', 6, 1, '...def(ghi...', '...def(ghijklmnopq', '('],
                                       ['abcdefgh<menu>ijklmnopqrst', 8, 6, '...fgh<menu>ijk...',
                                        '...fgh<menu>ijklmnopqrst', '<menu>']]

    unbalanced_lines_without_beginning = [[')', 0, 1, ')'],
                                          ['a)b', 1, 1, 'a)b'],
                                          ['abcde)', 5, 1, 'abcde)'],
                                          ['abcdefg)hij', 7, 1, 'abcdefg)hij'],
                                          ['abcde</i>fghijk', 5, 4, 'abcde</i>fgh...'],
                                          ['abcdef)ghijklmnopq', 6, 1, 'abcdef)ghi...'],
                                          ['abcdefgh</menu>ijklmnopqrst', 8, 7, 'abcdefgh</menu>ijk...']]

    def test_summaries_chars(self):
        for string, opening_pos, closing_pos, short_summary, long_summary in self.unbalanced_lines_chars:
            with self.subTest(msg=string):
                unbalanced = Unbalanced(string, 1, opening_pos, 1, closing_pos)
                self.assertEqual(unbalanced.short_summary, short_summary)
                self.assertEqual(unbalanced.long_summary, long_summary)
                self.assertEqual(unbalanced.unclosed, '(')

    def test_summaries_long_brackets(self):
        for string, opening_length, opening_pos, closing_length, closing_pos, short_summary, long_summary, unclosed \
                in self.unbalanced_lines_long:
            with self.subTest(msg=string):
                unbalanced = Unbalanced(string, opening_length, opening_pos, closing_length, closing_pos)
                self.assertEqual(unbalanced.short_summary, short_summary)
                self.assertEqual(unbalanced.long_summary, long_summary)
                self.assertEqual(unbalanced.unclosed, unclosed)

    def test_long_summaries_without_ending(self):
        for string, opening_pos, opening_length, short_summary, long_summary, unclosed \
                in self.unbalanced_lines_without_ending:
            with self.subTest(msg=string):
                unbalanced = Unbalanced(string, opening_length, opening_pos)
                self.assertEqual(unbalanced.short_summary, short_summary)
                self.assertEqual(unbalanced.long_summary, long_summary)
                self.assertEqual(unbalanced.unclosed, unclosed)

    def test_long_summaries_without_beginning(self):
        for string, closing_pos, closing_length, summary in self.unbalanced_lines_without_beginning:
            with self.subTest(msg=string):
                unbalanced = Unbalanced(string, 0, 0, closing_length, closing_pos)
                self.assertEqual(unbalanced.short_summary, summary)
                self.assertEqual(unbalanced.long_summary, summary)
                self.assertEqual(unbalanced.unclosed, '')
