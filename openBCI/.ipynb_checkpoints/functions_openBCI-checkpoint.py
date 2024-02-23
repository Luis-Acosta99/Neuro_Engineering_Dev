from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def connect_to_cyton():
    # Set up parameters for Cyton board
    params = BrainFlowInputParams()
    params.serial_port = 'COM5'  # Update this with your Cyton board's serial port (you can see it in the openBCI GUI)

    # Initialize the board
    board_id = BoardIds.CYTON_DAISY_BOARD.value

    # Connect to the board
    board = BoardShim(board_id, params)
    board.prepare_session()
    
    # Start streaming data
    board.start_stream()
    
    return board

# Step 4: Confirm the connection
def confirm_connection(board):
    if board.is_prepared():
        print("Connection to Cyton board established successfully!")
    else:
        print("Failed to establish connection to Cyton board.")

# Main function to execute the connection
def main():
    board = connect_to_cyton()
    confirm_connection(board)
    
    #
    print(board.get_board_id())
    
    # 
    board.stop_stream()
    board.release_session()