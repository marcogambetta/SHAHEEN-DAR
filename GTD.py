import pandas as pd

class gtd:
    def __init__(self, filename=None, seismic_timestamp= None):
        self.Filename = filename
        self._projection = None
        self._zone = None
        self._data = {}
        self._encoding = {}
        self._seismictimestamp = seismic_timestamp
        self.Dataframe = None
        self._parse()

    def _parse(self):
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
        self._encoding['INDEX'] = None
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
                    elif j in ['INDEX']:
                        timestamp = float(self._data['SHOT EPOCH'][-1])
                        self._data['INDEX'].append((self._seismictimestamp[self._seismictimestamp.ge(timestamp)].index[0]))  # index corresponding to picked event

        self._data.pop('RECORD CODE')
        self.Dataframe = pd.DataFrame.from_dict(self._data)
