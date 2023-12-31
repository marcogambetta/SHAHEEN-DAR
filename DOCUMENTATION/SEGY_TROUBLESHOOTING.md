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
![sketch](/RES/IMG_18.png)
8) place the cursor at the first break (bubble A) and take note of the time (bubble B) 
9) Iterate the procedure for all the AUV and both for initial and final synchronization acquisition
10) Assuming initial and final acquisition times report constant shifts, apply the shift to have a unique time origin.

    In the case of time shift drifting the procedure is complex and a tailored script must be created.
    
<h2>Source - AUV lack of synchronisation</h2>
It may happen that AUV and SOURCE time axis are not synchronized, which means there is a constant time shift between the clocks. 

Because AUV, DAR, and SOURCE **must** be synchronized this issue has to be solved.

<h3>Check the correctness</h3>
The potential time displacement can be verified using the propagation of sound waves in seawater. Since the speed of sound in seawater is constant at the scale of the transformation considered, the arrival time of the wave front at a given receiver can be calculated. This must correspond to the actual burst of energy recorded.

_First break_ $F_b$ is computed using **GEOMETRY** data.

$F_b = S_t+(D_{sr} / S_w)$

$S_t$ is the ```SHOT_EPOCH```, that is the point in time when the shot occurred, unit $[s]$. $D_{sr}$ is the Euclidean distance between source and receiver, unit $[m]$. $S_w$ is the sound speed in water, unit $[m/s]$

$D_{sr} = ((S_x-R_x)^2+(S_y-R_y)^2+(S_z-R_z)^2)^{1/2}$

where $S_{x,y,z}$ is the source 3D position and $R_{x,y,z}$ is the receiver (AUV) 3D position

$S_w$, the sound of speed in the water, is an integer value configured in the configuration file 

![sketch](/RES/IMG_19.png)

The sketch above shows a typical lack of synchronization between DAR/AUV and the GUN CONTROLLER (the SOURCE)

The vertical red line shows the provided shooting time and the computation provides the _Expected First break_, shown by the vertical blue line.

This example shows that the provided shooting is _Late_ with respect to the recorded burst of energy due to the propagation of the wave generated by the explosion. The red line is on the right of the recorded _First break_

In this example we assume that DAR/AUV is synchronized with GPS time, thus the lack of synchronization is on the gun controller clock.

The constant time shift can be compensated by setting the ```ShotEpochShift``` parameter in the configuration file 

```
ShotEpochShift =-1.234
```

```ShotEpochShift``` is a _real_ value whose unit is _seconds_. This value is algebraically added to the provided shooting time when it is necessary. The GEOMETRY file is **not** altered.





