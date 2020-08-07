import unittest
from balance import Balance


class TestBalancingExceptions(unittest.TestCase):
    pairs_for_sequences_in_opening_and_closing = [
        [['(+', '('], ['({', '})']],
        [[')', '>'], ['({', '})']],
        [['(+', '>'], ['({', '})'], ['"', '(+']]
    ]

    pairs_not_with_two_elements = [
        [['(+', '>'], ['({', '})'], ['"', '(+', '((']],
        [['>'], ['({', '})'], ['"', '(+']],
        ['(+', '>', '({', '})', '"', '(+']
    ]

    def test_pairs_not_array(self):
        with self.assertRaisesRegex(TypeError, 'pairs argument must be a list'):
            Balance(pairs='someline')

    def test_symmetrical_not_array(self):
        with self.assertRaisesRegex(TypeError, 'symmetrical argument must be a list'):
            Balance(symmetrical='someline')

    def test_tags_and_angle_brackets(self):
        with self.assertRaisesRegex(Exception, "can't process tags and angle brackets simultaneously"):
            Balance(tags=True, symmetrical=['{-', '≥', '>'])
        with self.assertRaisesRegex(Exception, "can't process tags and angle brackets simultaneously"):
            Balance(tags=True, pairs=[['(', '>'], ['({', '})']])

    def test_sequences_in_pairs_and_symmetrical(self):
        with self.assertRaisesRegex(Exception, ".* found both in symmetrical and in pairs"):
            Balance(symmetrical=['{', '≥', '>'])
        with self.assertRaisesRegex(Exception, ".* found both in symmetrical and in pairs"):
            Balance(pairs=[['(+', '>'], ['({', '})']], symmetrical=['({', '-a'])
        with self.assertRaisesRegex(Exception, ".* found both in symmetrical and in pairs"):
            Balance(pairs=[['(+', '>'], ['({', '})'], ['"', '-"']], straight=True)

    def test_sequences_in_opening_and_closing(self):
        for pairs in self.pairs_for_sequences_in_opening_and_closing:
            with self.assertRaisesRegex(Exception, ".* found both as opening and as closing sequence"):
                Balance(pairs=pairs)

    def test_pairs_two_element(self):
        for pairs in self.pairs_not_with_two_elements:
            with self.assertRaisesRegex(ValueError, "pairs must contain two elements each"):
                Balance(pairs=pairs)

    def test_string_not_string(self):
        with self.assertRaisesRegex(TypeError, "first argument must be string"):
            balance = Balance()
            balance.is_unbalanced(15)


class TestBalanceFlags(unittest.TestCase):
    string_not_closed = 'ancd{}efghijk'
    string_closed = 'ancd{}efg{}hijk'
    balance_without_flags = Balance()

    def test_pairs(self):
        balance_with_pairs = Balance(pairs=[['begin', 'end']])

        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('begin')))
        self.assertIsNotNone(balance_with_pairs.is_unbalanced(self.string_not_closed.format('begin')))
        self.assertIsNone(balance_with_pairs.is_unbalanced(self.string_closed.format('begin', 'end')))

    def test_symmetrical(self):
        balance_with_symmetrical = Balance(symmetrical=['--'])

        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('--')))
        self.assertIsNotNone(balance_with_symmetrical.is_unbalanced(self.string_not_closed.format('--')))
        self.assertIsNone(balance_with_symmetrical.is_unbalanced(self.string_closed.format('--', '--')))

    def test_cjk(self):
        balance_with_cjk = Balance(cjk=True)

        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('「')))
        self.assertIsNotNone(balance_with_cjk.is_unbalanced(self.string_not_closed.format('「')))
        self.assertIsNone(balance_with_cjk.is_unbalanced(self.string_closed.format('「', '」')))

    def test_straight(self):
        balance_with_straight = Balance(straight=True)

        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('"')))
        self.assertIsNotNone(balance_with_straight.is_unbalanced(self.string_not_closed.format('"')))
        self.assertIsNone(balance_with_straight.is_unbalanced(self.string_closed.format('"', '"')))

    def test_custom(self):
        balance_with_custom = Balance(custom=True)

        self.assertIsNotNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('(')))
        self.assertIsNone(balance_with_custom.is_unbalanced(self.string_not_closed.format('(')))
        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_closed.format('(', ')')))

    def test_german(self):
        balance_with_german = Balance(german=True)

        self.assertIsNotNone(self.balance_without_flags.is_unbalanced(self.string_closed.format('»', '«')))
        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_closed.format('«', '»')))
        self.assertIsNotNone(balance_with_german.is_unbalanced(self.string_closed.format('«', '»')))
        self.assertIsNone(balance_with_german.is_unbalanced(self.string_closed.format('»', '«')))

    def test_math(self):
        balance_with_math = Balance(math=True)

        self.assertIsNotNone(self.balance_without_flags.is_unbalanced(self.string_closed.format('(', ']')))
        self.assertIsNone(balance_with_math.is_unbalanced(self.string_closed.format('(', ']')))

    def test_tags(self):
        balance_with_tags = Balance(tags=True)
        self.assertIsNone(self.balance_without_flags.is_unbalanced(self.string_not_closed.format('<i>')))
        self.assertIsNotNone(balance_with_tags.is_unbalanced(self.string_not_closed.format('<i>')))
        self.assertIsNone(balance_with_tags.is_unbalanced(self.string_closed.format('<i>', '</i>')))

    def test_ignore_case(self):
        balance_case_sensitive = Balance(tags=True)
        balance_case_insensitive = Balance(tags=True, ignore_case=True)
        self.assertIsNotNone(balance_case_sensitive.is_unbalanced(self.string_closed.format('<i>', '</I>')))
        self.assertIsNone(balance_case_insensitive.is_unbalanced(self.string_closed.format('<i>', '</I>')))
        self.assertIsNone(balance_case_insensitive.is_unbalanced(self.string_closed.format('<i>', '</i>')))


