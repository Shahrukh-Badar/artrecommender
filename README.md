# _MET Museum art recommender_
This program will recommend you the art based on the input dimensions.

## _About data and assumptions_
#### Dimension data summary:
- Total number of records are `475774`
- Total number of null dimensions are `75403`
- Total number of unique dimension patterns are `38578`
- Total number of not processed records are `1498` among which `1497` records does not have dimensions in cm.
#### Dimension patters:
- Top 3 patterns occurred around more than `80000` times` (50000+20000+10000)`
- There are around `28000` patterns which are unique and exists only single time.
- Data Statics can be seen from the function `get_statics()` inside `data_analysis.py`

#### Extraction and Assumptions
* It will only extract the dimensions which are in cm.
* Dimension can either be 1D, 2D or 3D.
* Dimension will be extracted in this pattern
    * Example of 1D
        * `diam.11/16in.(1.7cm) -> output : 1.7`
        *` beforeconservation,greatestheight13.4cm(weft);greatestwidth24cm(warp) -> output : 13.47`
    * Example of 2D
        * `11x9in.(27.9x22.9cm) -> output : 27.9x22.9`
    * Example of 3D 
        * `23/4x31/2x23/4in.(7x8.9x7cm) -> output : 7x8.8x7 `
* In case of multiple brackets having single number inside with cm, it will extract it like
    * `h.69/16in.(16.7cm);diam.3in.(7.6cm)  -> output : 16.7x7.6`
    * `backplate:diam.27/8in.(7.3cm)ringpull:diam.17/8in.(4.8cm)  -> output : 7.3x4.8`
        * This above approach does not consider the order of dimensions.
            * For example: it will not check height comes first or diameter comes in second, because this h. for height is not constant and so on.
            * It will extract it till 3rd bracket and discard the data which have 4 brackets because 4D does not make sense.
* In case of such data where cm is outside brackets
    * `l.15.2cm(6.2in.)  -> output : 5.2`
* In case of no brackets, for example
    * `l.17xw.31/2inches43.2x8.9cm -> output : 43.2x8.9`
* In cases where multiple pairs of dimension are available, it will only consider the first, either its 1D, 2D or 3D.
    * `image(left):50.8x34.2cm(20x137/16in.)sheet(left):54.7x38.2cm(219/16x151/16in.)image(center):50.8x75.4cm(20x2911/16in.)sheet(center):54.7x79.3cm(219/16x311/4in.)image(right):50.8x34cm(20x133/8in.)sheet(right):54.7x38.2cm(219/16x151/16in.)  -> output : 50.8x34.2`
    * Mostly object type images, painting and drawing have such data.
* In the end if not any above rules match, it will perform dirty guess, which can be disable by config. But mostly data can be processed with above rules.
    * `h.10-3/4in.sq.xw.1-1/4in.thick(27.3cm.sq.x3.2cm.thick)  -> dirty guess 27.3`
    *` h.20xw.24xd.1inches(50.8x61.0xd.2.5cm)  -> dirty guess 50.8x61.0`
    * `h.113/4xw.211/2xl.371/4in.(29.8x211/2x94.6cm)  -> dirty guess 29.8x211`
* It will not process such data, for example
    * `42ft.x18in.(504in.x45.7cm)` where data is mixture of cm and inches.
    * `h.13in.(cm);w.231/4in.(cm)` when cm does not have any numerical value (only 1 record have this data)
* Some data have dimensions like below which will be marked as not processed
    * dimension unavailable
    * dimension not recorded
            
## _Extraction Flow:_
* Load the CSV dataset only Object ID and dimension columns
* Clean the Dimensions column
    * replace null with dimensionsunavailable
    * lowercase the data
    * remove spaces and special characters
* Extract Dimensions
    * process brackets (remove unwanted brackets)
        * that does not have `numeric` data inside 
        * that does not contains `cm`
    * extracts all brackets along with data recursively
    * based on conditions/rules extract dimensions
        * by using separate regex expressions for 1D, 2D and 3D.
    * at the end if any rule does not match
        * perform` dirty guess`
    * even its not matched
        * return `not_processed`
* Index it on Object Id
* Save it as pickle file
    * used pickle file because it will save exact representation and reduce the loading time as compared to csv, and does not need to process data after loading.
* Once saved it will again loaded in to memory for future seaches
    
 
## _Unit tests:_
* Two unit test are exists, to test unit tests a small chuck of data is extracted from original data
    * first to compare extracted dimension with the chunk of original data
        * where expected output is hard coded in test data
    * second is to check `does_it_fit` method is extracting valid data against the object id
      
## _Implementation:_
* Entry point for the application is main.py
    * takes object id and dimension as input
        * object id can be integer
        * dimension can be 1D, 2D and 3D, some of the valid inputs are
            * 17.5 | 17
            * 17.5x13.0 | 17x13.0 | 17x13 
            * 1x1x1 | 9.0x9.0x9.0
    * call `does_it_fit` method to get the result
        * accept object id and dimension as input paramenter
        * return True|False as output
        * this method has an option to match smartly, where it will not consider the placement in dimentions
            * for example, for dimension 1x2x3
                * if this feature is enable it will match any order of this dimension
                    * input of 1x2x3 will successfully match with
                        * 1x3x2 | 3x2x1 | 2x3x1
            
## _How to run the Converter:_

### _Local_
* Install `python 3.9`

* Create virtual environment

* Install packages from requirement.txt  `pip install -r requirements.txt ` 

* Make sure file paths is properly configured in `constant.py` 

* Run python script `main.py` 

* For test, run python script `main_test.py`
### _Docker_

* Locate `Dockerfile` 

* Make sure requirement.txt exists else generate it by `pip freeze > requirements.txt`

* Build docker image: `docker build -t artrecommenderdocker .`

* Run docker image: `docker  run -it artrecommenderdocker /bin/bash`
   

