#SEGY TROUBLESHOOTING

SEGY creation is a sensitive procedre, very sensitive to the multiple inputs required.

Data requirequed to create SEGY 
1) sensor data, with timestamp
2) AUV positioning data, with timestamp
3) Source positioning data, with timestamp

it is evident that misalignments between the clocks of the three systems lead to error, that can be large and jopardize the result.
Similarly uncertainty of positionin pushes delays in the direct wave traveltime that results as a error.

It is noteworthy stress the fact the 1.5 m of uncertainty queates 1 millisecond of error in the data reconstructioni.
As per Oil and Gas industry, errors larger than few milliseconds makes the recording not usable.

Also, the faste is the sampling rate, the more accurate needs to be positioning and clock synconization.

