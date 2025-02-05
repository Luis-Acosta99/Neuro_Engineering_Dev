import sys
# path to where the python api is stored on your local machine
sys.path.append( "C:/Users/luisf/Documents/gtec/Unicorn Suite/Hybrid Black/Unicorn Python/Lib")
import UnicornPy
import struct

class unicorn_device():
    def __init__(self, file_name:str):
        # Specifications for the data acquisition.
        #-------------------------------------------------------------------------------------
        self.TestsignaleEnabled = False;
        self.FrameLength = 1;
        self.AcquisitionDurationInSeconds = 10;
        self.DataFile = f"{file_name}.csv";
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
        deviceID = int(device_number)
        if deviceID < 0 or deviceID > len(deviceList):
            raise IndexError('The selected device ID is not valid.')
        
        self.deviceId = deviceList[deviceID]
    
    def unicorn_connect(self):
        # Open selected device.
        #-------------------------------------------------------------------------------------
        print()
        print("Trying to connect to '%s'." %self.deviceId)
        self.device = UnicornPy.Unicorn(self.deviceId)
        print("Connected to '%s'." %self.deviceId)
        print()

    def unicorn_stream(self):
        # Create a file to store data.
        file = open(self.DataFile, "w",encoding="utf-8")
        
        # Initialize acquisition members.
        #-------------------------------------------------------------------------------------
        numberOfAcquiredChannels= self.device.GetNumberOfAcquiredChannels()
        configuration = self.device.GetConfiguration()

        # Print acquisition configuration
        print("Acquisition Configuration:")
        print("Sampling Rate: %i Hz" %UnicornPy.SamplingRate)
        print("Frame Length: %i" %self.FrameLength)
        print("Number Of Acquired Channels: %i" %numberOfAcquiredChannels)
        print("Data Acquisition Length: %i s" %self.AcquisitionDurationInSeconds)
        print()

        # Allocate memory for the acquisition buffer.
        self.receiveBufferBufferLength = self.FrameLength * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(self.receiveBufferBufferLength)

        try:
            # Start data acquisition.
            #-------------------------------------------------------------------------------------
            self.device.StartAcquisition(self.TestsignaleEnabled)
            print("Data acquisition started.")

            # Calculate number of get data calls.
            numberOfGetDataCalls = int(self.AcquisitionDurationInSeconds * UnicornPy.SamplingRate / self.FrameLength);
        
            # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
            consoleUpdateRate = int((UnicornPy.SamplingRate / self.FrameLength) / 25.0);
            if consoleUpdateRate == 0:
                consoleUpdateRate = 1

            # Acquisition loop.
            #-------------------------------------------------------------------------------------
            for i in range (0,numberOfGetDataCalls):
                # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
                self.device.GetData(self.FrameLength,receiveBuffer,self.receiveBufferBufferLength)

                # Convert bytearray to a list of numbers (assuming float32 data format)
                data_values = list(struct.unpack(f"{len(receiveBuffer)//4}f", receiveBuffer))

                # Convert to UTF-8 friendly format (e.g., CSV or space-separated values)
                file.write(",".join(map(str, data_values)) + "\n")  # Write as CSV

                # Update console to indicate that the data acquisition is running.
                if i % consoleUpdateRate == 0:
                    print('.',end='',flush=True)

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
            file.close()
            print("File correctly written")

    def unicorn_disconnect(self):
        # Close device.
        #-------------------------------------------------------------------------------------
        del self.device
        print("Disconnected from Unicorn")

def unicorn_process(subject_id = "subject1", device_number=0):
    unicorn_tec = unicorn_device(subject_id)
    unicorn_tec.get_port_id(device_number)
    unicorn_tec.unicorn_connect()
    unicorn_tec.unicorn_stream()
    unicorn_tec.unicorn_disconnect()

if __name__ == '__main__':
    unicorn_process()