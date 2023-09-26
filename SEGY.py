from obspy import Trace, Stream, UTCDateTime
from obspy.core import AttribDict
from obspy.io.segy.segy import SEGYTraceHeader, SEGYBinaryFileHeader
import numpy as np

class segy:
    def __init__(self, filename=None):
        self.Filename = filename
        self.st = Stream() #SEGY stream
        self.seismic = None
        self.geometry = None
        self.configuration = None

        self.samples_before_event = 500
        self.trace_samples = 5000
        self.sf = 1000 #sampling rate [Hz]

    def _set_sf(self):
        self.sf = int(1.0/(self.seismic.Dataframe['Timestamp'].iloc[1] - self.seismic.Dataframe['Timestamp'].iloc[0]))

    def set_configuration(self, v):
        self.configuration = v
        self.samples_before_event = int(self.configuration ['SEGY_samples_before_event'])
        self.trace_samples = int(self.configuration ['SEGY_trace_samples'])
    def set_geometry(self,v):
        self.geometry = v
    def set_seismic(self,v):
        self.seismic = v
        self._set_sf()

    def create(self):
        print('|{0:^5s}|{1:^8s}|{2:^28s}|{3:^28s}|{4:^28s}|'.format('-'*5,'-'*8, '-'*28, '-'*28, '-'*28))
        print('|{0:^5s}|{1:^8s}|{2:^28s}|{3:^28s}|{4:^28s}|'.format('#','SPNB', 'START DATETIME', 'END DATETIME', 'SHOT DATETIME'))
        print('|{0:^5s}|{1:^8s}|{2:^28s}|{3:^28s}|{4:^28s}|'.format('-'*5,'-'*8, '-'*28, '-'*28, '-'*28))
        #slice Dataframe to get the data for the single trace
        for j, idx in enumerate(map(int,self.geometry.Dataframe['Expected_FB_Index'])):
            print('Adding shot              '+str(j)+' @ '+str(idx) , end="\r", flush=True)
            _ini = idx-self.samples_before_event
            _end = _ini+self.trace_samples
            indices = list(range(_ini, _end))
            slc = self.seismic.Dataframe.take(indices)                                     # slice of seismic dataframe corresponding to the wanted trace
            print('|{0:^5d}|{1:^8d}|{2:^28s}|{3:^28s}|{4:^28s}|'.format(j,
                                                             self.geometry.Dataframe['SPNB'][j],
                                                             str(UTCDateTime(slc['Timestamp'].iloc[0])),
                                                             str(UTCDateTime(slc['Timestamp'].iloc[-1])),
                                                             str(UTCDateTime(self.seismic.Dataframe['Timestamp'].iloc[idx]))))
            _y = np.asarray(slc[['Channel0','Channel1','Channel2','Channel3','TILT_X','TILT_Y','TILT_Z']])  # actual trace data
            for i, c in enumerate(['Channel0','Channel1','Channel2','Channel3','TILT_X','TILT_Y','TILT_Z']):
                y = _y[:, i]
                atrace = Trace(data=np.asarray(y, dtype=np.float32))
                atrace.stats.delta = slc['Timestamp'].iloc[1] - slc['Timestamp'].iloc[0]
                atrace.stats.starttime = UTCDateTime(slc['Timestamp'].iloc[0])
                if not hasattr(atrace.stats, 'segy.trace_header'):
                    atrace.stats.segy = {}
                atrace.stats.segy.trace_header = SEGYTraceHeader()
                atrace.stats.segy.trace_header.energy_source_point_number = self.geometry.Dataframe['SPNB'][j]
                atrace.stats.segy.trace_header.trace_identification_code = int(i)
                atrace.stats.segy.trace_header.group_coordinate_x = int(float(self.geometry.Dataframe['RECEIVER X [EASTING]'][j]))
                atrace.stats.segy.trace_header.group_coordinate_y = int(float(self.geometry.Dataframe['RECEIVER Y [NORTHING]'][j]))
                atrace.stats.segy.trace_header.source_coordinate_x = int(float(self.geometry.Dataframe['SHOT X [EASTING]'][j]))
                atrace.stats.segy.trace_header.source_coordinate_y = int(float(self.geometry.Dataframe['SHOT Y [NORTHING]'][j]))
                if i in [0, 1, 2]:
                    mu = 0
                elif i == 3:
                    mu = 1
                atrace.stats.segy.trace_header.trace_value_measurement_unit = int(mu)
                atrace.stats.segy.trace_header.datum_elevation_at_source = int(self.geometry.Dataframe['WATER BOTTOM'][j] * 100)
                atrace.stats.segy.trace_header.water_depth_at_source = int(self.geometry.Dataframe['SHOT Z [DEPTH]'][j] * 100)
                atrace.stats.segy.trace_header.water_depth_at_group = int(self.geometry.Dataframe['RECEIVER Z [DEPTH]'][j] * 100)
                atrace.stats.segy.trace_header.scalar_to_be_applied_to_all_elevations_and_depths = int(self.geometry.Dataframe['GUN PRESSURE'][j])
                ai = str(self.geometry.Dataframe['SHOT EPOCH'][j]).strip().split('.')[0]
                bi = str(self.geometry.Dataframe['SHOT EPOCH'][j]).strip().split('.')[1]
                atrace.stats.segy.trace_header.ensemble_number = int(ai)
                atrace.stats.segy.trace_header.trace_number_within_the_ensemble = int(bi)
                atrace.stats.segy.trace_header.number_of_vertically_summed_traces_yielding_this_trace = self.seismic.Attributes['Board Serial Number']
                self.st.append(atrace)
        print('|{0:^5s}|{1:^8s}|{2:^28s}|{3:^28s}|{4:^28s}|'.format('-' * 5, '-' * 8, '-' * 28, '-' * 28, '-' * 28))
        self.st.stats = AttribDict()
        #    0         1         2         3         4         5         6         7
        #    01234567890123456789012345678901234567890123456789012345678901234567890123456789
        h =  'C1  GRAALTECH s.r.l.'.ljust(80,' ')
        h += 'C2  SEGY created with DAR_TOOLKIT rev.10'.ljust(80,' ')
        h += 'C3  Author: M.Gambetta [marco.gambetta@gmail.com]'.ljust(80, ' ')
        s= 'C4  Coordinate system - Projection '+self.geometry._projection +', Zone '+self.geometry._zone
        h += s.ljust(80, ' ')
        h += 'C5  Trace units : 0 = mm/s, 1 = microbar'.ljust(80, ' ')
        h += 'C6  Source Pressure units : PSI'.ljust(80, ' ')
        h += 'C7  Depth  units : m/100 '.ljust(80, ' ')
        s = 'C8  Geophone scalar ' + str(self.seismic.Attributes['geophone_scalar'])
        h += s.ljust(80, ' ')
        s = 'C9  Hydrophone scalar ' + str(self.seismic.Attributes['hydrophone_scalar'])
        h += s.ljust(80, ' ')
        s = 'C10  Geophone gain ' + str(self.seismic.Attributes['geophone_gain'])
        h += s.ljust(80, ' ')
        s = 'C11  Hydrophone scalar ' + str(self.seismic.Attributes['hydrophone_gain'])
        h += s.ljust(80, ' ')

        self.st.stats.textual_file_header = h
        self.st.stats.binary_file_header = SEGYBinaryFileHeader()
        self.st.stats.binary_file_header.trace_sorting_code = 5
        ix = int(self.geometry.Dataframe['Expected_FB_Index'].iloc[0])
        ex= int(self.geometry.Dataframe['Expected_FB_Index'].iloc[-1])

        s = str(UTCDateTime(self.seismic.Dataframe['Timestamp'].iloc[ix]))+'_'+str(UTCDateTime(self.seismic.Dataframe['Timestamp'].iloc[ex]))
        self.Filename = str(self.seismic.Attributes['Board Serial Number'])+'_'+s.replace(':','-')+'.SGY'
        print('\n{0:>38s} :{1:8d}'.format('Samples before shot time', self.samples_before_event))
        print('{0:>38s} :{1:8d}'.format('Trace samples', self.trace_samples))
        print('{0:>38s} :{1:80s}\n'.format('Output', self.Filename))
        self.st.write(self.Filename, format="SEGY", data_encoding=1)


