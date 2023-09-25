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

Shooting time is independently recorded by the shooting equipment and the corresponding data ($SRC_X$,$SRC_Y$,$SRC_Z$,```SHOT_EPOCH```) must be provided.

Receiver time is provided by the DAR, embedded in the data file. DAR unit is GPS synchronized so it happens for the Navigation units which benefit from a direct GPS link through surface vehicles.

