import sys
# path to where the python api is stored on your local machine
sys.path.append( "C:/Users/luisf/Documents/gtec/Unicorn Suite/Hybrid Black/Unicorn Python/Lib")
import UnicornPy

class unicorn_device():
    def __init__(self, file_name:str):
        # Specifications for the data acquisition.
        #-------------------------------------------------------------------------------------
        self.TestsignaleEnabled = False;
        self.FrameLength = 1;
        self.AcquisitionDurationInSeconds = 10;
        self.DataFile = f"{file_name}.csv";
        pass

    def get_port_id(self):
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
        deviceID = int(input("Select device by ID #"))
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
        file = open(self.DataFile, "wb")
        #close file
        file.close()

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

    def unicorn_disconnect(self):
        # Close device.
        #-------------------------------------------------------------------------------------
        del self.device
        print("Disconnected from Unicorn")


        
        

unicorn_tec = unicorn_device("subject1")
unicorn_tec.get_port_id()
unicorn_tec.unicorn_connect()
unicorn_tec.unicorn_stream()
unicorn_tec.unicorn_disconnect()
