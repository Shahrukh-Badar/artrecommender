from text_processor import *
import constant as constant


class Extractor:
    @staticmethod
    def extract_dimension_in_cm(dim):
        result = constant.STR_NOT_PROCESSED
        if dim.lower() == constant.STR_DIMENSION_UNAVAILABLE:
            return result
        if not constant.STR_CM in dim:
            return result

        cm_str = TextProcessor.process_brackets(dim)
        bracket_data = TextProcessor.extract_all_brackets_with_data(cm_str, [])
        bracket_count = len(bracket_data)

        if bracket_count == 0:  # 'l.17xw.31/2inches43.2x8.9cm'
            if constant.STR_INCHES in cm_str:
                cm_data = [x for x in cm_str.split(constant.STR_INCHES) if constant.STR_CM in x]
                if cm_data:
                    found = TextProcessor.extract_only_valid_dimension(cm_data[0])
                    result = found
            else:
                result = TextProcessor.extract_only_valid_dimension(cm_str)
        elif bracket_count >= 1:
            if bracket_count in [1, 2, 3] and all(['x' not in x for x in bracket_data]) \
                    and all(
                TextProcessor.extract_regex_pattern_1d(x) != constant.STR_NOT_PROCESSED for x in bracket_data):
                cm_data = 'x'.join(TextProcessor.extract_regex_pattern_1d(x) for x in bracket_data)
                result = cm_data
            else:
                cm_data = [TextProcessor.extract_cm_inside_single_bracket(x) for x in bracket_data if
                           constant.STR_CM in x]
                result = cm_data[
                    0] if cm_data else constant.STR_NOT_PROCESSED  # get only first if multiple pairs exists

        if result == constant.STR_NOT_PROCESSED:
            if constant.CNF_ENABLE_DIRTY_GUESS:  # mostly for more than 3 brackets select only first and ambiguios data 'diam:31/4in.(8.3cm)mount:201/2x15x7/8in.(52.1x38.1x2.2cm)'
                result = TextProcessor.extract_only_valid_dimension(
                    bracket_data[0] if bracket_data else cm_str)  # dirty guess
            if result == constant.STR_NOT_PROCESSED:
                s = "" # breakpoint to debug if dimension is still not processed
        return result
