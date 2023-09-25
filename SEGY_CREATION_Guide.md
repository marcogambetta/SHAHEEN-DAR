# SEGY CREATION GUIDE

This document provides the needed detail to create a seismic SEGY merging DAR seismic recordings with navigation and shot data.

## Foreword
**SEGY** is an international standard for seismic data exchange and storage, designed to host multi-dimensional data with geographical and time reference.
Bare sensor recordings are nearly useless to the seismic industry because the description of elastic wave propagation requires accurate spatial and time localization.

a SEGY is, generally speaking, a collection of _seismic traces_. Each _seismic trace_ can be conceptualized as an _object_ provided with different data types. Some of those data are _signals_ as recorded by sensors, some others are values describing features such as the receive position, the sampling frequency, the source position, and the shooting time.
A comprehensive SGY description is provided in section nnn of this document.

## Simplified SEGY creation procedure

![sketch](/RES/IMG_05.png)

Data needed to create a SEGY comes from **three different sources** : 
1. sensor data
2. AUV positioning data
3. source (airgun) positioning data

Every single source must have the same _**time axis**_. The _time axis_ **must be carefully synchronized** among the different devices: DAR, Navigation and localization system, guns' controller

Synchronization must have higher accuracy than the actual fastest sampling rate. Normally seismic sensors (Hydrophones and Geophones) are sampled at 1 kHz. This means that the _time axis must be syncronized_ with accuracy not less than half a millisecond. Marginally an accuracy equal to the fastest sampling rate can be accepted.

## Sensor Data
Sensor data are recorded by DAR and organized in a database using DAR_TOOLIK. The collected data is a time stream: samples are collected in sequence, one after the other, from the start to the end of the recording.

![sketch](/RES/IMG_06.png)

The figure above shows an excerpt of one channel (i.e. the hydrophone) of the data stream. In this excerpt, some subsequent shots are recorded. At the drawing's scale, the shots appear as spikes. Each of these shots is the data we want in our SEGY, aka the SEGY will be made of as many traces as the recorded shots.

The task is to extract all the _shots_ from the stream

![sketch](/RES/IMG_07.png)

The figure above shows one (random) shot taken from the ensemble shown before. Now, with an enlarged horizontal scale, the burst of energy recorded by the system appears as a dumped wave.
The horizontal axis is the time axis, unit is the second. This is the excerpt of the signal that will form the SEGY trace.

# GEOMETRY
Geometry information is organized in a textual file, designed and simplified after the SPS format, namely _GT DATUM_.

Geometry information is composed of:
1. AUV positioning data, that is the three-dimensional geographical position of the receiver.
2. SOURCE positioning data, that is the three-dimensional geographical position of the source, the airgun, or other device that creates the pressure wave. In the case of a cluster source, this is the geometrical center of the cluster.

** Note**
_Three-dimensional geographical position_  is the geographical position (Longitude, Latitude) projected onto a UTM kilometric grid  [Easting, Northing] including depth data, computed from mean sea level. No tidal correction is applied at this stage.

 ## GT DATUM
 A working example of  _GT DATUM_ is in folder DEMODATA of this repository.

 here follows an excerpt

```
#RECORD CODE                0   1
#LINE NAME                  2   10
#SPNB                      11   15
#SHOT X [EASTING]          16   25
#SHOT Y [NORTHING]         26   37
#SHOT Z [DEPTH]            38   42
#RECEIVER NUMBER           43   47
#RECEIVER X [EASTING]      48   57
#RECEIVER Y [NORTHING]     58   69
#RECEIVER Z [DEPTH]        70   73
#WATER BOTTOM              75   79
#SHOT EPOCH                80   94
#GUN PRESSURE              95   99
#0       1         2         3         4         5         6         7         8         9
#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
H18 PROJECTION TYPE             utm
H19 PROJECTION ZONE             30
H999BOARD SERIAL NUMBER         1146
R        3 001 539356.31 5303810.03  3.0  1000 539405.61 5303788.26  5.0  48.0 1622033224.801 2000
R        3 002 539356.31 5303810.03  3.0  1000 539401.21 5303794.97  5.0  48.0 1622033232.800 2000
R        3 003 539356.31 5303810.03  3.0  1000 539396.80 5303801.68  5.0  48.0 1622033240.801 2000
R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000
R        3 005 539356.31 5303810.03  3.0  1000 539387.98 5303815.09  5.0  48.0 1622033256.802 2000
R        3 006 539356.31 5303810.03  3.0  1000 539383.58 5303821.79  5.0  48.0 1622033264.802 2000
```
The datum file has a very strict syntax and its encoding is based on position and the user must comply with that.   

The datum file is composed of a header, immutable, that specifies the keyword and its range of positions in the record.
The count of char is zero-based, this means
that the first char is chara number 0, and corresponds to the ```RECORD CODE```
Each keyword shows two digits: these are the position of the first and the last char that can be used to store the actual value in a record (line).


By using the immutable header, the class ```GDT``` interprets the file: 
i.e.:

```SHOT Y [NORTHING]``` is stored from char ```26``` to char ```37```, it value, in the case, is ```5303810.03```

```
#SHOT Y [NORTHING]         26   37
#0       1         2         3         4         5         6         7         8         9
#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789

R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000
```

```#SHOT EPOCH``` is stored from char ```80``` to char ```94```, its value, in the case, is ```1622033248.801```, note that ```SHOT EPOCH``` is a float with three decimals and its unit is seconds.

If the actual value is shorter than the allotted chars, left-align the value and fill the gap with spaces.

```
#SHOT EPOCH                80   94
#0       1         2         3         4         5         6         7         8         9
#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789

R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000
```

 # SEGY CREATION 
 SEGY creation is managed bt **DAR_TOOLIK** using the following command


