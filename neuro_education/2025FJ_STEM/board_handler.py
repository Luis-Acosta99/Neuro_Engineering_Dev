######### import libraries #########
####################################
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np

class brainflow_board_object():
    def __init__(self):
        # Set up parameters for Cyton board
        params = BrainFlowInputParams()
        params.serial_port = 'COM5'  # Update this with your Cyton board's serial port (you can see it in the openBCI GUI)
        
        # Initialize the board instance
        btype = "cyton"
        if btype == "cyton":
            board_id = BoardIds.CYTON_DAISY_BOARD.value
        else:
            board_id = BoardIds.SYNTHETIC_BOARD
        file_name = input("Please enter the file name with which the session will be saved (including extension .csv): \n")#"synthetic_data.csv"
        self.file = open(file_name, "w")

        # Connect to the board
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        # Start streaming data
        self.board.start_stream()
        self.confirm_connection()

        self.signal = np.empty((1, 1));

    def confirm_connection(self):
        if self.board.is_prepared():
            print("Connection to Cyton board established successfully!")
        else:
            print("Failed to establish connection to Cyton board.")

    def close_board(self):
        # stop streaming and disconnect from the board so a new session can be started without having to turn it on and off.
        self.file.close()
        self.board.stop_stream()
        self.board.release_session()
        print("Session ended")

    def get_signal(self):
        # cyton daisy returns a [32, 125 p/second] nd array 
        self.signal = np.transpose(self.board.get_board_data());
        np.savetxt(self.file, self.signal, delimiter=",") 
        
        # print statement for debugging purposes
        #print(self.session_samples,self.signal.shape)
        try:
            return (self.signal.shape[0] ,self.signal[-1][1:9]) #self.signal[0][1:9])
        except:
            return(60,[0,0,0,0,0,0,0,0])
        '''{'accel_channels': [17, 18, 19],
            'analog_channels': [27, 28, 29],
            'ecg_channels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            'eeg_channels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            'eeg_names': 'Fp1,Fp2,C3,C4,P7,P8,O1,O2,F7,F8,F3,F4,T7,T8,P3,P4',
            'emg_channels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            'eog_channels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            'marker_channel': 31,
            'name': 'CytonDaisy',
            'num_rows': 32,
            'other_channels': [20, 21, 22, 23, 24, 25, 26],
            'package_num_channel': 0,
            'sampling_rate': 125,
            'timestamp_channel': 30}'''
