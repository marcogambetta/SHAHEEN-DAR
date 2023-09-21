import argparse
import feather, pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DARV import Sequence,TimestampFromDatetime,DatetimeFromTimestamp
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, help="Input Filename - Feather format",required = True)
parser.add_argument("-c", type=int, default=3, help="Channel, as defined in Attributes, default is 3, Hydrophone")
parser.add_argument("-i", type=str, help="time interval for XLS and CSV output")
parser.add_argument("-m", type=str, default = 'plot', help="working mode : plot (default), info")

args = parser.parse_args()

class localSequence:
    def __init__(self):
        self.Dataframe= None
        self.Attributes= None


def getDFrange(Sqx,timerange):
    try:
        interval_dt_start = timerange.split(' to ')[0]
        interval_dt_end = timerange.split(' to ')[1]
        interval_ts_start = TimestampFromDatetime(interval_dt_start)+3600
        interval_ts_end = TimestampFromDatetime(interval_dt_end)+3600

        print("{0:25s} {1:^30s} {2:^30s}".format('', 'Start', 'End'))
        print("{0:25s} {1:>30s} {2:>30s}".format('-' * 25, '-' * 30, '-' * 30))

        print("{0:>25s} {1:>30s} {2:>30s}".format('Data Datetime', str(Sqx.Dataframe['Datetime'].iloc[0]),
                                                  str(Sqx.Dataframe['Datetime'].iloc[-1])))
        print("{0:>25s} {1:>30s} {2:>30s}".format('Target Datetime', interval_dt_start, interval_dt_end))

        dtobj = datetime.strptime(interval_dt_end, '%Y-%m-%d %H:%M:%S')
        if  dtobj >  Sqx.Dataframe['Datetime'].iloc[-1] :   raise Exception('End timestamp not included in data range')
        dtobj = datetime.strptime(interval_dt_start, '%Y-%m-%d %H:%M:%S')
        if  dtobj <  Sqx.Dataframe['Datetime'].iloc[0] :   raise Exception('Start timestamp not included in data range')

        idx_start = np.where(Sqx.Dataframe['Datetime'] <= interval_dt_start)[0][-1]
        idx_end = np.where(Sqx.Dataframe['Datetime'] >= interval_dt_end)[0][0]

        chk = idx_end-idx_start
        if chk == 0 : raise Exception('Null Range')
        if chk <= 0 : raise Exception('Negative Range')

        print("{0:>25s} {1:>30d} {2:>30d}".format('Target indices', idx_start, idx_end))
        print("{0:25s} {1:>30s} {2:>30s}".format('-' * 25, '-' * 30, '-' * 30))
        print("{0:>25s} {1:<30d} {2:>30s}".format('Total Record', idx_end - idx_start, ' '))
        print("{0:25s} {1:>30s} {2:>30s}".format('-' * 25, '-' * 30, '-' * 30))
        index_rng = list(range(idx_start, idx_end))

        return index_rng, str(interval_dt_start),str(interval_dt_end)
    except Exception as e:
        print ('\n Fatal Exception : ',e)
        print (' Check input formats and consistency with the input time boundaries.')
        print (' Execute a run using "-t vu"  and inspect the output of the seismic data summary for channels Datetime and Timestamp\n\n.')
        quit()


def showAttibutes(d):
    outs = '\n'
    for k in sorted(d.keys()):
        v = Sqx.Attributes[k]
        try:
            if type(v) is int:
                outs+=('\t{0:>70s} : {1:<10d}\n'.format(k, v))
            elif type(v) is float:
                outs+=('\t{0:>70s} : {1:<10.12f}\n'.format(k, v))
            elif type(v) is str:
                outs+=('\t{0:>70s} : {1:<40s}\n'.format(k, v))
        except:
            pass
    return outs

##-----------------------------------------------------------------------------------------------

#open feather format stream
with open(args.f, 'rb') as f:
    Sqx = localSequence()
    Sqx.Dataframe = feather.read_dataframe(f)
k = args.f.split('.raw.')
file_title = k[0]
boardID = k[1].split('.')[0]
try:
    with open(file_title+'.raw.Attributes.'+boardID+'.pkl', 'rb') as f:
         outdict= pickle.load(f)
    Sqx.Attributes = outdict['Attributes']
except Exception as e:
    print ('Fatal Exception\n\t',e,'\n\n\t Possible alteration of file names. Both feather format and Attributes dictionary are required.')
    print ('\n\t Feather format file name : <custom prefix>.raw.<4 digits Board ID>.feather')
    print('\t     Attributes file name : <custom prefix>.raw.Attributes.<4 digits Board ID>.pkl\n')
    quit()

if args.m.upper() == 'INFO':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    # Assimilate Geometry

    print('\n', '-' * 120, '\n\tSEISMIC DATABASE - HEAD\n', '-' * 120, '\n', Sqx.Dataframe.head().T, '\n')
    print('\n', '-' * 120, '\n\tSEISMIC DATABASE - TAIL\n', '-' * 120, '\n', Sqx.Dataframe.tail().T, '\n')
    print('\n', '-' * 120, '\n\tSEISMIC DATABASE - STATISTICS\n', '-' * 120, '\n', Sqx.Dataframe.describe().T, '\n')
    print('\n', '-' * 120, '\n\tSEISMIC ATTRIBUTES\n', '-' * 120, '\n', showAttibutes(Sqx.Attributes), '\n')
    quit()

if args.i is not None :
    Sqx.Dataframe = getDFrange(Sqx,args.i)


fig, (ax0, ax1) = plt.subplots(2, 1, layout='constrained')
s = Sqx.Dataframe['Channel'+str(args.c)]
t =  Sqx.Dataframe['Datetime']
dt = Sqx.Dataframe['Timestamp'].iloc[1]-Sqx.Dataframe['Timestamp'].iloc[0]
ax0.plot(t, s, label='Channel'+str(args.c) )
ax0.set_xlabel('Time (s)')
ax0.set_ylabel('Signal')
ax0.legend()
ax1.psd(s, 512, 1 / dt)
fig.suptitle(args.f)
plt.show()
