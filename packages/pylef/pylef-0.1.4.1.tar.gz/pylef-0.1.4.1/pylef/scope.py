#-*- coding: utf-8 -*-

""" Class for the Tektronics TBS1062 """

#################################
import visa   # interface with NI-Visa
import numpy  # module for array manipulation
import os   # module for general OS manipulation
import time # module for time related funtions
import pandas # module for general data analysis
################################
def read_only_properties(*attrs):
    """
        decorator to make some class variables read-only
        made by oz123 from   
        https://github.com/oz123/oz123.github.com/blob/master/media/uploads/readonly_properties.py
    """
    def class_rebuilder(cls):
        "The class decorator example"

        class NewClass(cls):
            "This is the overwritten class"
            def __setattr__(self, name, value):

                if name not in attrs:
                    pass
                elif name not in self.__dict__:
                    pass
                else:
                    raise AttributeError("Can't touch {}".format(name))

                super().__setattr__(name, value)

        return NewClass

    return class_rebuilder

@read_only_properties('id_tek', 'average_list', 'ch1', 'ch2', 'math')
class TektronixTBS1062:
    def __init__(self):
        """
            Classe para o osciloscópio
        """
        self.id_tek = '0x0699'; # identificador do fabricante TEK
        interface_name = self.find_interface()
        self.instr = visa.ResourceManager().open_resource(interface_name)   ## resource name
        self.ch1 = ChannelScope(self.instr, 'CH1')  # channel 1
        self.ch2 = ChannelScope(self.instr, 'CH2')   # channel 2
        self.math = ChannelScope(self.instr, 'MATH')   # channel 2
        self.trigger = Trigger(self.instr)
        self.average_list = [4, 16, 64, 128]
        ## VISA reading configurations
        self.instr.timeout = 10000 # set timeout to 10 seconds
        self.instr.chunk_size = 40960  # set the buffer size to 40 kB
        self.instr.write('Data:ENCDg SRI')  # set the instrument to read binary
        self.instr.write('Data:Width 1')   # set the data width to 1 byte
        self.instr.write('HEADER ON')   # set the header ON (needed)
        self.instr.values_format.is_binary = True
        self.instr.values_format.datatype = 'b'
        self.instr.values_format.is_big_endian = True
        self.instr.values_format.container = numpy.array    

    def find_interface(self):
        """ 
            Extract the interface name for the Tektronics scope
        """
        resources = visa.ResourceManager().list_resources()
        instr_n = len(resources)
        if instr_n == 0:
            raise ValueError('Nenhum instrumento foi identificado: \n Verique se estao' \
                             'ligados e se o cabo USB foi conectado. Se o problema persistir \n'\
                             'desconecte os cabos USB, aguarde 20 segundos e conecte novamente.')
        tek_str = ''
        for resource in resources:
            fab_id = resource.split('::')[1]
            if fab_id == self.id_tek:
                instr = visa.ResourceManager().open_resource(resource)
                instr.timeout = 10000 # set timeout to 10 seconds
                tek_str = instr.query('*IDN?')
                resource_out = resource
                print("Osciloscópio conectado! Id = " + tek_str[:-1])
        if tek_str == '':
            raise ValueError('O osciloscopio TEK 1062 nao foi identificado:\n'\
                         'Verique se o equipamento está ligado e se o cabo USB \n'\
                         'foi conectado. Se o problema persistir, \n'\
                         'desconecte o cabo USB, aguarde 20 segundos \n'\
                         'e conecte novamente.')
        return resource_out
#
####### Communications wraps    ########    
    def identify(self):
        """ identify the equipment """
        return self.instr.query('*IDN?')
#
    def clear(self):
        """ The the Data structures of the Scope """
        self.instr.write('*CLS')
        return None
#
    def wait(self):
        """ wait for the task to end """
        return self.instr.write('*WAI')
#
    def write(self, msg):
        """ write into the laser """
        write_output = self.instr.write(str(msg)) 
        self.wait()
        return write_output  
#
    def query(self, msg):
        """ query from the instrument """
        return self.instr.query(str(msg)) 
