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

Synchronization must have higher accuracy than the actual fastest sampling rate. Normally seismic sensors (Hydrophones and Geophones) are sampled at 1 kHz. this means that the _time axis must be syncronized_ with accuracy not less than half a millisecond. Marginally an accuracy equal to the fastest sampling rate can be accepted.

## Sensor Data
Sensor data are recorded by DAR and organized in a database using DAR_TOOLIK. The collected data is a time stream: samples are collected in sequence, one after the other, from the start to the end of the recording.

![sketch](/RES/IMG_06.png)

The figure above shows an excerpt of one channel (i.e. the hydrophone) of the data stream. In this excerpt, some subsequent shots are recorded. At the drawing's scale, the shots appear as spikes. Each of these shots is the data we want in our SEGY, aka the SEGY will be made of as many traces as the recorded shots.

The task is to extract all the _shots_ from the stream

![sketch](/RES/IMG_07.png)

The figure above shows one (random) shot taken from the ensemble shown before. Now, with an enlarged horizontal scale, the burst of energy recorded by the system appears as a dumped wave.
The horizontal axis is the time axis, unit is the second.

Let's assume that the energy was released at a given time, for the sake of the discussion, say equal to 36.000 seconds. 
The burst of energy starts at 39.651 seconds; this exact time is called _first break_

The difference between the time when energy was released and the _first break_, that is the time when the energy is recorded by the recording system on the AUV, is 3.651 seconds. 

This means the distance between the source and the receiver is 3.651 s times 1500 m/s = 5.476,5 m, assuming 1500 m/s is a typical value for sound speed in seawater.

We need to know when the _first break_ occurs to have a starting point to extract the data from the stream. 

Using **navigation and localization data** together with **shot data** it is possible to compute the 3D Euclidean distance between the source and the receive. Knowing the distance and the sound speed in seawater the travel time can be computed. Adding the travel time to the actual shooting time the _first break_ is known.

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
H19 PROJECTION ZONE             30U
H999BOARD SERIAL NUMBER         1146
R        3 001 539356.31 5303810.03  3.0  1000 539405.61 5303788.26  5.0  48.0 1622033224.801 2000
R        3 002 539356.31 5303810.03  3.0  1000 539401.21 5303794.97  5.0  48.0 1622033232.800 2000
R        3 003 539356.31 5303810.03  3.0  1000 539396.80 5303801.68  5.0  48.0 1622033240.801 2000
R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000
R        3 005 539356.31 5303810.03  3.0  1000 539387.98 5303815.09  5.0  48.0 1622033256.802 2000
R        3 006 539356.31 5303810.03  3.0  1000 539383.58 5303821.79  5.0  48.0 1622033264.802 2000
```
The datum file has a very strict syntax and its encoding is based on position and the user must comply with that.   

THe datum file is composed of a header, immutable, that specifies keyword and its range of positions in the record.
The count of char is zerobased, this means
that the first char is chara number 0, and corresponds to the ```RECORD CODE```
Each keyword shows two digits: these are the position of the first and the last char that can be used to store the actual value in a record (line).


By using the immutable header, the class ```GDT``` interprets the file: 
i.e.:

```SHOT Y [NORTHING]``` is stored from char ```26``` to char ```37```, it value, in the case, is ```5303810.03```
```#SHOT EPOCH``` is stored from char ```80``` to char ```94```, its value, in the case, is ```1622033248.801```, note that ```SHOT EPOCH``` is a float with three decimals and its unit is seconds.
If the actual value is shorter than the allotted chars, left-align the value and fill the gap with spaces.

```
#SHOT Y [NORTHING]         26   37
#0       1         2         3         4         5         6         7         8         9
#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789

R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000
```
