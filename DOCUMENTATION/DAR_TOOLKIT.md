# DAR_TOOLIT User Manual

DAR_TOOLKIT is a command line pure ```python``` script intended to manipulate DAR RAW data, as downloaded from the acquisition unit

## Dependencies
DAR_TOOLKIT depends on the availability of the following packages

```
argparse   pip install argparse
feather    pip install feather-format
obspy      pip install obspy
numpy      pip install numpy
openpyxl   pip install openpyxl
pandas     pip install pandas
pickle     Normally deployed with Python
pyproj     pip install pyproj
simplemkl  pip install simplekml
```

Invoke DAR_TOOLKIT with the following command to get help
```
python .\DAR_TOOLKIT.py -h
usage: DAR_TOOLKIT.py [-h] -f F -c C [-g G] [-t T]

options:
  -h, --help  show this help message and exit
  -f F        Input Filename - DAR RAW file format
  -c C        Configuration file
  -g G        Geometry file
  -t T        Output type [CSV(Z), XLS, FTH, PKL, VU], case insensitive
```

## Get a view of what is inside a given RAW file 

To inspect the content of any downloaded RAW file the user uses the ```-t vu``` mode

```python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t vu```

With this setting, the script provides information on the seismic section of the database.
Data are recorded as a standard PANDAS Dataframe
```
 ------------------------------------------------------------------------------------------------------------------------
        SEISMIC DATABASE
 ------------------------------------------------------------------------------------------------------------------------
                   count                           mean                  min                            25%                            50%                            75%                            max             std
TILT_Z        2001000.0                     -85.405653           -87.946293                     -85.421669                      -85.40293                     -85.375637                     -83.548251        0.191853
TILT_Y        2001000.0                      -4.531642            -6.446528                      -4.604163                      -4.535637                      -4.514363                       -2.00052        0.206968
TILT_X        2001000.0                      -0.271329             -2.44481                      -0.783485                      -0.083169                       0.070938                       2.694292        0.688327
AUX15         2001000.0                    5323.134509               5072.0                         5184.0                         5328.0                         5424.0                         5632.0      153.677525
AUX14         2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX13         2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX12         2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX11         2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX10         2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX9          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX8          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX7          2001000.0                   11800.449775              11723.0                       11800.42                      11803.928                        11804.0                        11813.0        8.609631
AUX6          2001000.0                    1016.208899                448.0                       1012.485                    1017.233999                       1031.482                         1449.0       46.482263
AUX5          2001000.0                     -58.616981               -528.0                        -169.18                     -17.976011                      15.280001                          582.0      148.605959
AUX4          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX3          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX2          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
AUX1          2001000.0                     147.801853               -296.0                     116.501748                     122.821001                     177.972004                          987.0       89.805598
AUX0          2001000.0                            0.0                  0.0                            0.0                            0.0                            0.0                            0.0             0.0
Channel3      2001000.0                    3883.787456       -191431.472195                    2523.985915                    3284.786049                    3887.787928                  228968.200411     3776.257545
Channel2      2001000.0                      -0.000477            -30.42653                      -0.355262                       0.000508                       0.354486                      30.426526        5.704832
Channel1      2001000.0                      -0.001059            -30.42653                      -0.435527                       0.000326                       0.429699                      30.426526        5.982242
Channel0      2001000.0                      -0.002855            -30.42653                      -0.292115                      -0.001378                       0.297934                      30.426526        4.427493
Datetime        2001000  2021-05-26 12:39:45.499499520  2021-05-26 12:23:05  2021-05-26 12:31:25.249750016  2021-05-26 12:39:45.499500032  2021-05-26 12:48:05.749250048  2021-05-26 12:56:25.999000064             NaN
Timestamp     2001000.0                1622032785.4995         1622031785.0               1622032285.24975                1622032785.4995               1622033285.74925                 1622033785.999      577.639089
Channel0_ADC  2001000.0                    -787.179183           -8388608.0                      -80536.25                         -380.0                        82140.5                      8388607.0  1220661.893261
Channel1_ADC  2001000.0                    -291.883879           -8388608.0                      -120075.0                           90.0                      118468.25                      8388607.0  1649306.707028
Channel2_ADC  2001000.0                    -131.564538           -8388608.0                       -97946.0                          140.0                        97732.0                      8388607.0  1572824.691229
Channel3_ADC  2001000.0                  104977.868195           -5174348.0                       68222.75                        88787.0                       105086.0                      6188957.0   102071.359811


 ------------------------------------------------------------------------------------------------------------------------
        SEISMIC ATTRIBUTES
 ------------------------------------------------------------------------------------------------------------------------

                            Battery Voltage at start of recording (millivolts) : 11777
                             Battery Voltage at stop of recording (millivolts) : 11782
                                                           Board Serial Number : 1149
                                              Last Clock Set to GPS time (UTC) : 1622031779
                                              Last Skew Check to GPS time(UTC) : 1621517735
                                                        Last skew value in PPM : nan
                                                    Micro Second Skew Detected : -233
            Minimum Battery Voltage Setting at start of recording (millivolts) : 6500
             Minimum Battery Voltage Setting at stop of recording (millivolts) : 6500
                                      Offset to apply to X tilt (signed short) : -14
                                      Offset to apply to Y tilt (signed short) : 48
                                      Offset to apply to Z tilt (signed short) : 183
                                                         Scale to apply X tilt : 741
                                                         Scale to apply Y tilt : -737
                                                         Scale to apply Z tilt : -839
                          Temperature at start of recording (signed degrees C) : 5440
                           Temperature at stop of recording (signed degrees C) : 5152
                                            X tilt value at start of recording : 1031
                                             X tilt value at stop of recording : 1020
                                            Y tilt value at start of recording : 12
                                             Y tilt value at stop of recording : 171
                                            Z tilt value at start of recording : 127
                                             Z tilt value at stop of recording : 112
                                                                      channels : 0:Inline Geophone, 1: Crossline Geophone, 2: Vertical Geophone, 3 : Hydrophone
                                                                 geophone_gain : 8
                                                               geophone_scalar : 0.000000029017
                                                                geophone_units : mm/s
                                                               hydrophone_gain : 8
                                                             hydrophone_scalar : 0.000000295970
                                                              hydrophone_units : microbar


```

