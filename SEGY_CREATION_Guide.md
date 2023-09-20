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


some energy is recorded. This is the energy that propagates from a source point through the seawater and reaches the sensor. To create a seismic trace it is necessary to know the time of the explosion (_**shot epoch**_) and the reciprocal position of the source and the receiver.

Knowing the reciprocal position of source and receiver the Euclidean distance is known and thus the travel time of the direct wave, assuming the sound speed in seawater is constant. this information is also used to independently check the accuracy of the positioning system. Knowing the travel time the wanted signal can be uniquely identified in time.

A convenient delay, an amount of time _before_ the actual shot, is defined, and similarly, a convenient time duration to encompass the whole energy recorded by the sensor is defined. This information is used to excerpt the data from the stream of data and create the SEGY data body. This is applied to all channels recorded by the recording device.


   
