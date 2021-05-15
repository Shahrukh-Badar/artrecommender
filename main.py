from process import ProcessDimension
from data_analysis import DataStatics
if __name__ == "__main__":
    # DataStatics.get_statics()

    process_dimension = ProcessDimension()
    while True:
        print('Please enter object id.')
        object_id = input()
        print('Please enter dimension.')
        dimension = input()
        if dimension:
            process_dimension.does_it_fit(object_id, dimension)
            print('Please enter q to quit or enter to continue.')
            stop = input()
            if stop.strip() == 'q':
                break
