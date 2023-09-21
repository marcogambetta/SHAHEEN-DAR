"""
DAR TOOLKIT
version 10.1 18/03/2022
Author M.Gambetta
marco.gambetta@graaltech.it

GRAAL TECH SRL
www.graaltech.com

-------------------------------------------------------------
Purpose
-------------------------------------------------------------
This app decodes and produces a SEGY out of RAW DAR datafile

-------------------------------------------------------------
Usage
-------------------------------------------------------------
  python DAR_TOOLKIT.py -h
  this comamnd line provides the minimal help

  python .\DAR_TOOLKIT.py -fi .\myDataFile.raw -c \.myConfig.ini -g .\myGeometry.gtd2 -t SEGY
  this command line decodes MyDatafile.raw into a shot gather [SEGY] as specified by myConfig.ini and myGeometry.gtd2

-------------------------------------------------------------
Requirements
-------------------------------------------------------------
 GEOMETRY FILE
 CONFIGURATION FILE [Ascii file]

-------------------------------------------------------------
 GEOMETRY FILE
-------------------------------------------------------------
 hereafter follows the self explanatory file format

#RECORD CODE                0   1
#LINE NAME                  2   10
#SPNB                      11   15
#SHOT X [EASTING]          16   25
#SHOT Y [NORTHING]         26   37
#SHOT Z [DEPTH]            38   42
#RECEIVER NUMBER           43   47
#RECEIVER X [EASTING]      48   57
#RECEIVER Y [NORTHING]     58   69
#RECEIVER Z [DEPTH]        70   73
#WATER BOTTOM              75   79
#SHOT EPOCH                80   94
#GUN PRESSURE              95   99
#0       1         2         3         4         5         6         7         8         9
#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
H18 PROJECTION TYPE             utm
H19 PROJECTION ZONE             30U
H999BOARD SERIAL NUMBER         1146
R        3 001 539356.31 5303810.03  3.0  1000 539405.61 5303788.26  5.0  48.0 1622033224.801 2000
R        3 002 539356.31 5303810.03  3.0  1000 539401.21 5303794.97  5.0  48.0 1622033232.800 2000
R        3 003 539356.31 5303810.03  3.0  1000 539396.80 5303801.68  5.0  48.0 1622033240.801 2000
R        3 004 539356.31 5303810.03  3.0  1000 539392.39 5303808.38  5.0  48.0 1622033248.801 2000


-------------------------------------------------------------
 CONFIGURATION FILE
-------------------------------------------------------------
 Hereafter follows the self explanatory configuration file format

geophone_scalar = 0.000000029017
hydrophone_scalar = 0.00000029597
geophone_gain = 8
hydrophone_gain = 8
SEGY_samples_before_event =2000
SEGY_trace_samples = 5000

-------------------------------------------------------------
SEGY TRACE ATTRIBUTES (Trace header)
-------------------------------------------------------------

BYTE	BYTE	DESC
0	    15	    EMPTY
16	    19	    SHOT POINT NUMBER
20	    23	    SHOT EPOCH BASE (second)
24	    27	    SHOT EPOCH MANTISSA (millisecond)
28	    29	    TRACE TYPE ID CODE
30	    31	    RECORDER SERIAL NUMBER
32	    55	    EMPTY
56	    59	    WATER DEPTH (cm)
60	    63	    SOURCE DEPTH (cm)
64	    67	    RECEIVER DEPTH (cm)
68	    69	    SOURCE PRESSURE(PSI)
70	    71	    EMPTY
72	    75	    SOURCE X (EASTING, meter)
76	    79	    SOURCE Y (NORTHING, meter)
80	    83	    RECEIVER X (EASTING, meter)
84	    87	    RECEIVER Y (NORTHING, meter)
88	    113	    EMPTY
114	    115	    NUMBER OF SAMPLES IN THIS TRACE
116	    117	    SAMPLE INTERVAL (millisecond)
118	    155	    EMPTY
156	    157	    SHOT YEAR
158	    159	    SHOT DAY OF THE YEAR
160	    161	    SHOT HOUR OF DAY
162	    163	    SHOT MINUTE OF HOUR
164	    165	    SHOT SECOND OF MINUTE
166	    203	    EMPTY


"""
import argparse
import feather, pickle
import pandas as pd
import numpy as np
from DARV import Sequence,TimestampFromDatetime
from GTD import gtd
from datetime import datetime

