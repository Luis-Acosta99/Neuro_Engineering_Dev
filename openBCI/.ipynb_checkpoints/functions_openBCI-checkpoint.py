######### import libraries #########
####################################
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np

######### Manage CYTON #########
####################################
def connect_to_cyton(btype):
    # Set up parameters for Cyton board
	params = BrainFlowInputParams()
	params.serial_port = 'COM5'  # Update this with your Cyton board's serial port (you can see it in the openBCI GUI)
	# Initialize the board instance
	if btype == "cyton":
		board_id = BoardIds.CYTON_DAISY_BOARD.value
	else:
		board_id = BoardIds.SYNTHETIC_BOARD
	# Connect to the board
	board = BoardShim(board_id, params)
	board.prepare_session()
	return board

# Main function to execute the connection
def open_board(btype="cyton"):
	board = connect_to_cyton(btype)
	# Start streaming data
	board.start_stream()
	confirm_connection(board)
	return board

def confirm_connection(board):
	if board.is_prepared():
		print("Connection to Cyton board established successfully!")
	else:
		print("Failed to establish connection to Cyton board.")

def close_board(board):
	# stop streaming and disconnect from the board so a new session can be started without having to turn it on and off.
	board.stop_stream()
	board.release_session()
	print("Session ended")

######### Manage DATA #########
####################################
def signal_acquisition(board):
	while True:
		buffer_data = board.get_board_data()
		height, width = buffer_data.shape
		print("Height of the array:", height)
		print("Width of the array:", width)
		time.sleep(2)
	return buffer_data

