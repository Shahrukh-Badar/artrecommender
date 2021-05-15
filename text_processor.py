import re
import pandas as pd
import constant as constant


class TextProcessor:
    @staticmethod
    def process_brackets(data):
        brackets = TextProcessor.extract_all_brackets_with_data(data, [])
        for bracket in brackets:
            bracket_data = bracket.replace('(', '').replace(')', '').replace(',', '')
            if all([x.isalpha() for x in bracket_data]):
                data = data.replace(bracket, '')
            if constant.STR_CM not in bracket_data:
                data = data.replace(bracket, '')
            if not any([x.isnumeric() for x in bracket_data]):
                data = data.replace(bracket, '', 1)
        return data

    @staticmethod
    def post_process_brackets(data):
        # remove cm for such cases (70.8cmx87.3cmx84.5cm) so that regex can work
        return data.replace('diam', '').replace(constant.STR_CM, '').replace('h', '').replace('d', '')

    @staticmethod
    def extract_all_brackets_with_data(data, brackets=[]):
        bracket = re.search(r"\(([A-Za-z0-9_./,-]+)\)", data)
        if bracket:
            bracket = bracket.group(0)
            brackets.append(bracket)
            bracket_count = data.count(bracket)
            data = data.replace(bracket, '')
            if bracket_count > 1:
                data = data + (bracket * (bracket_count - 1))
            TextProcessor.extract_all_brackets_with_data(data, brackets)

        return brackets

    @staticmethod
    def extract_regex_pattern_2d(data):
        data = TextProcessor.post_process_brackets(data)
        pattern_cm_decimal = re.search('\d+\.*\d*x{1}\d+\.*\d*', data)
        if pattern_cm_decimal:
            found = pattern_cm_decimal.group(0)
            return found
        else:
            return constant.STR_NOT_PROCESSED

    @staticmethod
    def extract_regex_pattern_3d(data):
        data = TextProcessor.post_process_brackets(data)
        pattern_cm_decimal = re.search('\d+\.*\d*x{1}\d+\.*\d*x{1}\d+\.*\d*', data)
        if pattern_cm_decimal:
            found = pattern_cm_decimal.group(0)
            return found
        else:
            return constant.STR_NOT_PROCESSED

    @staticmethod
    def extract_regex_pattern_1d(data):
        data = data.replace(constant.STR_CM, '')
        pattern_cm_decimal = re.search('\d+\.*\d*', data)
        if pattern_cm_decimal:
            found = pattern_cm_decimal.group(0)
            return found
        else:
            return constant.STR_NOT_PROCESSED

    @staticmethod
    def extract_cm_inside_single_bracket(bracket):
        if 'cm' in bracket and bracket.count('x') == 2:
            bracket = TextProcessor.extract_regex_pattern_3d(bracket)
            return bracket
        if 'cm' in bracket and bracket.count('x') == 1:
            bracket = TextProcessor.extract_regex_pattern_2d(bracket)
            return bracket
        elif 'cm' in bracket and 'x' not in bracket:
            bracket = TextProcessor.extract_regex_pattern_1d(bracket)
            return bracket

    @staticmethod
    def extract_only_valid_dimension(data):
        general_3d = TextProcessor.extract_regex_pattern_3d(data)
        general_2d = TextProcessor.extract_regex_pattern_2d(data)
        general_1d = TextProcessor.extract_regex_pattern_1d(data)
        result = general_3d if general_3d != constant.STR_NOT_PROCESSED else constant.STR_NOT_PROCESSED
        result = result if result != constant.STR_NOT_PROCESSED else general_2d
        result = result if result != constant.STR_NOT_PROCESSED else general_1d
        return result

    @staticmethod
    def string_cleaning(data):
        if pd.isna(data):
            return constant.STR_DIMENSION_UNAVAILABLE
        else:
            data = data.lower()
            data = constant.STR_DIMENSION_UNAVAILABLE if pd.isna(data) else data.replace('\n', ' ').replace('\r', '') \
                .replace('×', 'x').replace(' ', '').replace('approx.', '').replace('–', '-').replace('()', '').strip()
            data = data.replace('x.', 'x0.')  # for such cases (26.7x26.7x.14cm) where number starts with point
            return data

    @staticmethod
    def dimension_transformation(dim):
        if pd.isna(dim):
            return constant.STR_DIMENSION_UNAVAILABLE
        for x in range(0, 10):
            dim = dim.replace(str(x), '#')
        for x in range(5, 1, -1):
            dim = dim.replace('#' * x, '#')

        return TextProcessor.string_cleaning(dim)