class localSequence:
    def __init__(self):
        self.Dataframe= None
        self.Attributes= None

def getDFrange(timerange):
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

#configure Pandas options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#configure argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, help="Input Filename - DAR RAW fileformat",required = True)
parser.add_argument("-c", type=str, help="Configuration file ",required = True)
parser.add_argument("-g", type=str, help="Geometry file ",required = False)
parser.add_argument("-t", type=str, help="Output type [CSV(Z), FTH, PKL, VU]",default='FTH')
parser.add_argument("-i", type=str, help="time interval for XLS and CSV output")

args = parser.parse_args()

print('\n' * 100, '\t{0:>30s} : {1:<50s}'.format('Source filename', args.f))
print('\t{0:>30s} : {1:<50s}\n'.format('Output format', args.t))


#Assimilate Configuration
with open(args.c, 'r') as f:
    content = f.readlines()
Config = {}
for e in content:
    k = e.strip().replace(' ', '').split('=')
    if k[0] in ['geophone_scalar', 'hydrophone_scalar']:
        Config[k[0]] = float(k[1])
    elif k[0] in ['geophone_gain', 'hydrophone_gain']:
        Config[k[0]] = int(k[1])
    else:
        Config[k[0]] = k[1]
del content
del f

#Initialize Geometry
if args.g is not None:
    Geometry = gtd(filename=args.g, config=Config)
else:
    Geometry = None

#parse input file extension
ext = args.f[-3::]
if ext == 'raw':
       #serialize DAR RAW
       Sqx = Sequence(filename=args.f)
       #stores sclars in Attributes and converts seismic data to phyical units.
       Sqx.Attributes['geophone_scalar'] = Config['geophone_scalar']
       Sqx.Attributes['hydrophone_scalar'] = Config['hydrophone_scalar']
       Sqx.Attributes['geophone_gain'] = Config['geophone_gain']
       Sqx.Attributes['hydrophone_gain'] = Config['hydrophone_gain']
       Sqx.Attributes['geophone_units'] = 'mm/s'
       Sqx.Attributes['hydrophone_units'] = 'microbar'
       Sqx.Attributes['channels'] = '0:Inline Geophone, 1: Crossline Geophone, 2: Vertical Geophone, 3 : Hydrophone'
       Sqx.Dataframe['Channel0_ADC'] = Sqx.Dataframe["Channel0"]
       Sqx.Dataframe['Channel1_ADC'] = Sqx.Dataframe["Channel1"]
       Sqx.Dataframe['Channel2_ADC'] = Sqx.Dataframe["Channel2"]
       Sqx.Dataframe['Channel3_ADC'] = Sqx.Dataframe["Channel3"]
       Sqx.Dataframe["Channel0"] = 1000 * Config['geophone_scalar'] * Sqx.Dataframe['Channel0_ADC'] / Config['geophone_gain']
       Sqx.Dataframe["Channel1"] = 1000 * Config['geophone_scalar'] * Sqx.Dataframe['Channel1_ADC'] / Config['geophone_gain']
       Sqx.Dataframe["Channel2"] = 1000 * Config['geophone_scalar'] * Sqx.Dataframe['Channel2_ADC'] / Config['geophone_gain']
       Sqx.Dataframe["Channel3"] = 1000000 * Config['hydrophone_scalar'] * Sqx.Dataframe['Channel3_ADC'] / Config['hydrophone_gain']

elif ext == 'her':
    #assimilate feather format
    with open(args.f, 'rb') as f:
        Sqx = localSequence()
        Sqx.Dataframe = feather.read_dataframe(f)
    k = args.f.split('.raw.')
    file_title = k[0]
    boardID = k[1].split('.')[0]
    #assimilate attributes
    try:
        with open(file_title+'.raw.Attributes.'+boardID+'.pkl', 'rb') as f:
             outdict= pickle.load(f)
        Sqx.Attributes = outdict['Attributes']
    except Exception as e:
        print ('Fatal Exception\n\t',e,'\n\n\t Possible alteration of file names. Both feather format and Attributes dictionary are required.')
        print ('\n\t Feather format file name : <custom prefix>.raw.<4 digits Board ID>.feather')
        print('\t     Attributes file name : <custom prefix>.raw.Attributes.<4 digits Board ID>.pkl\n')
        quit()

