from multiprocessing import Process
import os
import unicorn_ne as up
from psychopy import visual, core, gui, event
import pandas as pd
import random
import os
import psychopy_ne as psy_ui

# SET UP
# pip install --upgrade --upgrade-strategy only-if-needed pyglet==1.5.26
# 1) link device (download unicorn software, access licenses, then get the python library link, and put it in the file)
# 2) download python 3.9.10 amd64 from https://www.python.org/ftp/python/3.9.10/
#     https://www.python.org/ftp/python/3.6.8/
# 3) get the local direction to this python version and put it in the venv creating step
#  C:\Users\luisf\AppData\Local\Programs\Python\Python39\python.exe -m venv venv39
#  C:\Users\luisf\AppData\Local\Programs\Python\Python36\python.exe -m venv venv36
# 4) pip install psychopy


# --- Parameters ---
# --- Parameters ---
IMAGE_DURATION = 2  # Initial image duration (seconds) BASAL
TRIAL_DURATION_ARITHMETIC = 5  # Duration for each arithmetic cycle (seconds)
BREAK_DURATION = 2  # Duration of the break between arithmetic cycles (seconds)
NUM_CYCLES = 4  # Number of cycles arithmetic cycles
MATH_QUESTION_CSV = 'C:/Users/luisf/git_projects/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/math_test.csv'  # Path to the arithmetic QUESTIONS
DISPLAY_IMAGE_PATH = 'C:/Users/luisf/git_projects/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/image_bank/1x/estado_basal.png'  # Path to the initial image BASAL
CYCLE_TYPES = ['add', 'substraction', 'multiplication', 'division']  # Order of question types for Arithmetic cycles
PROGRAMMING_CSV = 'C:/Users/luisf/git_projects/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/coding_questions.csv'  # Path to the programming questions CSV file
PROGRAMMING_DURATION = 15  # Duration for the programming cycle (seconds)
TRIAL_DURATION_SA = 15  # Duration for each trial cycle (seconds) for Spatial abilities cycle 
SA_QUESTION_CSV = 'C:/Users/luisf/git_projects/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/sa.csv'  # Path to the SA questions CSV
device_number = 0
image_bank_path = 'C:/Users/luisf/git_projects/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/image_bank/1x/'

""" 
p1 = Process(target=calculate_squares, args=(first_half,))
p2 = Process(target=calculate_squares, args=(second_half,))

p1.start()
p2.start() """

def unicorn_process(device_number=device_number):
    unicorn_tec = up.unicorn_device("subject1")
    unicorn_tec.get_port_id(device_number)
    unicorn_tec.unicorn_connect()
    unicorn_tec.unicorn_stream()
    unicorn_tec.unicorn_disconnect()

def ui_process():
    # --- Main Script ---
    info = {'Participant ID': ''}
    dlg = gui.DlgFromDict(info)
    if not dlg.OK or not info['Participant ID']:
        core.quit()
    participant_id = info['Participant ID']

    win = visual.Window(fullscr=True, size=(1440, 900), color='black') #window specifications

    all_arithmetic_responses = []  # To store all arithmetic responses
    programming_responses = []     # To store all programming responses
    sa_responses = []  # To store all SA responses

    try:
        psy_ui.log_message("Starting experiment.")

        # Step 1: Display initial image BASAL
        psy_ui.display_image(DISPLAY_IMAGE_PATH, IMAGE_DURATION)
        # Step 2: arithmetic cycle display function
        all_arithmetic_responses = psy_ui.arithmetic_questions_flow(MATH_QUESTION_CSV, NUM_CYCLES, TRIAL_DURATION_ARITHMETIC, BREAK_DURATION, CYCLE_TYPES, participant_id)
        # Step 3: programming cycle display function
        programming_responses = psy_ui.programming_questions_flow(PROGRAMMING_CSV, PROGRAMMING_DURATION)
        # Step 4: programming cycle display function
        sa_responses = psy_ui.spatial_abilities_flow(image_bank_path, SA_QUESTION_CSV, TRIAL_DURATION_SA)

        # Save all responses
        psy_ui.save_data(all_arithmetic_responses, participant_id, 'arithmetic')
        psy_ui.save_data(programming_responses, participant_id, 'programming')
        psy_ui.save_data(sa_responses, participant_id, "spatial_abilities")
    except Exception as e:
        psy_ui.log_message(f"Unhandled error: {e}")
    finally:
        win.close()
        core.quit()
    

if __name__ == '__main__':
    p1 = Process(target=unicorn_process, args=())
    p2 = Process(target=ui_process, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()

