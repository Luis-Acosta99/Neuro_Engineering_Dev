from multiprocessing import Process
import os
import unicorn_connect as upc
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

# Modify `main` so that PsychoPy runs on the main thread
if __name__ == '__main__':
    # Start the Unicorn acquisition in a separate process
    p1 = Process(target=upc.unicorn_process, args=())
    p1.start()

    p2 = Process(target=psy_ui.psychopy_process, args=())
    p2.start()

    # Ensure Unicorn acquisition process ends
    p1.join()
    p2.join()