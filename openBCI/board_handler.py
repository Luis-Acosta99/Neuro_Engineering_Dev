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
        btype = "other"
        if btype == "cyton":
            board_id = BoardIds.CYTON_DAISY_BOARD.value
        else:
            board_id = BoardIds.SYNTHETIC_BOARD

        # Connect to the board
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        # Start streaming data
        self.board.start_stream()
        self.confirm_connection()

        self.signal = np.empty((1, 16))

    def confirm_connection(self):
        if self.board.is_prepared():
            print("Connection to Cyton board established successfully!")
        else:
            print("Failed to establish connection to Cyton board.")

    def close_board(self):
        # stop streaming and disconnect from the board so a new session can be started without having to turn it on and off.
        self.board.stop_stream()
        self.board.release_session()
        print("Session ended")

    def get_signal(self):
        # cyton daisy returns a [32, 125 p/second] nd array 
        self.signal = self.board.get_board_data()
        file_name = "synthetic_data.csv"
        file = open(file_name, "w")
        np.savetxt(file, self.signal, delimiter=",")