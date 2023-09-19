# DAR_TOOLIT User Manual

DAR_TOOLKIT is a command line pure python script intended to manipulate DAR RAW data, as donwloaded from the acquisition unit

## Dependedncies
DAR_TOOLKIT depends on the availability of the following packages

```
argparse   pip install argparse
feather    pip install feather-format
obspy      pip install obspy
pandas     pip install pandas
pickle     Noramlly deployed with Python
pyproj     pip install pyproj
simplemkl  pip install simplekml
```

Invoke DAR_TOOLKIT wqith the following command to get help
```
python .\DAR_TOOLKIT.py -h
usage: DAR_TOOLKIT.py [-h] -f F -c C [-g G] [-t T]

options:
  -h, --help  show this help message and exit
  -f F        Input Filename - DAR RAW fileformat
  -c C        Configuration file
  -g G        Geometry file
  -t T        Output type [CSV(Z), FTH, PKL, VU]
```
