# strbalance

This small Python library provides functionality to check whether brackets, quotation marks, tags etc. inside the string are balanced, i.e. whether each of them is opened and closed properly with respect to other punctuation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `strbalance`:

```bash
pip install strbalance
```

## Usage

If the punctuation in the string is not balanced, the result is an Unbalanced object, `None` otherwise:

```python
import strbalance

balance = strbalance.Balance()
print(balance.is_unbalanced('{[]}[()]'))  # outputs None
print(balance.is_unbalanced('abc(def"gh"ijkl)'))  # outputs None

unbalanced = balance.is_unbalanced('abcdefgh(ijkl]mnopqrst')
print(unbalanced.unclosed, unbalanced.short_summary, 
        unbalanced.long_summary)  # outputs ( ...fgh(ijk... ...fgh(ijkl]mno...
print(unbalanced.opening_position, unbalanced.opening_length,
        unbalanced.closing_position, unbalanced.closing_length)  # outputs 8 1 13 1
```

Istead of

```python
import strbalance
balance = strbalance.Balance()
balance.is_unbalanced('{[]}[()]')
```

one can simply write

```python
import strbalance
strbalance.is_unbalanced('{[]}[()]')
```

Apart from the string to check, `strbalance.is_unbalanced()` accepts all the optional parameters which can be passed to `Balance` constructor:

- `pairs` and `symmetrical` are lists of additional characters (or lines) to match; they default to `None`:
    - `pairs` – a list containing pairs of strings in the following format: 
    
        `[['a-opening'], ['a-closing'], ['b-opening', 'b-closing'] ...]`
    
    - `symmetrical` – a list of strings representing characters (or their sequences) which have identical opening and closing forms.
- All other parameters are boolean and default to `False`:
    - `tags` – match HTML (XML) paired tags (case sensitive).
    - `ignore_case` – ignore case in tags.
    - `cjk` – include CJK brackets and quotation signs: ｢…｣, 「…」, 〈…〉, 《…》, 『…』, （…）, ［…］, ＜…＞, ｛…｝, ｟…｠, 【…】, 〔…〕, 〖…〗, 〘…〙, 〚…〛.
    - `straight` – include straight quotation marks (single and double).
    - `custom` - balance only custom characters and character sequences (listed in `pairs` and `symmetrical` and/or added with other parameters).
    - `german` - use German quoting convention: „…“, ‚…‘, »…«, ›…‹ instead of “…”, ‘…’, «…», ‹…›.
    - `math` - match parentheses with brackets in order to include mathematical [a,c) notation.
    
The pairs of characters matched by default:
 - (…)  parentheses
 - […]  brackets
 - {…}  braces
 - “…”  double quotes
 - ‘…’  single quotes
 - «…»  double angle quotes
 - ‹…›  single angle quotes

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).