Note that seismic data are not corrected by time skew, while the time drift coefficients, if available, are recorded as attributes. Also, Scalars and gains are stored as attributes.

Channels' physical meaning is defined in the corresponding attribute *channels*

## Save RAW data to FEATHER FORMAT

Feather Format is a quick and compact format suited to store large dataframes.

DAR_TOOLKIT offers the possibility to encode and decode this efficient data exchange format using the ``` -t fth ``` option as shown below.
```
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t fth
```
Note that **two** files are created.
1. a feather format binary data file, which has the same name of the input file, plus the DAR board ID and the extension _.feather_
2. a pickle format that holds the attributes.

   **both files are needed to recover the original data - do not alter the names**
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
la---          26/05/2021    14:57       24093092 03-AUV-1khz-gain32-50THR-3_5m.raw
la---          20/09/2023    10:01      184702786 03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather
la---          20/09/2023    10:01           1336 03-AUV-1khz-gain32-50THR-3_5m.raw.Attributes.1149.pkl
```

**_Best Practice_**

it is advisable to _serialize_ the original _RAW_ file into a _Feather format_ pair of files before running the SEGY creation. Serializing a _raw_ file requires time, while reading _feather format_ is much quicker. Being the SEGY creation procedure prone to tuning, it is better to have a quick input.

Nevertheless, please note that _Feather format_, despite being quick and efficient is **not intended for long-term data storage**, thus it is safe to archive the _raw_ data as well,

## Read Feather Format data 
DAR_TOOLKIT is sensitive to input file extension.
1. :  _.raw_ : activates the serialization procedure of the datafile downloaded from the AUV
2. :  _.feather_ : activates the assimilation of pre-serialized data  saved in _feather format_ as described in the section above.

example
```
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t fth
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -c .\CONFIG.INI -t vu
```
These two commands instruct the script, first, to serialize a _.raw_ data file (as downloaded from the AUV) and save it in _feather format_, and then, to  assimilate the pre-serialised _feather format_ file and show the report

## Convert RAW data to CSV(z), XLS

The script provides the feature of encoding the data in plain textual format and MS Excel format. This feature is intended mainly for small samples to ease data manipulation with custom software (i.e. MatLab).

Conversion format is controlled using either  ``` CSV, CSVZ, XLS ``` keywords as shown below. ``` CSVZ ``` provides a gzipped CSV. 

```
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t csv
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t csvZ
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t XLS
```


It is not advisable to ASCII encode large databases because the resulting output will be huge. Data and attributes are encoded in different files.
Here is a listing of RAW and corresponding ASCII-encoded files of 2 001 000 records.
 
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
la---          26/05/2021    14:57       24093092 03-AUV-1khz-gain32-50THR-3_5m.raw
la---          19/09/2023    14:46           2784 03-AUV-1khz-gain32-50THR-3_5m.raw.1149_Attributes.csv
la---          19/09/2023    14:35      615560542 03-AUV-1khz-gain32-50THR-3_5m.raw.1149.csv
-a---          19/09/2023    14:46      190215807 03-AUV-1khz-gain32-50THR-3_5m.raw.1149.csv.gz
```
Note that DAR serial number is added to the filename to ease data management when several vehicles are involved.

