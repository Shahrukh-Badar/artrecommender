from text_processor import *


class Extractor:
    @staticmethod
    def extract_dimension_in_cm(dim):
        result = 'not_processed'
        if dim.lower() == 'dimensionsunavailable':
            return result
        if not 'cm' in dim:
            return result



        #dim = 'h.101/2xw.101/2xd.51/2in.(26.7x26.7x.14cm)'
        if 'overall(withoutloop):37x773/4in.(94x197.5cm)overall(withloop):37x801/4in.(94x203.8cm)' in dim:
            sd = 22
        cm_str_orig = dim
        cm_str = TextProcessor.process_brackets(dim)
        bracket_data = TextProcessor.extract_all_brackets_with_data(cm_str, [])
        bracket_count = len(bracket_data)  # extract_bracket_count(cm_str)

        if bracket_count == 0:
            # found = 'not_processed'
            if 'inches' in cm_str:
                cm_data = [x for x in cm_str.split('inches') if 'cm' in x]
                if cm_data:
                    found = TextProcessor.extract_only_valid_dimension(cm_data[0])
                    result = found #'l.17xw.31/2inches43.2x8.9cm'
            else:
                result = TextProcessor.extract_only_valid_dimension(cm_str)
        elif bracket_count >= 1:
            if bracket_count in [1, 2, 3] and all(['x' not in x for x in bracket_data]) \
                    and all(TextProcessor.extract_regex_pattern_1d(x) != 'not_processed' for x in bracket_data):
                cm_data = 'x'.join(TextProcessor.extract_regex_pattern_1d(x) for x in bracket_data)
                result = cm_data
            else:
                cm_data = [TextProcessor.extract_cm_inside_single_bracket(x) for x in bracket_data if 'cm' in x]
                result = cm_data[0] if cm_data else 'not_processed'  # get only first if multiple pairs exists

        if result == 'not_processed':  # mostly for more than 3 brackets select only first and ambiguios data 'diam:31/4in.(8.3cm)mount:201/2x15x7/8in.(52.1x38.1x2.2cm)'
            result = TextProcessor.extract_only_valid_dimension(bracket_data[0] if bracket_data else cm_str) #dirty guess
            if result == 'not_processed':
                s = ""
        return result
