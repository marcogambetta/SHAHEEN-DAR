# SHAHEEN DAR
This repository contains the code needed to extract and interpret DAR raw data[^1] and create output
in several different formats including SEGY

## General data flow scheme
In general, data are continuously recorded on board the AVU by the DAR. Data are stored in a custom format on an sd card.

Using the provided tool DART_TEST (Windows) it is possible to interpret and download the recorded data and save it as _RAW_ data

![sketch](/RES/IMG_00.png)

[^1]: Format description is provided in [DAR RAW FILE FORMAT SPECS(DOCUMENTATION/DAR RAW FILE FORMAT SPECS.pdf)

### Configuration file
The configuration file is used by the app to convert ADC  to physical data, to set gain[^2], and to define the way the SEGY data is created
```
geophone_scalar = 0.000000029017
hydrophone_scalar = 0.00000029597
geophone_gain = 8
hydrophone_gain = 8
SEGY_samples_before_event =2000
SEGY_trace_samples = 5000
```
[^2]: there is no way to store gain information in any file when running the acquisition. Gain must be manually written in some configuration. Best Practice is to make a note in the comment box before launching acquisition with DAT_TEST

Sensors scalars are defined for the specific sensors mounted on the shaheens. Altering/replacing the sensor requires scalars adjustment



