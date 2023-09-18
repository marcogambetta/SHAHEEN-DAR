# SHAHEEN DAR
This repository contains the code needed to extract and interpret DAR raw data and create output
in several different formats including SEGY

## General data flow scheme
In general, data are continuously recorded on board the AVU by the DAR. Data are stored in a custom format on an sd card.

Using the provided tool DART_TEST (Windows) it is possible to interpret and download the recorded data and save it as _RAW_ data

![sketch](/RES/IMG_00.png)


###Configuration file
The configuration file is used by the app to convert ADC  to physical data, to set gain and define the way the SEGY data is create 
geophone_scalar = 0.000000029017
hydrophone_scalar = 0.00000029597
geophone_gain = 8
hydrophone_gain = 8
SEGY_samples_before_event =2000
SEGY_trace_samples = 5000

