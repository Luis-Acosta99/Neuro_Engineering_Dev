import sys
import time
import csv
# path to where the python api is stored on your local machine
sys.path.append( "C:/Users/luisf/Documents/gtec/Unicorn Suite/Hybrid Black/Unicorn Python/Lib")

import UnicornPy
import struct

class unicorn_device():
    def __init__(self, path:str):
        # Specifications for the data acquisition.
        #-------------------------------------------------------------------------------------
        self.TestsignaleEnabled = False;
        self.FrameLength = 1;
        self.path = path;
        self.DataFile = f"{path}eeg.csv";
        pass

    def get_port_id(self,device_number=0):
        # Get available device serials.
        deviceList = UnicornPy.GetAvailableDevices(True)

        if len(deviceList) <= 0 or deviceList is None:
            raise Exception("No device available.Please pair with a Unicorn first.")

        # Print available device serials.
        print("Available devices:")
        i = 0
        for device in deviceList:
            print("#%i %s" % (i,device))
            i+=1

        # Request device selection.
        print()
        print(deviceList[device_number])
        self.deviceId = deviceList[device_number]
    
    def unicorn_connect(self):
        # Open selected device.
        #-------------------------------------------------------------------------------------
        print()
        print("Trying to connect to '%s'." %self.deviceId)
        self.device = UnicornPy.Unicorn(self.deviceId)
        print("Connected to '%s'." %self.deviceId)
        print()

    def unicorn_stream(self, start_time):
        # Create a file to store data.
        eeg_results = open(self.DataFile, "w",encoding="utf-8")
        eeg_results.close()
        eeg_results = open(self.DataFile, "a",encoding="utf-8")
        
        # Initialize acquisition members.
        #-------------------------------------------------------------------------------------
        numberOfAcquiredChannels= self.device.GetNumberOfAcquiredChannels()
        configuration = self.device.GetConfiguration()

        # Print acquisition configuration
        print("Acquisition Configuration:")
        print("Sampling Rate: %i Hz" %UnicornPy.SamplingRate)
        print("Frame Length: %i" %self.FrameLength)
        print("Number Of Acquired Channels: %i" %numberOfAcquiredChannels)
        print()

        # Allocate memory for the acquisition buffer.
        self.receiveBufferBufferLength = self.FrameLength * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(self.receiveBufferBufferLength)

        try:
            # Start data acquisition.
            #-------------------------------------------------------------------------------------
            self.device.StartAcquisition(self.TestsignaleEnabled)
            print("Data acquisition started.")
        

            # Acquisition loop.
            #-------------------------------------------------------------------------------------
            psychopy_has_closed = 0

            while psychopy_has_closed == 0:
                # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
                self.device.GetData(self.FrameLength,receiveBuffer,self.receiveBufferBufferLength)

                # Convert bytearray to a list of numbers (assuming float32 data format)
                data_values = list(struct.unpack(f"{len(receiveBuffer)//4}f", receiveBuffer))

                # Convert to UTF-8 friendly format (e.g., CSV or space-separated values)
                data_reshaped = [data_values[i:i + numberOfAcquiredChannels] for i in range(0, len(data_values), numberOfAcquiredChannels)]
                data_reshaped = [row + [time.time() - start_time.value] for row in data_reshaped]
                for row in data_reshaped:
                    eeg_results.write(",".join(map(str, row)) + "\n")  # Write as CSV
                
                psychopy_flag_file =  open("psychopy closed.txt", "r")
                psychopy_has_closed = int(psychopy_flag_file.read().strip())
                                
                
            # Stop data acquisition.
            #-------------------------------------------------------------------------------------
            self.device.StopAcquisition();
            print()
            print("Data acquisition stopped.");

        except UnicornPy.DeviceException as e:
            print(e)
        except Exception as e:
            print("An unknown error occured. %s" %e)
        finally:
            # release receive allocated memory of receive buffer
            del receiveBuffer

            #close file
            eeg_results.close()
            print("File correctly written")

    def unicorn_disconnect(self):
        # Close device.
        #-------------------------------------------------------------------------------------
        del self.device
        print("Disconnected from Unicorn")

    def get_psychopy_status(self):
        status_file = open("psychopy closed.txt", "r")
        try:
            status = int(status_file.read().strip())
        except:
            status = 0
            print("EEG STOPED UPON EMPTY FLAG")
        return status

        

def unicorn_process(subject_id, results_path, start_time, debuging = False):

    if debuging == True:
        exit()

    unicorn_tec = unicorn_device(path= f'{results_path}/{subject_id}/')
    unicorn_tec.get_port_id()
    unicorn_tec.unicorn_connect()

    while start_time.value == 0:
        pass  # Wait for synchronization

    unicorn_tec.unicorn_stream(start_time)
    unicorn_tec.unicorn_disconnect()

