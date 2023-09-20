# DAR_TOOLIT User Manual

DAR_TOOLKIT is a command line pure python script intended to manipulate DAR RAW data, as donwloaded from the acquisition unit

## Dependedncies
DAR_TOOLKIT depends on the availability of the following packages

```
argparse   pip install argparse
feather    pip install feather-format
obspy      pip install obspy
pandas     pip install pandas
pickle     Noramlly deployed with Python
pyproj     pip install pyproj
simplemkl  pip install simplekml
```

Invoke DAR_TOOLKIT wqith the following command to get help
```
python .\DAR_TOOLKIT.py -h
usage: DAR_TOOLKIT.py [-h] -f F -c C [-g G] [-t T]

options:
  -h, --help  show this help message and exit
  -f F        Input Filename - DAR RAW fileformat
  -c C        Configuration file
  -g G        Geometry file
  -t T        Output type [CSV(Z), FTH, PKL, VU]
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

## Convert RAW data to CSV(z)

The script provides the feature of encoding the data in plain textual format. This feature is intended mainly for small samples to ease data manipulation with custom software (i.e. MatLab).

```
python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw -c .\CONFIG.INI -t csv
```


It is not advisable to ASCII encode large databases because the resulting output will be huge. Data and attributes are encoded in different files.
Here is a listing of RAW and corresponding ASCII-encoded files of 2 001 000 records.
By using   ```-t csvz``` the ASCII-encoded data is gzipped to save disk.
 
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
la---          26/05/2021    14:57       24093092 03-AUV-1khz-gain32-50THR-3_5m.raw
la---          19/09/2023    14:46           2784 03-AUV-1khz-gain32-50THR-3_5m.raw.1149_Attributes.csv
la---          19/09/2023    14:35      615560542 03-AUV-1khz-gain32-50THR-3_5m.raw.1149.csv
-a---          19/09/2023    14:46      190215807 03-AUV-1khz-gain32-50THR-3_5m.raw.1149.csv.gz
```
Note that DAR serial number is adde to the filename to ease data management when several vehicles are involved.

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

## Read Feather Foramt data 
DAR_TOOLKIT is sensitive to input file extension.
1. _.raw_ : activates the serialization procedure of the datafile downloaded from the AUV
2. _.feather_ : activates the assimilation of pre-serialized data  saved in _feather format_ as described in the section above.
3. 

