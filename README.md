
# geoweather
    GEOWEATHER extracts raster info over geometries and sends alerts through slack API
```
    Server: ---
    Status: Development
```

### Technologies:
  * Python 3.8.*
  * [Numpy] 1.25.2
  * [Pandas] 2.0.3
  * [arm_pyart] 1.15.2
  * [boto3]


### settings.py:
The *settings.py* contains constant information, directories, DB queries, colorbars, etc.

```sh
$ more /home/rbatistavilela/work/codes/geoweather/geoweather/settings.py
``` 
### config.json:
The .json files in geoweather subfolder are configuration files you must provide as input parameter (--configure paramenter for service.py). These files have information about the input file like path, variables; and the output like path and the file content.

### service.py:
Is the executable that receives the input parameters and send it to controller.py

```sh
$ /home/rbatistavilela/work/codes/geoweather/service.py --help

``` 
#### Execution:
You can set up a date and time to run the code. This means that the code can reprocess observations in the past. If "start" and "end" parameters are the same you'll run only that specific hour (for exemple for operational purposes), otherwise you'll have "n" hourly files, one for each hour in your input interval.

```sh
$ ./service.py --configure geoweather/product.json --filetime <YYYYmmddHHMM>

```

### controller.py:
This module is responsible for receiving the input parameters from service.py and executing the function run_process that manages every step of code execution.

### library/datahub.py
Internal functions responsible for opening the input data.


### Outputs
The geoweather code generates fields in netdf format

### process running on CRONTAB
Not operational

        
[Numpy]: <https://anaconda.org/anaconda/numpy>
[Pandas]: <https://anaconda.org/anaconda/pandas>
