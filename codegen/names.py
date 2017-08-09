"""Utilities for normalizing identifiers."""
import re

INPUT_TYPES = [(r'^\w*$', r'(?P<term>[a-z]+|[A-Z][a-z]*|[0-9]+)'),
               (r'', r'(?P<term>[^\\\/\-_\s]+)')]


class SimpleFormat:
    """Generic formatter for various naming conventions."""
    def __init__(self, delimeter, format_term=None):
        self.delimeter = delimeter
        if format_term:
            self.format_term = format_term

    def __call__(self, terms):
        return self.delimeter.join(self.format_term(term) for term in terms)

    def format_term(term):
        return term


def smart_capitalize(value):
    """Return value if it is all-caps, otherwise capitalize the first letter."""
    return value if re.match(r'[A-Z]+', value) else value.capitalize()


def parse_terms(value):
    """Split an identifier into terms."""
    for pattern, terms in INPUT_TYPES:
        if re.search(pattern, value):
            return [m.group('term') for m in re.finditer(terms, value)]


def format_as(value, output_format, input_parser=parse_terms):
    """Parse an identifier, and reformat it a different way."""
    return FORMAT_NAMES[output_format](input_parser(value))


# Simple format styles
CamelCase = SimpleFormat('', smart_capitalize)
KebabCase = SimpleFormat('-', str.lower)
SnakeCase = SimpleFormat('_', str.lower)
TitleCase = SimpleFormat(' ', str.capitalize)
UpperSnakeCase = SimpleFormat('_', str.upper)

# Format aliases
FORMAT_NAMES = {
    'class': CamelCase,
    'constant': UpperSnakeCase,
    'function': SnakeCase,
    'module': SnakeCase
}