#
    def read(self):
        """ read from the instrument """
        return self.instr.read()
#
    def close(self):
        """ close the instrument """
        return self.instr.close()
######
    def set_average(self):
        """ start average acquisition """
        self.instr.write('ACQuire:MODe AVERAge')
        return None
#
    def set_sample(self):
        """ start sample acquisition """
        self.instr.write('ACQuire:MODe SAMPle')
        return None
#    
    def set_horizontal_scale(self, val):
        """ set horizontal scale """
        self.instr.write('HORizontal:MAIn:SCALE ' + str(val))
        return None
#    
    def horizontal_scale(self):
        return float(self.instr.query('HORizontal:MAIn:SCALE?').split(' ')[-1])
#
    def set_horizontal_position(self, val):
        """ set horizontal scale """
        self.instr.write('HORizontal:MAIn:POSition ' + str(val))
        return None
#
    def horizontal_position(self):
        return float(self.instr.query('HORizontal:MAIn:POSition?').split(' ')[-1])

##### commands ###########
    def aquisition_params(self):
        """ return the aquisition parameters  """
        return self.instr.query('ACQuire?').split(';')
#
    def cursor_params(self):
        """ return the cursos parameters  """
        return self.instr.query('CURSor?').split(';')
#    
    def average_number(self):
        """ return the number of waveforms used in the average """
        return int(self.instr.query('ACQuire:NUMAVg?').split(':')[-1].split(' ')[-1])
#
    def set_average_number(self, msg):
        """ set the number of waveforms used in the average """
        if int(msg) in self.average_list:                
            self.instr.write('ACQuire:NUMAVg %3d' % int(msg))   
            return None
        else: 
            raise ValueError("The number of waveforms must be one of " + ', '.join(['%3d' % l for l in self.average_list]))
#
    def get_active_channel(self):
        """ return the active channel for the waveform aquisition """
        return self.instr.query('DATa:SOUrce?').split(' ')[-1][:-1]             
#          
##### waveform reading commands #####
    def start_acquisition(self):
        """ start the aquisition of the waveform """
        return self.instr.write('ACQuire:STATE RUN')
#
    def stop_acquisition(self):
        """ stop the aquisition of the waveform """
        return self.instr.write('ACQuire:STATE STOP')

    
############## Saving functions ##### (They shouldn' t be here!!)
    def save_channels(self, name, header = ['time (s)', 'Channel 1 (V)', 'Channel 2 (V)'], PATH = '', extension = '.dat', sep = '\t', time_stamp = True):
        """ Saves on file the channels 1 and 2 as well as
        the time sweep
        
        Usage
        -----

            >>> import pylef.TektronixTBS1062 as scope
            >>> t, x, y = scope.save_channels('file_name', sep = ',')

        This code will save a file names 'file_name.dat' at 
        the working directory and with comma separation. You
        also use the arrays t, x and y to data processing and
        plotting. For example, the Lissajous figure can be 
        plotted as 

            >>> plt.plot(x, y)
            >>> plt.show()

        Parameters
        -----------
        name: string
            File name to be saved
        header: 3-parameter list - optional
            List with the name of the header for the 3 array-like 
            data in the format [time, channel 1, channel 2 ] 
        PATH: PATH-like string - optional 
            PATH for where the dada should be saved 
        extension: string - optional
            Extesions should be one of '.dat', '.csv', '.txt'
        sep: sting - optional
            Separator. Normally used are ',', '.', ' ', '\t'
        time_stamp: boolean
            Makes a time stamp file system and adds a time stamp 
            the end of each file
        Returns
        --------

        t, x, y = tuple 
            t: array-like time parameter
            x: array-like channel 1
            y: array-like channel 2
        
        """
##### reading and setting directory name
        t, x = self.ch1.read_channel()   # read channel 1
        t0, y = self.ch2.read_channel()   # read channel 2
