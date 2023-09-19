# SHAHEEN DAR
This repository contains the code needed to extract and interpret DAR raw data[^1] and create output
in several different formats including SEGY

## General data flow scheme
In general, data are continuously recorded on board the AVU by the DAR. Data are stored in a custom format on an SD card.

Using the provided tool DART_TEST (Windows) it is possible to interpret and download the recorded data and save it as _RAW_ data

![sketch](/RES/IMG_00.png)

[^1]: Format description is provided in DOCUMENTATION/DAR RAW FILE FORMAT SPECS.pdf

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
[^2]: there is no way to store gain information in any file when running the acquisition. Gain must be manually written in some configuration. Best Practice is to make a note in the comment box before launching the acquisition with DAT_TEST

Sensor scalars are defined for the specific sensors mounted on the shaheens. Altering/replacing the sensor requires scalar adjustment

#HOW TO START ACQUISITION

Data acquisition is managed by DAR_TEST software, created by SBGS [SeaBed GeoSolutions]. This company winded off in 2018, thus there is no support available for their products.

DAR_TEST suite is available for download within this repository [DAR_TEST Suite](RES\205-DAR_SOFTWARE.zip). DAR_TEST documentation from the author is included in the archive.

##Start up Acquisition Procedure 

1. Configure an Ethernet router to operate in 192.168.0.nnn
2. Power up the AUV
3. Connect the AUV to a router (DHCP) using the provided ethernet cable, plugged into the recharge/data socket, located in the AUV tail.
4. Connect the router to a Windows-based PC.
5. Start DAR_TEST
6. Provide IP and PORT (56789) of the wired unit. Normally AUV IP is visible from the router web page (preferable), or it can be scanned using DAR_TEST.
7. press the Connect DAR button

![sketch](/RES/IMG_01.png)

Once DAR is connected the button Recording becomes active. Press it and the Recording Sequence Dialog pops up.

1. set the sampling rate
2. set the gain for geophones
3. set the gain for hydrophone
4. set the phase filter (Minimum phase)
5. check that channels 0 to 4 are enabled
6. fill the comment text box with gain values and other information you may want to store

1. First list item
   - First nested list item
     - Second nested list item

7. TIME SYNC
   _ If DAR is synchronized with GPS just press SET TIME
   _ If GPS Sync is not available then check the checkbox Use CPU Time
8. press Start Recording   

   






