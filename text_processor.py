import re


def replace_non_numeric_brackets(data):
    brackets = extract_all_brackets_with_data(data, [])
    for bracket in brackets:
        bracket_data = bracket.replace('(', '').replace(')', '').replace(',', '')
        if all([x.isalpha() for x in bracket_data]):
            data = data.replace(bracket, '')
        if 'cm' not in bracket_data:
            data = data.replace(bracket, '')
    return data


def extract_all_brackets_with_data(data, brackets=[]):
    bracket = re.search(r"\(([A-Za-z0-9_./,-]+)\)", data)
    if bracket:
        bracket = bracket.group(0)
        brackets.append(bracket)
        bracket_count = data.count(bracket)
        data = data.replace(bracket, '')
        if bracket_count > 1:
            data = data + (bracket * (bracket_count - 1))
        extract_all_brackets_with_data(data, brackets)

    return brackets


def extract_regex_pattern_2d(data):
    pattern_cm_decimal = re.search('\d+\.*\d*x{1}\d+\.*\d+', data)
    if pattern_cm_decimal:
        found = pattern_cm_decimal.group(0)
        return found
    else:
        return 'not_processed'


def extract_regex_pattern_3d(data):
    pattern_cm_decimal = re.search('\d+\.*\d+x{1}\d+\.*\d+x{1}\d+\.*\d+', data)
    if pattern_cm_decimal:
        found = pattern_cm_decimal.group(0)
        return found
    else:
        return 'not_processed'


def extract_regex_pattern_1d(data):
    pattern_cm_decimal = re.search('\d+\.*\d*', data)
    if pattern_cm_decimal:
        found = pattern_cm_decimal.group(0)
        return found
    else:
        return 'not_processed'


def extract_cm_inside_single_bracket(bracket):
    if 'cm' in bracket and bracket.count('x') == 2:
        bracket = extract_regex_pattern_3d(bracket)
        return bracket
    if 'cm' in bracket and bracket.count('x') == 1:
        bracket = extract_regex_pattern_2d(bracket)  # extract_numeric_data(bracket)
        return bracket
    elif 'cm' in bracket and 'x' not in bracket:
        bracket = extract_regex_pattern_1d(bracket)  # extract_numeric_data(bracket)
        # return bracket  # 'h. 6 1/2 in. (16.5 cm)'
        return bracket


def extract_image_and_sheet_data(data):
    not_in = ['imageandsheet', 'imagesandsheets', 'image and sheet']
    data = data.replace('image():', '')
    data = data.replace('image(a):', '')
    if any(x in data for x in not_in):
        return data

    return ''.join(
        [x for x in data.split('sheet') if
         'image' in x]) if 'image' in data and 'sheet' in data else data


def truncate_unwanted_part(data):
    unwanted_part = {'averagetextsize': 'overall', 'other': 'overall', 'mount': 'diam'}
    for to_truncate, to_keep in unwanted_part.items():
        if all(x in data for x in [to_truncate, to_keep]):
            return ''.join([y for y in data.split(to_truncate) if to_keep in y])
    return data


def extract_only_valid_dimension(data):
    general_3d = extract_regex_pattern_3d(data)
    general_2d = extract_regex_pattern_2d(data)
    general_1d = extract_regex_pattern_1d(data)
    result = general_3d if general_3d != 'not_processed' else 'not_processed'
    result = result if result != 'not_processed' else general_2d
    result = result if result != 'not_processed' else general_1d
    return result
