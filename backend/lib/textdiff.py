import difflib


def save_couple(a, b):
    return [a, b]


def diff(a, b):
    return ''.join(difflib.unified_diff(
        (a or '').splitlines(keepends=True),
        (b or '').splitlines(keepends=True)
    ))