###### name of the file        
        Npts = t.shape[0]
        indexh = range(Npts)
        df = pandas.DataFrame(columns = header, index = indexh)  # initialization of the filtered dataframe        
        df[header[0]] = t  # set the t variable
        df[header[1]] = x  # set the channel 1
        df[header[2]] = y  # set the channel 2
        ## time stamp and directory creation
        if time_stamp:
            dir_name = os.path.join(PATH,time.strftime('%Y_%m_%d', time.localtime(time.time()))) # set directory name
         # check the directory exist and create it automaticaly
            try: 
                os.makedirs(dir_name)     # make new directory unless it already exists
            except OSError:
                if not os.path.isdir(dir_name):
                    raise
            time_stamp_suf = time.strftime('_%H_%M_%S', time.localtime(time.time()))
            full_name = os.path.join(dir_name,name + time_stamp_suf)
        else: full_name = PATH + name    
        ## extension setting
        extension = extension.lower()  # set to lower case
        if extension not in ['.dat', '.csv', '.txt']:
            extension = '.dat'
            print("Your file will be saved as a '.dat'. The extension should be one of those: '.dat', '.csv' and '.txt'")
        df.to_csv(full_name + extension, sep = sep)  # save data
        print('... file => %s saved !!' % full_name)
        return t, x, y

##
@read_only_properties('instrument', 'channel', 'probe_list')
class ChannelScope:
    def __init__(self, instrument, channel):
        """ 
           Channel class for the oscilloscopes
        """
        self.instr = instrument  ## resource name
        self.channel = channel
        self.probe_list = [0.2, 1, 10, 20, 50, 100, 500, 1000]
        self.state_list = {"1": "on", "0": "off"} 
        self.measure = Measure(instrument, channel)  
#
    def state(self):
        """ check whether channel is on"""
        return  self.state_list[self.instr.query('SELECT:'+self.channel+'?').split(' ')[-1][0]]
#
    def turn_on(self):
        """ turn channel on"""
        self.instr.write('SELECT:'+self.channel+' ON')
        return  None
#
    def turn_off(self):
        """ turn channel off"""
        self.instr.write('SELECT:'+self.channel+' OFF')
#
    def set_scale(self, val):
        """ set channel scale """
        self.instr.write(self.channel  + ':SCALE ' + str(val))
        return None
#
    def scale(self):
        """ return channel scale """
        return float(self.instr.query(self.channel + ':SCALE?').split(' ')[-1])
#
    def set_position(self, val):
        """ set channel position """
        self.instr.write(self.channel  + ':POSITION ' + str(val))
        return None
#
    def position(self):
        """ return channel position """
        return float(self.instr.query(self.channel + ':POSITION?').split(' ')[-1])
#
    def set_bandwidth_on(self, val):
        """ set channel bandwidth ON """
        self.instr.write(self.channel  + ':BANDWIDth ON')
        return None
#
    def set_bandwidth_off(self, val):
        """ set channel bandwidth OFF """
        self.instr.write(self.channel  + ':BANDWIDth OFF')
        return None
#
    def set_invert_on(self):
        """ set channel invert ON """
        self.instr.write(self.channel  + ':INVERT ON')
        return None
#
    def set_invert_off(self):
        """ set channel invert OFF """
        self.instr.write(self.channel  + ':INVERT OFF')
        return None
#
    def set_ac(self):
        """ set channel coupling to AC """
        self.instr.write(self.channel  + ':COUPLING AC')
        return None
#
    def set_dc(self):
        """ set channel coupling to DC """
        self.instr.write(self.channel  + ':COUPLING DC')
        return None
#
    def set_ground(self):
        """ set channel coupling to DC """
        self.instr.write(self.channel  + ':COUPLING GND')
        return None    
#
    def coupling(self):
        """ return channel coupling """
        return self.instr.query(self.channel + ':COUPLING?')[:-1].split(' ')[-1]   
#
    def set_probe(self, val):
        """ set oscilloscope probe """
        if val in self.probe_list:
            self.instr.write(self.channel  + ':PROBE ' + str(val))
        else: 
            raise ValueError("The probes must be one of " + ', '.join(['%3d' % l for l in self.probe_list]))        
        return None
#
    def probe(self):
        """ return oscilloscope scale """
        return float(self.instr.query(self.channel + ':PROBE?').split(' ')[-1])