```
  python .\DAR_TOOLKIT.py -f .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather -t SEGY -g .\DEMODATA\03-50-05.gtd2 -c .\CONFIG.INI
```
the output is a SEGY file and a log on the console, hereafter an example


```

                       Source filename : .\DEMODATA\03-AUV-1khz-gain32-50THR-3_5m.raw.1149.feather
                         Output format : SEGY

|-----|--------|----------------------------|----------------------------|----------------------------|
|  #  |  SPNB  |       START DATETIME       |        END DATETIME        |       SHOT DATETIME        |
|-----|--------|----------------------------|----------------------------|----------------------------|
|  0  |   1    |2021-05-26T12:47:01.660000Z |2021-05-26T12:47:06.659000Z |2021-05-26T12:47:03.660000Z |
|  1  |   2    |2021-05-26T12:47:09.655000Z |2021-05-26T12:47:14.654000Z |2021-05-26T12:47:11.655000Z |
|  2  |   3    |2021-05-26T12:47:17.651000Z |2021-05-26T12:47:22.650000Z |2021-05-26T12:47:19.651000Z |
|  3  |   4    |2021-05-26T12:47:25.648000Z |2021-05-26T12:47:30.647000Z |2021-05-26T12:47:27.648000Z |
|  4  |   5    |2021-05-26T12:47:33.646000Z |2021-05-26T12:47:38.645000Z |2021-05-26T12:47:35.646000Z |
|  5  |   6    |2021-05-26T12:47:41.645000Z |2021-05-26T12:47:46.644000Z |2021-05-26T12:47:43.645000Z |
|  6  |   7    |2021-05-26T12:47:49.644000Z |2021-05-26T12:47:54.643000Z |2021-05-26T12:47:51.644000Z |
|  7  |   8    |2021-05-26T12:47:57.645000Z |2021-05-26T12:48:02.644000Z |2021-05-26T12:47:59.645000Z |
|  8  |   9    |2021-05-26T12:48:05.645000Z |2021-05-26T12:48:10.644000Z |2021-05-26T12:48:07.645000Z |
|  9  |   10   |2021-05-26T12:48:13.647000Z |2021-05-26T12:48:18.646000Z |2021-05-26T12:48:15.647000Z |
| 10  |   11   |2021-05-26T12:48:21.650000Z |2021-05-26T12:48:26.649000Z |2021-05-26T12:48:23.650000Z |
| 11  |   12   |2021-05-26T12:48:29.654000Z |2021-05-26T12:48:34.653000Z |2021-05-26T12:48:31.654000Z |
| 12  |   13   |2021-05-26T12:48:37.657000Z |2021-05-26T12:48:42.656000Z |2021-05-26T12:48:39.657000Z |
| 13  |   14   |2021-05-26T12:48:45.661000Z |2021-05-26T12:48:50.660000Z |2021-05-26T12:48:47.661000Z |
| 14  |   15   |2021-05-26T12:48:53.664000Z |2021-05-26T12:48:58.663000Z |2021-05-26T12:48:55.664000Z |
| 15  |   16   |2021-05-26T12:49:01.669000Z |2021-05-26T12:49:06.668000Z |2021-05-26T12:49:03.669000Z |
| 16  |   17   |2021-05-26T12:49:09.672000Z |2021-05-26T12:49:14.671000Z |2021-05-26T12:49:11.672000Z |
| 17  |   18   |2021-05-26T12:49:17.676000Z |2021-05-26T12:49:22.675000Z |2021-05-26T12:49:19.676000Z |
| 18  |   19   |2021-05-26T12:49:25.681000Z |2021-05-26T12:49:30.680000Z |2021-05-26T12:49:27.681000Z |
| 19  |   10   |2021-05-26T12:49:33.685000Z |2021-05-26T12:49:38.684000Z |2021-05-26T12:49:35.685000Z |
| 20  |   21   |2021-05-26T12:49:41.690000Z |2021-05-26T12:49:46.689000Z |2021-05-26T12:49:43.690000Z |
| 21  |   22   |2021-05-26T12:49:49.695000Z |2021-05-26T12:49:54.694000Z |2021-05-26T12:49:51.695000Z |
| 22  |   23   |2021-05-26T12:49:57.701000Z |2021-05-26T12:50:02.700000Z |2021-05-26T12:49:59.701000Z |
|-----|--------|----------------------------|----------------------------|----------------------------|

              Samples before shot time:    2000
                         Trace samples:    5000
                                Output:1149_2021-05-26T12-47-03.660000Z_2021-05-26T12-49-59.701000Z.SGY
```

Everything is plain and easy pending the correct _configuration_ and the correct _geometry_ file.

## Configuration file [SEGY Creation parameters]

The following are configuration file parameters to be set to create a SEGY.
```
SEGY_samples_before_event =200
SEGY_trace_samples = 1500
Sound_Speed_in_water = 1480
ShotEpochShift = -1.178
```

![sketch](/RES/IMG_12.png)

The picture shows in orange the actual trace that will be inserted in the SEGY. ```
SEGY_samples_before_event =200``` is the amount of samples taken **before** the _envent_

 _envent_ is the first break, that is the point in time when the emitted wave starts being recorded. This point in time is highlighted in the picture above with the vertical  _blue_ line right on the left of the burt of energy (high amplitudes)

 ```SEGY_trace_samples = 1500``` sets the number of samples of the actual trace that will be inserted in the SEGY. This number of samples is counted from the _beginning of the trace_ (leftmost point is the overlapped orange signal in the picture above), and not from the _first break_.




