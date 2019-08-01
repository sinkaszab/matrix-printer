from collections import namedtuple
from functools import partial, reduce
from itertools import repeat
from pydash import flow_right as compose

a_matrix = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'],
            ['m', 'n', 'o', 'p'], ['q', 'r', 's', 't']]

b_matrix = [[1, 2], [3, 4]]


def init(source):
    cols_to_str = compose(list, partial(map, str))
    fields_to_str = compose(list, partial(map, cols_to_str))
    return {'source': fields_to_str(source)}


longest_item_in_list = compose(max, partial(map, len))


def longest_item(matrix):
    process_rows = partial(map, longest_item_in_list)
    max_col_length = compose(max, process_rows)
    return {**matrix, 'max_col_length': max_col_length(matrix['source'])}


def size(matrix):
    m = matrix['source']
    height = len(m)
    width = len(list(m[0]))
    return {**matrix, 'width': width, 'height': height}


def calc_row_width(matrix, spacing):
    all_spacing = matrix['width'] * spacing + 1
    all_margin_chars = matrix['max_col_length'] * matrix['width']
    return all_spacing + all_margin_chars


def put(line, matrix):
    print_list = matrix.get('print', [])
    return {**matrix, 'print': [*print_list, line]}


render = compose(''.join, list)


def memoize_chars_and_setup(*, char, spacing=3):
    chars_str = ''

    def print_row_of_chars(matrix):
        nonlocal chars_str
        if not chars_str:
            row_width = calc_row_width(matrix, spacing)
            chars = repeat(char, row_width)
            chars_str = render(chars)
        return put(chars_str, matrix)

    return print_row_of_chars


def format_line(line):
    return '| {row} |'.format(row=' | '.join(line))


def with_setup_print_line(print_empty_line):
    def print_line(line, matrix):
        put_line = partial(put, format_line(line))
        print_comp = compose(print_margin, put_line)
        return print_comp(matrix)

    return print_line


def with_config_print_lines(print_empty_line):
    def print_lines(matrix):
        print_line = with_setup_print_line(print_empty_line)
        return reduce(
            lambda current, row: print_line(row, current),
            matrix['source'], matrix)
    return print_lines


print_margin = memoize_chars_and_setup(char='-')
print_empty_row = memoize_chars_and_setup(char=' ')
print_lines = with_config_print_lines(print_empty_row)

print_matrix = compose(print_lines, print_margin, longest_item, size, init)

printed = print_matrix(a_matrix)

print('\n'.join(printed['print']))

# TODO:
# - Implement left, right and centered padding of field content.
# - When calculating row length, decorator character's length should also be considered.
# - Create a public API.
