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
 A working example of  _GT DATUM_ is in folder DEMODATA of this repository

 
   
