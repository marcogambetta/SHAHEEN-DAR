import numpy as np
import pandas as pd

class gtd:
    def __init__(self, filename=None, seismic_dataframe= None,config=None):
        self.Filename = filename
        self._projection = None
        self._zone = None
        self._data = {}
        self._encoding = {}
        self.seismic_dataframe = seismic_dataframe
        self.Dataframe = None
        self.SoundSpeedInWater=config['Sound_Speed_in_water']
        self.ShotEpochShift=config['ShotEpochShift']

    def show_Dataframe(self):
        print('\n', '-' * 120, '\n\tGEOMETRY\n', '-' * 120)
        print (self.Dataframe.head(), '\n' * 2)
        print (self.Dataframe.tail(), '\n' * 2)

    def parse(self):
        #Read the GDT2 (modified SPS)
        with open(self.Filename , 'r') as f:
            c = f.readlines()
        for i, e in enumerate(c):
            if e.strip() == "#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789":
                h = list(map(str.strip, c[0:i]))
                d = list(map(str.strip, c[i + 1::]))
                break
        #Get Ancillary Information (constants)
        for e in d:
            if e[0:4] == "H18 ":
                self._projection = list(filter(None, e.split(' ')))[-1]
            if e[0:4] == "H19 ":
                self._zone = list(filter(None, e.split(' ')))[-1]
            if e[0:4] == "H999":
                self._board_serial_number= int(list(filter(None, e.split(' ')))[-1])
        #Get data encoding

        for e in h:
            k = e[0:27]
            v = e[27::]
            e = list(filter(None, v.split(' ')))  # clean the input
            if k[0:2] != '#0':
                self._encoding[k[1::].rstrip()] = {'ini': e[0], 'end': e[1]}
        #Get File content
        for k in self._encoding.keys():
            self._data[k] = []
        for e in d:
            if e[0:1] == 'R':
                for j in  self._encoding.keys():
                    if not j in ['INDEX','RECORD CODE','SPNB', 'RECEIVER NUMBER','LINE NAME'] :
                        self._data[j].append(float(e[int(self._encoding[j]['ini']) - 1:int(self._encoding[j]['end'])].lstrip()))
                    elif j in ['SPNB', 'RECEIVER NUMBER', 'LINE NAME']:
                        self._data[j].append(int(e[int(self._encoding[j]['ini']) - 1:int(self._encoding[j]['end'])].lstrip()))
                    # elif j in ['INDEX']:
                    #     timestamp = float(self._data['SHOT EPOCH'][-1])
                    #     self._data['INDEX'].append((self._seismictimestamp[self._seismictimestamp.ge(timestamp)].index[0]))  # index corresponding to picked event

        self._data.pop('RECORD CODE')
        self.Dataframe = pd.DataFrame.from_dict(self._data)

        #compute offset and time of expected first break
        self.Dataframe['SHOT EPOCH']  = self.Dataframe['SHOT EPOCH']+float(self.ShotEpochShift)
        self.Dataframe['3D_Offset'] = np.sqrt(np.square(self.Dataframe['SHOT X [EASTING]']-self.Dataframe['RECEIVER X [EASTING]'])+
                                              np.square(self.Dataframe['SHOT Y [NORTHING]'] - self.Dataframe['RECEIVER Y [NORTHING]']) +
                                              np.square(self.Dataframe['SHOT Z [DEPTH]'] - self.Dataframe['RECEIVER Z [DEPTH]']))
        self.Dataframe['DirectWave_Traveltime']= self.Dataframe['3D_Offset'] / float(self.SoundSpeedInWater)
        self.Dataframe['Expected_FB_Timestamp'] = self.Dataframe['SHOT EPOCH']+self.Dataframe['DirectWave_Traveltime']

        #compute index in seismic dataframe corresponding to the 'Expected_FB_Timestamp'
        expected_fb_index = []
        for v in np.array(self.Dataframe['Expected_FB_Timestamp']):
            expected_fb_index.append(np.where(v<= np.array(self.seismic_dataframe['Timestamp']))[0][0])
        self.Dataframe['Expected_FB_Index'] =expected_fb_index