#
    def read_preface(self):
        """ return a list with the praface parameters  """
        return self.instr.query('WFMPRe?').split(':')[-1].split(',')  # read the preface and convert into a list
#
    def waveform_conversion(self):
        """ return the waveform convertion values in the form
        "[[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]" """
        temp = self.read_preface()[-1].split(';')   # read the 6 position of the preface and convert into a list
        temp = [x.split(' ') for x in temp]   
        for test in temp:
            if test[0] == 'XZERO': x_zero = float(test[1])
            if test[0] == 'XINCR': x_factor = float(test[1])
            if test[0] == 'PT_OFF': x_offset = float(test[1])
            if test[0] == 'YZERO': y_zero = float(test[1])
            if test[0] == 'YMULT': y_factor = float(test[1])
            if test[0] == 'YOFF': y_offset = float(test[1])        
        return [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]
#
    def waveform_conversion_no_header(self):
        """ return the waveform convertion values in the form
        "[[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]" """
        temp = self.read_preface()[-1].split(';')   # read the 6 position of the preface and convert into a list
        
        x_factor, x_offset, x_zero = float(temp[2]), float(temp[3]), float(temp[4]) 
        y_factor, y_offset, y_zero = float(temp[6]), float(temp[8]), float(temp[7])  #indices 7 and 8 are right! 
        return [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]   
#
    def set_dynamic_scale(self):
        """ dynamically scales the oscilloscope to the measurement. Only works if the offset is correct """
        keep_loop = True
        while keep_loop:
            Vpp = self.measure.Vpp()
            if Vpp > 9*self.scale(): self.set_scale(Vpp)
            else:
                keep_loop = False
                self.set_scale(Vpp/7.)
        return None
#
    def set_smart_scale(self, log_step = 10, Vmax = 4., D = 0.75):
        """ dynamically scales the oscilloscope to the measurement. """
        #test whether channel is on
        if self.state() == 'off':
            raise ValueError('O canal %s do osciloscópio está desligado!' % self.channel)
        keep_loop = True
        while keep_loop:
            scale, pos_div = self.scale(), self.position()
            max0, min0 = self.measure.maximum(), self.measure.minimum()
            pos_top, pos_bot = (Vmax - pos_div)*scale, (-Vmax - pos_div)*scale
            if max0 >= pos_top or min0 <= pos_bot:  # rescale until one of them comes into the scale 
                self.set_position(pos_div/log_step)
                self.set_scale(log_step*scale)
            else:
                eta = (max0 + min0)/(max0 - min0)
                new_pos, new_scale = -eta*(Vmax - D), max0/((1. + eta)*(Vmax - D))
                self.set_position(new_pos)    
                self.set_scale(new_scale)
                keep_loop = False
        return None
#
    def acquire_y_raw_ascii(self):
        """acquire the raw curve of whatever channel is set in "set_channel" """
        return numpy.array(self.instr.query('CURVe?').split(' ')[-1].split(','), float)
#
    def acquire_y_raw(self):
        """acquire the raw curve of whatever channel is set in "set_channel" """
        return numpy.array(self.instr.query_values('CURVe?'))
#
    def read_channel(self):
        """ returns a tuple with both the x and y axis already converted. It creates the x axis and reads the y axis from the channel set with the function "set_channel". The y acquisition is done using the function "acquire_y_raw" the converting factor by using the "waveform_conversion" function """
        self.instr.write('DATa:SOUrce ' + self.channel)  # set channel to active
        y_raw = self.acquire_y_raw()    # acquire y raw curve
        [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]] = self.waveform_conversion()
        x_raw = numpy.arange(len(y_raw))        
        x = x_zero + x_factor*(x_raw - x_offset)
        y = y_zero + y_factor*(y_raw - y_offset)
        return (x, y)
#    
# subclass with the measurements     
class Measure:
    def __init__(self, instrument, source):
        # instrument initialization
        """ Make the all measure"""
        self.instr = instrument   ## resource name
        self.source = source   # source variable
#        
    def do_measure_no_header(self, prop):
        """measure the property on channel """
        self.instr.write('MEASUREMENT:IMMED:TYPE ' + prop)
        self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)
        if prop.lower() == 'phase':
            self.instr.write('MEASUREMENT:IMMED:Source2 CH1')                        
            self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)         
        return float(self.instr.query('MEASUREMENT:IMMED:Value?'))
