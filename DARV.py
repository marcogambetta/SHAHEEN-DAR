"""
DAR Decoder class

versioning
1.0 - 13 Jan 2020
2.0 - 26 Mar 2020 (reduced numpy to needed modules, made linspace integer)
3.0 - 15 June 2020, updated time array creation
4.0 - 29 June 2020 (aux decode implemented)
6.0 - 13 Nov 2020 (aligned with GTVU 6.0)
7.0 - 01 Apr 2021 (complete revision)
8.0 - 19 Nov 2021 (further revision to create a class able operate as stand alone command line, to be invoked by DAR_TOOLKIT.py).

Author:
M.GAMBETTA
Ph.D Geophysicis, Geologist,
Project Manager
_______________
GRAALTECH SRL

All rights reserved to GRAALTECH SRL.

Discalimer
No alteration of this code is allowed.
Not to be used without GRAALTECH's express consent.
No parts or whole of this code can be dissemitated by any means, copied and/or distributed
without GRAALTECH's express written consent.

"""

BlockStructure = {
    0: [0, 3, 'Start of Second Code'],
    1: [4, 7, 'Current UTC Time'],
    2: [8, 8, 'Data Packet type'],
    3: [9, 9, 'Recording sequence'],
    4: [10, 13, 'Starting Disc Sector'],
    5: [14, 17, 'Line Number Identification'],
    6: [18, 21, 'Station Number Identification'],
    7: [22, 23, 'Aux  Chans Status'],
    8: [24, 25, 'Aux Channel 0 Sample interval (in seconds)  '],
    9: [26, 27, 'Aux Channel 1 Sample interval (in seconds)  '],
    10: [28, 29, 'Aux Channel 2 Sample interval (in seconds)  '],
    11: [30, 31, 'Aux Channel 3 Sample interval (in seconds)  '],
    12: [32, 33, 'Aux Channel 4 Sample interval (in seconds)  '],
    13: [34, 35, 'Aux Channel 5 Sample interval (in seconds)  '],
    14: [36, 37, 'Aux Channel 6 Sample interval (in seconds)  '],
    15: [38, 39, 'Aux Channel 7 Sample interval (in seconds)  '],
    16: [40, 41, 'Aux Channel 8 Sample interval (in seconds)  '],
    17: [42, 43, 'Aux Channel 9 Sample interval (in seconds)  '],
    18: [44, 45, 'Aux Channel 10 Sample interval (in seconds) '],
    19: [46, 47, 'Aux Channel 11 Sample interval (in seconds) '],
    20: [48, 49, 'Aux Channel 12 Sample interval (in seconds) '],
    21: [50, 51, 'Aux Channel 13 Sample interval (in seconds) '],
    22: [52, 53, 'Aux Channel 14 Sample interval (in seconds) '],
    23: [54, 55, 'Aux Channel 15 Sample interval (in seconds) '],
    24: [56, 56, 'Data Channels  @ 1 ms (Binary xxxx xxxx - chans 0 to 7, Off=0, On =1)'],
    25: [57, 57, 'Data Channels  @ 2 ms (Binary xxxx xxxx - chans 0 to 7, Off=0, On =1)'],
    26: [58, 58, 'Data Channels  @ 4 ms (Binary xxxx xxxx - chans 0 to 7, Off=0, On =1)'],
    27: [59, 59, 'Data Channels  @ 8 ms (Binary xxxx xxxx - chans 0 to 7, Off=0, On =1)'],
    28: [60, 61, 'Minimum Battery Voltage Setting at start of recording (millivolts)'],
    29: [62, 63, 'Battery Voltage at start of recording (millivolts)'],
    30: [64, 65, 'Temperature at start of recording (signed degrees C)'],
    31: [68, 69, 'Offset to apply to Y tilt (signed short)'],
    32: [70, 71, 'Offset to apply to Z tilt (signed short)'],
    33: [72, 73, 'Scale to apply X tilt (signed short)'],
    34: [74, 75, 'Scale to apply Y tilt (signed short)'],
    35: [76, 77, 'Scale to apply Z tilt (signed short'],
    36: [78, 79, 'X tilt value at beginning of recording'],
    37: [80, 81, 'Y tilt value at beginning of recording'],
    38: [82, 83, 'Z tilt value at beginning of recording'],
    39: [84, 85, 'Pressure at beginning of recording (bars?)'],
    40: [86, 89, 'Recorder Board  Firmware Revision – dd mm yy bb (day month year build) '],
    41: [90, 93, 'Recorder Board  FPGA #1 Revision '],
    42: [94, 97, 'Recorder Board  FPGA #2 Revision  '],
    43: [98, 101, 'Recorder Board Serial Number     '],
    44: [102, 105, 'Recorder Board Hardware Revision  '],
    45: [106, 109, 'Communication Board  Firmware Revision – dd mm yy bb (day month year build)'],
    46: [110, 113, 'Communication Board Serial Number'],
    47: [114, 117, 'Communication Board Hardware Revision'],
    48: [118, 118, 'Recorder Board Clock Type'],
    49: [119, 119, 'Recorder Unit Type'],
    50: [120, 120, 'Command code used to start this recording (I.E.  0x41, 0x85, etc'],
    51: [121, 121, 'Phase filter used on this recoding 0 =Linear 1= Minimum'],
    52: [122, 255, 'Reserved, written as zero)'],
    53: [256, 511, 'Comments'],
}

