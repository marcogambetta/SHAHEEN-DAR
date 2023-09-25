import argparse
import feather, pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DARV import Sequence,TimestampFromDatetime,DatetimeFromTimestamp
from datetime import timedelta,datetime
from shutil import copyfile

class localSequence:
    def __init__(self):
        self.Dataframe= None
        self.Attributes= None
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, help="Input Filename - Feather format",required = True)
parser.add_argument("-t", type=int, help="time shift in milliseconds",required = True)
parser.add_argument("-quiet", type=str, default = 'NO', help="specfy qiet YES not be asked for file substituion",required = False)
#get args
args = parser.parse_args()
#convert time correction into seconds
time_correction = args.t /1000.0
#show the user the input file and correction
print ('\n'*10)
print('\t{0:>30s} : {1:<50s}'.format('Input filename', args.f))
print('\t{0:>30s} : {1:<s} millis [{2:<s}] '.format('Time shift', str(args.t),str(timedelta(seconds = time_correction))))
#check use if not in quiet mode
if args.quiet.upper() != 'YES':
    akn = input("\n\tWARNING\n\t-------\n\tThe orginal file will be replaced!\n\tA copy of it will be created as :"+ args.f+'.ORIGINAL.feather\n\n\t>> Type "YES" if agree ')
    if  akn.upper() == 'YES':
        # copy the original file
        copyfile(args.f, args.f + '.ORIGINAL.feather')
ext = args.f[-3::]
if ext == 'her':
    #assimilate feather format
    with open(args.f, 'rb') as f:
        Sqx = localSequence()
        Sqx.Dataframe = feather.read_dataframe(f)

h = []
for i in [0,1,2,3]:
    h.append(Sqx.Dataframe.Timestamp.iloc[i])
Sqx.Dataframe.Timestamp=Sqx.Dataframe.Timestamp+time_correction
#remove dataframe column in place
Sqx.Dataframe.drop('Datetime', axis=1, inplace=True)
#insert Datetime created with shifted Timestamp
Sqx.Dataframe.insert(0, 'Datetime', pd.to_datetime(Sqx.Dataframe['Timestamp'], unit='s', utc=False), allow_duplicates=False)

print('\nExample of the correction to be applied\n','-'*35,'\n')
for i in range(4):
    print ("{0:>20.3f}  --> {1:<20.3f}  {2:<24s}   -->   {3:<24s}".format(h[i],
                                               Sqx.Dataframe.Timestamp.iloc[i],
                                               str(DatetimeFromTimestamp(h[i])),
                                               str(DatetimeFromTimestamp(Sqx.Dataframe.Timestamp.iloc[i]))
                                                         ))
if  akn.upper() == 'YES':
  feather.write_dataframe(Sqx.Dataframe, args.f)
  print ('\n Time shift correction has been applied to ', args.f,'\n'  )
else :
    print('\n No time shift correction has been applied because of the user denied permission to overwrite the input file\n ')
