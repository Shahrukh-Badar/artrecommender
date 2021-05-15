from process import ProcessDimension
from data_analysis import DataStatics
import constant as constant

if __name__ == "__main__":
    if constant.CNF_ENABLE_DATA_STATICS:
        DataStatics.get_statics()

    process_dimension = ProcessDimension()
    while True:
        print('#' * 30)
        print(constant.MSG_OBJECT_ID_INPUT)
        object_id = input()  # sample object id: 200000
        print(constant.MSG_DIMENSION_INPUT)
        dimension = input()  # sample dimension: 22.9x11.7
        if dimension:
            process_dimension.does_it_fit(object_id, dimension)
            print(constant.MSG_APP_CONTINUE)
            stop = input()
            if stop.strip() == constant.BREAK_POINT:
                break