class TestBalanceGeneral(unittest.TestCase):
    # string, opening_length, opening_position, closing_length, closing_position
    simple_unbalanced_strings = [['(]', 1, 0, 1, 1],
                                 ['a(b]', 1, 1, 1, 3],
                                 ['(abcde]', 1, 0, 1, 6],
                                 ['abc(defghij]', 1, 3, 1, 11],
                                 ['abcdef(ghijkl]mno', 1, 6, 1, 13],

                                 ['<i>]', 3, 0, 1, 3],
                                 ['a<i>b</b>', 3, 1, 4, 5],
                                 ['abcdef<p>ghijkl]mnopqr', 3, 6, 1, 15],

                                 ['(', 1, 0, 0, 0],
                                 ['(abcde', 1, 0, 0, 0],
                                 ['abc(defghij', 1, 3, 0, 0],
                                 ['abcdefghij<i>', 3, 10, 0, 0],

                                 [')', 0, 0, 1, 0],
                                 ['a)b', 0, 0, 1, 1],
                                 ['abcde)', 0, 0, 1, 5],
                                 ['abcdef)ghijklmnopq', 0, 0, 1, 6],
                                 ['</menu>abcdefghijklmnopqrst', 0, 0, 7, 0]]

    complex_unbalanced_strings = [['[{}(()[]])', 1, 3, 1, 8],
                                  ['abc(def"gh"ijkl]', 1, 3, 1, 15],
                                  ['(abc"de)', 1, 4, 1, 7],
                                  ['(()((())())', 1, 0, 0, 0],
                                  ['( ( ( ) ] ) )', 1, 2, 1, 8]]

    balanced_strings = ['<a>text<form />text<area>text</a>',
                        '<a>text<form />text<article>text</article>text</a>',
                        'abc(def"gh"ijkl)',
                        'a(bc)<a rel="tag">a[c]</a>',
                        '(?=^(([ac]*[bd]){2})*[ac]*$)(([bd]*[ac]){2})*[bd]*',
                        '{[]}[()]',
                        '{{[[(())]]}}',
                        ]

    incomplete_tags = [['text<atext</a>', 6, 4, 0, 0],
                       ['text<atext<a>', 6, 4, 0, 0],
                       ['text<a>text</atext', 7, 11, 0, 0],
                       ['text<a>text>text', 3, 4, 1, 11]]

    def _unbalanced_assertions(self, unbalanced, opening_length, opening_position, closing_length, closing_position):
        self.assertEqual(unbalanced.opening_position, opening_position)
        self.assertEqual(unbalanced.closing_position, closing_position)
        self.assertEqual(unbalanced.opening_length, opening_length)
        self.assertEqual(unbalanced.closing_length, closing_length)

    def test_simple_unbalanced(self):
        balance = Balance(tags=True)
        for string, opening_length, opening_position, closing_length, closing_position \
                in self.simple_unbalanced_strings:
            with self.subTest(msg=string):
                unbalanced = balance.is_unbalanced(string)
                self._unbalanced_assertions(unbalanced,
                                            opening_length, opening_position, closing_length, closing_position)

    def test_complex_unbalanced(self):
        balance = Balance(tags=True, straight=True)
        for string, opening_length, opening_position, closing_length, closing_position \
                in self.complex_unbalanced_strings:
            with self.subTest(msg=string):
                unbalanced = balance.is_unbalanced(string)
                self._unbalanced_assertions(unbalanced,
                                            opening_length, opening_position, closing_length, closing_position)

    def test_incomplete_tags(self):
        balance = Balance(tags=True, straight=True)
        for string, opening_length, opening_position, closing_length, closing_position in self.incomplete_tags:
            with self.subTest(msg=string):
                unbalanced = balance.is_unbalanced(string)
                self._unbalanced_assertions(unbalanced, opening_length, opening_position,
                                            closing_length, closing_position)

    def test_balanced(self):
        balance = Balance(tags=True, straight=True)
        for string in self.balanced_strings:
            with self.subTest(msg=string):
                self.assertIsNone(balance.is_unbalanced(string))