### Datetime range selection 
Conversion towards textual/xls formats enables the possibility to select a specific datetime range. This is mandatory when the output is XLS beacuse of the limited capabilities of EXCEL to handle large amounts of data.

The option is activated using the option ``` -i ```
The user must provide initial and final datetime in the strict format described hereafter

```
-i "<initial datatime> to <finale datetime>"
where datatime is YYYY-MM-DD hh:mm:ss, the argument must be enclosed in quotation marks
example : -i "2021-05-26 12:40:00 to 2021-05-26 12:40:10"

the whole command line to get XLS output is something like this: 

python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -c .\CONFIG.INI -t xls -i "2021-05-26 12:40:00 to 2021-05-26 12:40:10"

```
the  ``` -i ``` activates a specific report. The newly created filename has the datetime range appended in the name. Attributes file is also dumped as plain text
```


                       Source filename : .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather
                         Output format : xls

                                      Start                           End
------------------------- ------------------------------ ------------------------------
            Data Datetime            2021-05-26 12:23:05  2021-05-26 12:56:25.999000064
           Data Timestamp              1622031785.000000              1622033785.999000
          Target Datetime            2021-05-26 12:40:00            2021-05-26 12:40:10
         Target Timestamp              1622025600.000000              1622025610.000000
           Target indices                        1015000                        1025000
------------------------- ------------------------------ ------------------------------
             Total Record 10000
------------------------- ------------------------------ ------------------------------
                  Output Data filename : .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather.1149_2021-05-26_12-40-00-to-2021-05-26_12-40-10.xlsx
            Output Attributes filename : .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather.1149_Attributes.csv

 
```
Note that  ``` -i ``` option is useless with other output formats than ``` CSV, CSVZ, XLS ```.

# STREAM_SCOPE

This script is intended to show the signal(s) saved in a Feather-Format archive.

Note that this script requires, on top of other dependencies, ``` matplotlib ```

Invoke STRAMSCOPE with the following command to get help
```
python .\STREAM_SCOPE.py -h
usage: STREAM_SCOPE.py [-h] -f F [-ch CH] -c C [-i I] [-m M] [-g G]

options:
  -h, --help      show this help message and exit
  -f F            Input Filename - Feather format
  -ch CH          Channel, as defined in Attributes, default is 3, Hydrophone
  -c C            Configuration file
  -i I            time interval, details in DAR_TOOLKIT.md
  -m M            working mode : plot (default), info
  -g G            Geometry file
  -colors COLORS  colors of chart elements, details in DAR_TOOLKIT.md, section STREAM_SCOPE
```

Option  ``` -m info ``` prevents the chart and provides extensive information on data. This option may work in conjunction with ``` -i ```, in this case only data within the time windows will be analyzed.

The following picture shows the chart created using the converted RAW file stored in /DEMODATA of this repository
```
 python .\STREAM_SCOPE.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -c .\CONFIG.ini -m plot
```
![sketch](/RES/IMG_09.png)

### Time slice

Option  ``` -i ``` defines a time window. Only data within the time window will be shown.

The input format and details are described in a previous section of this document: _Datetime range selection

### Geometry

Option ``` -g ``` enables Geometry processing.

with this option enabled, the provided _Geometry_ file is processed and its information is shown. Details about the _Geometry_ files are in the document SEGY_CREATION_Guide.md
```
python .\STREAM_SCOPE.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -c .\CONFIG.ini -m plot -g .\DEMODATA\03-50-05.gtd2
```
The following pictures show, at increasing scale the output using the ``` -g ``` option.

![sketch](/RES/IMG_10a.png)
![sketch](/RES/IMG_10b.png)
![sketch](/RES/IMG_10c.png)


The actual data chunk that will be inserted in the SEGY is highlighted (i.e. middle picture where the selected data chunk is colored in orange).

The vertical lines point to the actual shooting time (```SHOT EPOCH```) and the _expected first break_. In the zoomed view ```SHOT EPOCH``` is red and the  _expected first break_ is blue.

The best practice is to check the consistency of the  _expected first break_ with the actual signal. If there is no accurate matching then the source's and/or the receiver's position is biased by some error. Deepening on this is in the  document SEGY_CREATION_Guide.md


### Colors

Colors codes are controlled using the option ``` -colors <list of color names> ```, which is a list of Matplotlib color names, separated by semicolons end enclosed between quotation marks, as in the example below.

```
python .\STREAM_SCOPE.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -c .\CONFIG.ini -colors "tab:purple;tab:blue;tab:red;tab:olive" -m plot -g .\DEMODATA\03-50-05.gtd2 

```
A list of suitable color names is available here https://matplotlib.org/stable/gallery/color/named_colors.html



# TIME_SHIFT

This script enables the user to manipulate the original data by adjusting the ```Timestamp```

<table><tr><td>This script creates a copy of the original data file and then replaces it with the time-shifted version.</td></tr></table>