import  struct, os, binascii
import numpy as np
import pandas as pd
import feather

from numpy import linspace, array_split
from datetime import datetime
import time,pytz





# TIMESTAMP - DATETIME CONVERTERS

#given timestamp and timezone returns a datetime object
def DatetimeFromTimestamp(timestamp=None, tz=pytz.timezone("Europe/Amsterdam")):
    dt_obj = datetime.fromtimestamp(timestamp, tz)
    x = dt_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    return x

#given Dattime string returns Timestamp
def TimestampFromDatetime( date_time_str = None):
    if not '.' in date_time_str :
        date_time_str = date_time_str+'.000'
    dtobj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    ts = time.mktime(dtobj.timetuple())
    return  ts

#given a datetime object returns a formatted string
def StringFromDatetime(dtobj):
    return str(dtobj[:23])



class Sequence:
    """ Class Constructor
        Filename is mandatory

        Usage :
        from dar import Sequence
        sqx=Sequence(filename='t.raw')

        Note :
        DEV Release : NOT TO BE USED IN PRODUCTION
        File structure is hardcoded in each module.
     _______________________________
     rev 1.0 Mon 13/01/20 M.Gambetta first draft
     rev 1.1 Thr 16/01/20 M.Gambetta decoded seismic data into _d structure, not scaled
     rev 1.2 Thr 29/01/20 M.Gambetta decoded seismic data into _d structure, not scaled
     rev 4.0  July 2020 M.Gambetta : integrated attributes, Data to Pandas Dataframe
     rev 7.0 April 2021 M.Gambetta : Corrected Timezone, simplified code, improved info
     rev 8.0 November 2021 M.Gambetta : Implemented more ATTRIBUTES, simplified the code and corrected timestamp.
     _______________________________



    """

    def __init__(self, filename=None, MaxBlockToProcess=None, TimeWindow=None, InfoOnly=None, debug=False):
        self.TimeWindow = TimeWindow
        self.InfoOnly = InfoOnly
        if TimeWindow == None:
            self.tw = {'ini': None, 'end': None, 'active': False}
        else:
            self.tw = {'ini':TimestampFromDatetime(self.TimeWindow[0]),
                       'end': TimestampFromDatetime(self.TimeWindow[1]),
                       'active': True}
        self.blocksize = {128: 512, 129: 512, 1: None}
        self.AUXchannels = {'Total': 16, 'Active': 0, 'Status': None}
        self.SEISchannels = {'Total': 8, '1ms': [], '2ms': [], '4ms': [], '8ms': []}
        self.FileName = filename
        self.FileObj = open(self.FileName, mode='rb')
        self.Filesize = os.path.getsize(self.FileName)
        self.TotalDataBlocks = 0
        self.MinSamplingRate = 0

        self.MaxBlockToProcess = MaxBlockToProcess  # Number of data blocks to convert.Implemente for debug/develop purposes only.
        # Data Structure
        self.OUTPUT = {}
        self._d = {'timestamp': [],
                   'channels': {0: [], 1: [], 2: [],3: [],4: [],5: [],6: [],7: []},
                   'aux': {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [],
                           13: [], 14: [], 15: []},
                   'packettimestamp': [],
                   'attributes': {}
                   }
        self._listAllBlocks()
        self.FileObj.close()

    def err(self, ern=None):
        print('Fatal Exception ' + str(ern))
        quit()

    """ Method : _getBlockType

     Description :
     This method gets a given block type providing the pointer offset.
     If block type is 128 and/or 129 ancillary information are derived and stored into attributes.

     Usage :
     sqx=Sequence(filename='t.raw')
     sqx._getBlockType()
     print(sqx.AUXchannels,sqx.SEISchannels,sqx.blocksize)

     note : 
     Use this methods with no offset to get the first block of the datafile.
     blocksize data provides the information to acquire the next block.

     _______________________________
     rev 1.0 Mon 13/01/20 M.Gambetta
     rev 2.0 Fri 19/11/21 M.Gambetta
    """

    def _getBlockType(self, offset=None):
        out = {}
        if offset is None: offset = 0

        self.FileObj.seek(0 + offset)
        bytes = self.FileObj.read(4)
        out['Start of Second Code'] = int.from_bytes(bytes, byteorder='big')

        self.FileObj.seek(4 + offset)
        bytes = self.FileObj.read(4)
        dtime_obj =  DatetimeFromTimestamp(int.from_bytes(bytes, byteorder='big')) #convert timestamp to datetime object
        out['Current UTC Time'] = StringFromDatetime(dtime_obj) # store datetime as string

        self.FileObj.seek(8 + offset)
        bytes = self.FileObj.read(1)
        out['Data Packet type'] = int.from_bytes(bytes, byteorder='big')
        if not out['Data Packet type'] in [128,129,1] :
            out['Data Packet type'] = None
            return out

        self.FileObj.seek(9 + offset)
        bytes = self.FileObj.read(1)
        out['Recording sequence'] = int.from_bytes(bytes, byteorder='big')

        if out['Data Packet type'] in [129]:  # END LOG block
            self.FileObj.seek(60 + offset)
            bytes = self.FileObj.read(2)
            out['Minimum Battery Voltage Setting at stop of recording (millivolts)'] = int.from_bytes(bytes, byteorder='big')
            self.FileObj.seek(62 + offset)
            bytes = self.FileObj.read(2)
            out['Battery Voltage at stop of recording (millivolts)'] = int.from_bytes(bytes, byteorder='big')

            self.FileObj.seek(64 + offset)
            bytes = self.FileObj.read(2)
            out['Temperature at stop of recording (signed degrees C)'] = int.from_bytes(bytes, byteorder='big',signed=True)

            self.FileObj.seek(78 + offset)
            bytes = self.FileObj.read(2)
            out['X tilt value at stop of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(80 + offset)
            bytes = self.FileObj.read(2)
            out['Y tilt value at stop of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(82 + offset)
            bytes = self.FileObj.read(2)
            out['Z tilt value at stop of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(86 + offset)
            bytes = self.FileObj.read(4)
            out['Last Clock Set to GPS time (UTC)'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(90 + offset)
            bytes = self.FileObj.read(4)
            out['Last Skew Check to GPS time(UTC)'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(94 + offset)
            bytes = self.FileObj.read(4)
            out['Micro Second Skew Detected'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(94 + offset)
            bytes = self.FileObj.read(4)
            out['Last skew value in PPM'] = struct.unpack('>f', bytes)[0] # big-endian


        if out['Data Packet type'] in [128]:  # START LOG block
            # AUX channels
            self.FileObj.seek(22 + offset)
            bytes = self.FileObj.read(2)
            self.AUXchannels['Status'] = str(bin(int('0x' + binascii.hexlify(bytes).decode(), 16))[2::])
            self.AUXchannels['Active'] = sum(list(map(int, self.AUXchannels['Status'])))

            # DATA channels
            self.FileObj.seek(56 + offset)
            bytes = self.FileObj.read(1)
            k = ''.join(format(byte, '08b') for byte in bytes)
            self.SEISchannels['1ms'] = [i for i, ltr in enumerate(k) if ltr == '1']

            self.FileObj.seek(57 + offset)
            bytes = self.FileObj.read(1)
            k = ''.join(format(byte, '08b') for byte in bytes)
            self.SEISchannels['2ms'] = [i for i, ltr in enumerate(k) if ltr == '1']

            self.FileObj.seek(58 + offset)
            bytes = self.FileObj.read(1)
            k = ''.join(format(byte, '08b') for byte in bytes)
            self.SEISchannels['4ms'] = [i for i, ltr in enumerate(k) if ltr == '1']

            self.FileObj.seek(59 + offset)
            bytes = self.FileObj.read(1)
            k = ''.join(format(byte, '08b') for byte in bytes)
            self.SEISchannels['8ms'] = [i for i, ltr in enumerate(k) if ltr == '1']

            self.SEISchannels['Total'] = len(self.SEISchannels['1ms']) + len(self.SEISchannels['2ms']) + len(
                self.SEISchannels['4ms']) + len(self.SEISchannels['8ms'])
            # Block Size
            self.blocksize[1] = (10 + self.AUXchannels['Active'] * 4 + (1000 * len(self.SEISchannels['1ms'])) * 3 + (
                        500 * len(self.SEISchannels['2ms'])) * 3 + (250 * len(self.SEISchannels['4ms'])) * 3 + (
                                             125 * len(self.SEISchannels['8ms'])) * 3)
            # Minimum Sampling rate
            if len(self.SEISchannels['8ms']) > 0:
                self.MinSamplingRate = 8
            else:
                if len(self.SEISchannels['4ms']) > 0:
                    self.MinSamplingRate = 4
                else:
                    if len(self.SEISchannels['2ms']) > 0:
                        self.MinSamplingRate = 2
                    else:
                        if len(self.SEISchannels['1ms']) > 0:
                            self.MinSamplingRate = 1
                        else:
                            self.err(ern=100)

            self.FileObj.seek(60 + offset)
            bytes = self.FileObj.read(2)
            out['Minimum Battery Voltage Setting at start of recording (millivolts)'] = int.from_bytes(bytes,
                                                                                                       byteorder='big')

            self.FileObj.seek(62 + offset)
            bytes = self.FileObj.read(2)
            out['Battery Voltage at start of recording (millivolts)'] = int.from_bytes(bytes, byteorder='big')

            self.FileObj.seek(64 + offset)
            bytes = self.FileObj.read(2)
            out['Temperature at start of recording (signed degrees C)'] = int.from_bytes(bytes, byteorder='big',
                                                                                         signed=True)
            self.FileObj.seek(66 + offset)
            bytes = self.FileObj.read(2)
            out['Offset to apply to X tilt (signed short)'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(68 + offset)
            bytes = self.FileObj.read(2)
            out['Offset to apply to Y tilt (signed short)'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(70 + offset)
            bytes = self.FileObj.read(2)
            out['Offset to apply to Z tilt (signed short)'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(72 + offset)
            bytes = self.FileObj.read(2)
            out['Scale to apply X tilt'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(74 + offset)
            bytes = self.FileObj.read(2)
            out['Scale to apply Y tilt'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(76 + offset)
            bytes = self.FileObj.read(2)
            out['Scale to apply Z tilt'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(78 + offset)
            bytes = self.FileObj.read(2)
            out['X tilt value at start of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(80 + offset)
            bytes = self.FileObj.read(2)
            out['Y tilt value at start of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(82 + offset)
            bytes = self.FileObj.read(2)
            out['Z tilt value at start of recording'] = int.from_bytes(bytes, byteorder='big', signed=True)

            self.FileObj.seek(100 + offset)
            bytes = self.FileObj.read(2)
            out['Board Serial Number'] = int.from_bytes(bytes, byteorder='big', signed=True)

        return out

    def save(self, fname=None):
        if fname == None:
            path = self.FileName.strip().split('.')[0] + '-'+str(self.Attributes['Board Serial Number'])+'.feather'
        else:
            path = fname
        feather.write_dataframe(self.Dataframe, path)

    def _listAllBlocks(self):
        trap = True
        ofs = 0
        while trap == True:
            # check if pointer reached the end of the file.
            print ("Reading data is ongoing : {0:5.2f}%".format(ofs/self.Filesize*100), end="\r", flush=True)
            #get block from source file
            ablock = self._getBlockType(offset=ofs)
            #test if block type is one of the expected
            if ablock['Data Packet type'] not in [128, 129, 1]:
                print ('\n\tFATAL EXCEPTION : Unexpected packet type\n')
                quit()
            #START LOG PACKET
            if ablock['Data Packet type'] == 128:
                ofs = ofs + 512
                self._d['attributes']['Minimum Battery Voltage Setting at start of recording (millivolts)'] = ablock[
                    'Minimum Battery Voltage Setting at start of recording (millivolts)']
                self._d['attributes']['Battery Voltage at start of recording (millivolts)'] = ablock[
                    'Battery Voltage at start of recording (millivolts)']
                self._d['attributes']['Temperature at start of recording (signed degrees C)'] = ablock[
                    'Temperature at start of recording (signed degrees C)']
                self._d['attributes']['Offset to apply to X tilt (signed short)'] = ablock[
                    'Offset to apply to X tilt (signed short)']
                self._d['attributes']['Offset to apply to Y tilt (signed short)'] = ablock[
                    'Offset to apply to Y tilt (signed short)']
                self._d['attributes']['Offset to apply to Z tilt (signed short)'] = ablock[
                    'Offset to apply to Z tilt (signed short)']
                self._d['attributes']['Scale to apply X tilt'] = ablock['Scale to apply X tilt']
                self._d['attributes']['Scale to apply Y tilt'] = ablock['Scale to apply Y tilt']
                self._d['attributes']['Scale to apply Z tilt'] = ablock['Scale to apply Z tilt']
                self._d['attributes']['X tilt value at start of recording'] = ablock[
                    'X tilt value at start of recording']
                self._d['attributes']['Y tilt value at start of recording'] = ablock[
                    'Y tilt value at start of recording']
                self._d['attributes']['Z tilt value at start of recording'] = ablock[
                    'Z tilt value at start of recording']
                self._d['attributes']['Board Serial Number'] = ablock['Board Serial Number']
            # STOP LOG PACKET
            if ablock['Data Packet type'] == 129:
                ofs = ofs + 512
                self._d['attributes']['Minimum Battery Voltage Setting at stop of recording (millivolts)'] = ablock['Minimum Battery Voltage Setting at stop of recording (millivolts)']
                self._d['attributes']['Battery Voltage at stop of recording (millivolts)'] = ablock['Battery Voltage at stop of recording (millivolts)']
                self._d['attributes']['Temperature at stop of recording (signed degrees C)'] = ablock['Temperature at stop of recording (signed degrees C)']
                self._d['attributes']['X tilt value at stop of recording'] = ablock['X tilt value at stop of recording']
                self._d['attributes']['Y tilt value at stop of recording'] = ablock['Y tilt value at stop of recording']
                self._d['attributes']['Z tilt value at stop of recording'] = ablock['Z tilt value at stop of recording']
                self._d['attributes']['Last Clock Set to GPS time (UTC)'] =ablock['Last Clock Set to GPS time (UTC)']
                self._d['attributes']['Last Skew Check to GPS time(UTC)'] =ablock['Last Skew Check to GPS time(UTC)']
                self._d['attributes']['Micro Second Skew Detected'] = ablock['Micro Second Skew Detected']
                self._d['attributes']['Last skew value in PPM'] = ablock['Last skew value in PPM']

            #DATA PACKET
            if ablock['Data Packet type'] == 1:
                ofs = ofs + self.blocksize[1]
                if ofs >= self.Filesize:
                    trap = False
                else :
                    try :
                        t= TimestampFromDatetime(ablock['Current UTC Time'])
                        if len(self._d['timestamp']) > 1 :
                            if int(self._d['timestamp'][-1])+1 != int(t):
                                print ('\n\tFATAL EXCEPTION : Time gap\n\t', int (self._d['timestamp'][-1])+1, int(t))
                                quit()
                    except :
                        print('\n\tFATAL EXCEPTION : Unexpected timestamp\n\t'+str(ablock['Current UTC Time'])+'\n')
                        quit()
                    self._d['packettimestamp'].append(t)
                    #process data
                    if ((self.tw['active'] == True) and (self.tw['ini'] <= t) and (self.tw['end'] >= t) == True) or self.tw['ini'] == None:
                        k = linspace(0, (1000 - self.MinSamplingRate), int(1000 / self.MinSamplingRate)) / 1000.0 + t
                        # increment block initial time by sampling rate
                        self._d['timestamp'].extend(list(k))  # populate timestamp list
                        if self.MinSamplingRate == 1: nchans = len(self.SEISchannels['1ms'])
                        if self.MinSamplingRate == 2: nchans = len(self.SEISchannels['2ms'])
                        if self.MinSamplingRate == 4: nchans = len(self.SEISchannels['4ms'])
                        if self.MinSamplingRate == 8: nchans = len(self.SEISchannels['8ms'])
                        self.FileObj.seek(ofs + 10)
                        # get AUX data
                        AUX_data = self.FileObj.read(self.AUXchannels['Active'] * 4)
                        aux_out_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        ll = [i for i in range(len(str(self.AUXchannels['Status']))) if
                              str(self.AUXchannels['Status']).startswith('1', i)]
                        for idx, k in enumerate(range(0, len(AUX_data), 4)):
                            aux_out_row[ll[idx]] = int.from_bytes(AUX_data[k + 1:k + 4], byteorder='big', signed=True)
                        tt = list(reversed(aux_out_row))
                        for idx, e in enumerate(tt):
                            self._d['aux'][idx].append(tt[idx])
                        # get SEIS data
                        bytes_object = self.FileObj.read(nchans * int(1000 / self.MinSamplingRate) * 3)
                        SEIS_DATA = [int.from_bytes(bytes_object[x:x + 3], byteorder='big', signed=True) for x in
                                     range(0, len(bytes_object), 3)]
                        SEIS_DATA = array_split(SEIS_DATA, nchans)
                        self._d['channels'][0].extend(list(SEIS_DATA[0]))
                        self._d['channels'][1].extend(list(SEIS_DATA[1]))
                        self._d['channels'][2].extend(list(SEIS_DATA[2]))
                        self._d['channels'][3].extend(list(SEIS_DATA[3]))

        print ('Accelerometer calibration is ongoing ... ',end="\r", flush=True)
        # Calibrates Accelerometers
        den = (float(self._d['attributes']['Scale to apply X tilt']) - self._d['attributes']['Offset to apply to X tilt (signed short)'])
        num = np.asarray(np.asarray(self._d['aux'][5] )* 724) - self._d['attributes']['Offset to apply to X tilt (signed short)']
        arr = num/den
        self._d['ACC_X'] = arr
        den = (float(self._d['attributes']['Scale to apply Y tilt']) - self._d['attributes']['Offset to apply to Y tilt (signed short)'])
        num = np.asarray(np.asarray(self._d['aux'][6] ) * 724) - self._d['attributes']['Offset to apply to Y tilt (signed short)']
        arr = num/den
        self._d['ACC_Y'] = arr
        den = (float(self._d['attributes']['Scale to apply Z tilt']) - self._d['attributes']['Offset to apply to Z tilt (signed short)'])
        num = np.asarray(np.asarray(self._d['aux'][7] )* 1024) - self._d['attributes']['Offset to apply to Z tilt (signed short)']
        arr = num/den
        self._d['ACC_Z'] =  arr
        # Computing tilts
        Gravity =  np.sqrt(np.square(self._d['ACC_X']) + np.square(self._d['ACC_Y']) + np.square(self._d['ACC_Z']))
        self._d['TILT_X']=np.arcsin(np.asarray(self._d['ACC_X'])/Gravity)*(180.0/np.pi)
        self._d['TILT_Y'] = np.arcsin(np.asarray(self._d['ACC_Y']) / Gravity)*(180.0/np.pi)
        self._d['TILT_Z'] = np.arcsin(np.asarray(self._d['ACC_Z']) / Gravity)*(180.0/np.pi)

        # creates fully qualified datatime from timestamp
        print ('Time axis creation is ongoing ...              ',end="\r", flush=True)
        self._d['datetime'] = []
        df = pd.DataFrame(self._d['timestamp'], columns=['Timestamp'])
        df.insert(0, 'Datetime', pd.to_datetime(df['Timestamp'], unit='s',utc=False), allow_duplicates=False)
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            if len(self._d['channels'][i]) > 0 :
               print('Adding seismic channel ' + str(i), len(self._d['channels'][i]), 'samples',end="\r", flush=True)
               if len(self._d['channels'][i]) == len(df['Timestamp']):
                   df.insert(0, 'Channel' + str(i), self._d['channels'][i], allow_duplicates=False)
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            print('Adding AUX channel ' + str(i), len(self._d['aux'][i]), 'samples', end="\r", flush=True)
            if len(self._d['packettimestamp']) == len(self._d['aux'][i]):
                k = np.interp(self._d['timestamp'], self._d['packettimestamp'], self._d['aux'][i])
            else:
                k = np.interp(self._d['timestamp'], self._d['packettimestamp'][0:-1], self._d['aux'][i])
            df.insert(0, 'AUX' + str(i), k, allow_duplicates=False)
        for i,j in enumerate(['TILT_X','TILT_Y','TILT_Z']):
            print('Adding Tilt channel ' + j+ '                ', end="\r", flush=True)
            if len(self._d['packettimestamp']) == len(self._d[j]):
                k = np.interp(self._d['timestamp'], self._d['packettimestamp'], self._d[j])
            else:
                k = np.interp(self._d['timestamp'], self._d['packettimestamp'][0:-1], self._d[j])
            df.insert(0, j, k, allow_duplicates=False)
        self.Dataframe = df
        self.Attributes = self._d['attributes']
        del self._d
        del df
        print ('                                                                      ',end="\r", flush=True)