#        
    def do_measure(self, prop):
        """measure the property on channel """
        self.instr.write('MEASUREMENT:IMMED:TYPE ' + prop)
        self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)
        if prop.lower() == 'phase':
            self.instr.write('MEASUREMENT:IMMED:Source2 CH1')                        
            self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)
            output = float(self.instr.query('MEASUREMENT:IMMED:Value?').split(' ')[-1])
            if output == 9.9e37:
                output = float('nan')
        else:
            output = float(self.instr.query('MEASUREMENT:IMMED:Value?').split(' ')[-1])
        return output
#
    def phase(self):
        """measure the phase """
        return float(self.do_measure('PHASE'))
    def Vpp(self):
        """measure the peak-to-peak voltage """
        return float(self.do_measure('PK2PK'))
    def frequency(self):
        """measure the frequency in Hz """
        return float(self.do_measure('FREQ'))
    def period(self):
        """measure the period in s """
        return float(self.do_measure('PERIOd'))
    def mean(self):
        """measure the average value """
        return float(self.do_measure('MEAN'))
    def cycle_rms(self):
        """measure the RMS voltage in one period in V """
        return float(self.do_measure('CRMS'))
    def rms(self):
        """measure the RMS voltage in the screen in V """
        return float(self.do_measure('RMS'))
    def maximum(self):
        """measure the maximum voltage in one period in V """
        return float(self.do_measure('MAXImum'))
    def minimum(self):
        """measure the minimum voltage in the screen in V """
        return float(self.do_measure('MINImum'))    

@read_only_properties('instrument', 'trigger_list')
class Trigger:
    def __init__(self, instrument):
        """ 
           Channel class for the oscilloscope trigger
        """
        self.instr = instrument  ## resource name
        self.trigger_list = ['CH1', 'CH2', 'EXT', 'EXT5', 'EXT10', 'AC LINE']
        self.coupling_list = ['AC', 'DC', 'HFRej', 'LFRej', 'NOISErej']

    def state(self):
        """ return the trigger state """
        return self.instr.query('TRIGGER:STATE?')[:-1]
#
    def set_source(self, source):
        """ set trigger source"""
        source = source.upper()  # set the word to upper case
        if source in self.trigger_list:
            self.instr.write('TRIGGER:MAIN:EDGE:SOURCe ' + source)
        else:
            raise ValueError('The trigger should be one of those: ' + ', '.join([l for l in self.trigger_list]))
#
    def source(self):
        """ return the trigger level"""
        return self.instr.query('TRIGGER:MAIN:EDGE:SOURCe?')[:-1].split(' ')[-1]
#
    def set_level(self, val):
        """ set trigger level"""
        self.instr.write('TRIGGER:MAIN:LEVEL ' + str(val))
#
    def level(self):
        return float(self.instr.query('TRIGGER:MAIN:LEVEL?').split()[-1])
#
    def set_to_50(self):
        """ set trigger level to 50 % """
        self.instr.write('TRIGGER:MAIN SETLevel')
#
    def set_slope_fall(self):
        """ set trigger slope fall """
        self.instr.write('TRIGGER:MAIN:EDGE:SLOPE FALL')
#
    def set_slope_rise(self):
        """ set trigger slope rise """
        self.instr.write('TRIGGER:MAIN:EDGE:SLOPE RISE')
#
    def slope(self):
        return self.instr.query('TRIGGER:MAIN:EDGE:SLOPE?')[:-1]     
#
    def set_coupling(self, val):
        """ set trigger coupling """
        source = source.upper()  # set the word to upper case
        if source in self.trigger_list:
            self.instr.write('TRIGGER:MAIN:EDGE:COUPLing ' + source)
        else:
            raise ValueError('The trigger coupling should be one of those: ' + ', '.join([l for l in self.coupling_list]))
#
    def coupling(self):
        return self.instr.query('TRIGGER:MAIN:EDGE:COUPLING?')[:-1]

