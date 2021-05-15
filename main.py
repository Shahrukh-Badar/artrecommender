from process import ProcessDimension

if __name__ == "__main__":
    process_dimension = ProcessDimension()
    while True:
        print('Please enter object id.')
        object_id = input()  # 1000
        print('Please enter dimension.')
        dimension = input()  # '135.6x186.4x46.7'
        if dimension:
            process_dimension.does_it_fit(object_id, dimension)
            print('Please enter q to quit or enter to continue.')
            stop = input()
            if stop.strip() == 'q':
                break