Invoke TIME_SHIFT with the following command to get help
```
python .\TIME_SHIFT.py -h

  -h, --help    show this help message and exit
  -f F          Input Filename - Feather format
  -t T          time shift in milliseconds
  -quiet QUIET  specify quiet YES not be asked for file substitution

```
The script is designed to prevent the user from replacing the original data, by default running in _verbose_ mode.
```
 python .\TIME_SHIFT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -t -12304000

                        Input filename : .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather
                            Time shift : -12304000 millis [-1 day, 20:34:56]

        WARNING
        -------
        The orignal file will be replaced!
        A copy of it will be created as :.\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather.ORIGINAL.feather

        >> Type "YES" if agree

```
If the user denies the permission to replace the original file (typing anything but YES or just pressing ENTER), the script computes the actual _time-shift_ to be applied and shows it to the user by displaying the first 4 rows of the database but doesn't overwrite the original file.
```
Example of the correction to be applied
 -----------------------------------

      1622031785.000  --> 1622019481.000        2021-05-26 14:23:05.000000   -->   2021-05-26 10:58:01.000000
      1622031785.001  --> 1622019481.001        2021-05-26 14:23:05.001000   -->   2021-05-26 10:58:01.001000
      1622031785.002  --> 1622019481.002        2021-05-26 14:23:05.002000   -->   2021-05-26 10:58:01.002000
      1622031785.003  --> 1622019481.003        2021-05-26 14:23:05.003000   -->   2021-05-26 10:58:01.003000

 No time shift correction has been applied because the user denied permission to overwrite the input file
```


# GTDtoKML

This script interprets the GT DATUM file ver 2 (aka the **GEOMETRY** file) and creates a corresponding geographical representation of shots and receivers using the Google Earth engine and visualization app.

Invoke GTDtoKML with the following command to get help
```
python  .\GTDtoKML.py -h

usage: GTDtoKML.py [-h] -fi FI [-d D]

GDT to KML - Shot map created from Seismic Geometry

options:
  -h, --help  show this help message and exit
  -fi FI      GDT file (input)
  -d D        if -d TRUE, it returns the list of shot points with planar coordinates (optional)

```


optionally the script returns a list of shot locations 

```
          Input file : .\DEMODATA\03-50-05.gtd2


          Projection : utm
          Input file : 30
               Shots : 22
          Ouput file : .\DEMODATA\03-50-05.gtd2.source.kml

RECEIVER 001  LOCATION
      SHOT   RECEIVER EASTING      NORTHING     LONGITUDE        LATITUDE
      001        001  539356.31    5303810.03   -2.473557525035  47.886415489308
      002        002  539356.31    5303810.03   -2.473557525035  47.886415489308
      003        003  539356.31    5303810.03   -2.473557525035  47.886415489308
      004        004  539356.31    5303810.03   -2.473557525035  47.886415489308
      005        005  539356.31    5303810.03   -2.473557525035  47.886415489308
      006        006  539356.31    5303810.03   -2.473557525035  47.886415489308
      007        007  539356.31    5303810.03   -2.473557525035  47.886415489308
      008        008  539356.31    5303810.03   -2.473557525035  47.886415489308
      009        009  539356.31    5303810.03   -2.473557525035  47.886415489308
      010        010  539356.31    5303810.03   -2.473557525035  47.886415489308
      011        011  539356.31    5303810.03   -2.473557525035  47.886415489308
      012        012  539356.31    5303810.03   -2.473557525035  47.886415489308
      013        013  539356.31    5303810.03   -2.473557525035  47.886415489308
      014        014  539356.31    5303810.03   -2.473557525035  47.886415489308
      015        015  539356.31    5303810.03   -2.473557525035  47.886415489308
      016        016  539356.31    5303810.03   -2.473557525035  47.886415489308
      017        017  539356.31    5303810.03   -2.473557525035  47.886415489308
      018        018  539356.31    5303810.03   -2.473557525035  47.886415489308
      019        019  539356.31    5303810.03   -2.473557525035  47.886415489308
      021        021  539356.31    5303810.03   -2.473557525035  47.886415489308
      022        022  539356.31    5303810.03   -2.473557525035  47.886415489308
      023        023  539356.31    5303810.03   -2.473557525035  47.886415489308

```

the standard output is a pair of files placed in the same folder of the input data 
```
la---          21/09/2023    10:05           3127 03-50-05.gtd2
la---          26/09/2023    10:39           5761 03-50-05.gtd2.receiver.kml
la---          26/09/2023    10:39           5753 03-50-05.gtd2.source.kml
```
 To view the ```kml``` files please refer to Google Earth documentation. (https://www.google.com/intl/it/earth/about/versions/#earth-pro)

![sketch](/RES/IMG_20.png)
the picture above shows and example of both kml 

