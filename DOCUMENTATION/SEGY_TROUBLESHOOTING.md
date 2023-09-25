<h1>SEGY TROUBLESHOOTING</h1>

SEGY creation is a sensitive procedure, very sensitive to the multiple inputs required.

Data required to create SEGY 
1) sensor data, with timestamp
2) AUV positioning data, with timestamp
3) Source positioning data, with timestamp

it is evident that misalignments between the clocks of the three systems lead to errors, which can be large and jeopardize the result.
Similarly, the uncertainty of positioning pushes delays in the direct wave travel time that results in an error.

It is noteworthy to stress the fact that 1.5 m of uncertainty on positioning equates to 1 millisecond of error in the data reconstruction.
As per the Oil and Gas industry, errors larger than a few milliseconds make the recording not usable.

Also, the faster the sampling rate, the more accurate needs to be positioning and clock synchronization.

<h2>DC Timeshift</h2>

This error is fairly easy to compensate for because of its static (constant) nature. The error might be caused by human mistakes or equipment malfunction. In any case it a constant time delay between the clocks.

Shooting time is independently recorded by the shooting equipment and the corresponding data ($SRC_X$, $SRC_Y$, $SRC_Z$, ```SHOT_EPOCH```) must be provided.

Receiver time is provided by the DAR, embedded in the data file. DAR unit is GPS synchronized so it happens for the Navigation units which benefit from a direct GPS link through surface vehicles.

<table><tr><td>Syncronization refers to the whole ensemble, all the AUV and the SOURCE must share the same time axis, synchronized at least at the actual sampling rate of the fastest sampling device, advisable at 1 millisecond</td></tr></table>
Constant time shift correction can be applied on a _feather format_ data file using a script provided in this repository:

[the script : TIME_SHIFT](DAR_TOOLKIT.md#TIME_SHIFT)

<h3>Proceure to obtain data for AUV Time alignment</h3>

It is very advisable, prior to and after acquisition and despite the fact that DARs are GPS 1PPS synchronized, to make a specific acquisition that can be helpful to retrieve synchronization.

1) place the units in mutual close proximity, ideally, the whole ensemble should stay in a box on 1.5 x 1.5 m. If the units touch each other it is not an issue. the unit can be tied together.
2) All the units must be in acquisition mode.
3) make a sequence of shots at a suitable distance, depending on the volume and pressure fired. The recorded signal should not saturate and the wave should be well formed; some preliminary tests might be required.
4) the sequence of shots should last the needed time to collect a dozen of well-formed shot's recording with adequate time separation between each first break.
5) Take note of the UTC test time
6) Download the data and extract the time-slice corresponding the tests (initial and final) so to have two feather-format files for each AUV
7) Inspect the files with ```STREAM_VIEW```
8) 