#------------------------------------------------------------------------------------------------------------------------
#output
#------------------------------------------------------------------------------------------------------------------------
if args.t.upper() == 'SEGY':
    try:
        from SEGY import segy
        # Compute Geometry
        Geometry.seismic_dataframe = Sqx.Dataframe
        Geometry.SoundSpeedInWater= Config['Sound_Speed_in_water']
        Geometry.parse()
        #Assimilate Geometry
        SGY = segy()
        SGY.set_seismic(Sqx)
        SGY.set_geometry(Geometry)
        SGY.set_configuration(Config)
        SGY.create()
    except Exception as e: 
        print ('Failed to execute because : ' + str(e))

if args.t.upper() == 'FTH':
    #Output Feather
    fo = args.f + '.' + str(Sqx.Attributes['Board Serial Number']) + '.feather'
    feather.write_dataframe(Sqx.Dataframe, fo)
    print('\n' * 100, '\t{0:>30s} : {1:<50s}'.format('Output filename', fo))
    # Output Attributes
    outdict = {'Attributes': Sqx.Attributes,
               'Source_filename': Sqx.FileName}
    fo = args.f + '.Attributes.' + str(Sqx.Attributes['Board Serial Number']) + '.pkl'
    pickle.dump(outdict, file=open(fo, "wb"))

if args.t.upper() == 'PKL':
     #Assimilate Geometry
     outdict = {'AUXchannels': Sqx.AUXchannels,
                'Attributes': Sqx.Attributes,
                'Dataframe': Sqx.Dataframe,
                'SEISchannels': Sqx.SEISchannels,
                'Source_filename': Sqx.FileName}
     fo = args.fi + '.' + str(Sqx.Attributes['Board Serial Number']) + '.pkl'
     pickle.dump(outdict, file=open(fo, "wb"))
     print('\n' * 100, '\t{0:>30s} : {1:<50s}'.format('Output filename', fo))

if args.t.upper() in  ['CSV','CSVZ','XLS']:
     # data
     print("Encoding dataframe to CSV/CSVZ/XLS                                         ", end="\r", flush=True)
     if args.i is not None:
        index_rng, dt_start, dr_end = getDFrange(args.i )
        outDF = Sqx.Dataframe.take(index_rng)
        fo = args.f + '.' + str(Sqx.Attributes['Board Serial Number']) +'_'+ dt_start.replace(' ','_').replace(':','-')+ '-to-'+dr_end.replace(' ','_').replace(':','-')
     else:
        outDF = Sqx.Dataframe
        fo = args.f + '.' + str(Sqx.Attributes['Board Serial Number'])

     if args.t.upper()  == 'CSV' :
        fo += '.csv'
        outDF.to_csv(fo, sep=';', header=True, index=False, chunksize=100000, encoding='utf-8')
     elif args.t.upper() == 'CSVZ':
         fo += '.csv.gz'
         outDF.to_csv(fo, sep=';', header=True, index=False, chunksize=100000, compression='gzip',encoding='utf-8')
     elif args.t.upper() == 'XLS':
         fo += '.xlsx'
         outDF.to_excel(fo)

     print('\t{0:>30s} : {1:<50s}'.format('Output Data filename', fo))
     # attributes
     fo = args.f + '.' + str(Sqx.Attributes['Board Serial Number']) + '_Attributes.csv'
     s = fo + '\n'
     s += showAttibutes(Sqx.Attributes)
     with open(fo, 'w') as f:
         f.write(s)
     print('\t{0:>30s} : {1:<50s}'.format('Output Attributes filename', fo))

if args.t.upper() == 'VU':
     print ('\n','-'*120,'\n\tSEISMIC DATABASE\n','-'*120,'\n',Sqx.Dataframe.describe().T,'\n')
     print ('\n','-'*120,'\n\tSEISMIC ATTRIBUTES\n','-'*120,'\n',showAttibutes(Sqx.Attributes),'\n')
     if Geometry is not None:
         Geometry.seismic_dataframe = Sqx.Dataframe
         Geometry.SoundSpeedInWater = Config['Sound_Speed_in_water']
         Geometry.parse()
         Geometry.show_Dataframe()
