import multiprocessing as mup
import main_unicorn as upc
import main_psychopy as psy_ui
import os
import time

# SET UP
# pip install --upgrade --upgrade-strategy only-if-needed pyglet==1.5.26
# 1) link device (download unicorn software, access licenses, then get the python library link, and put it in the file)
# 2) download python 3.9.10 amd64 from https://www.python.org/ftp/python/3.9.10/
#     https://www.python.org/ftp/python/3.6.8/
# 3) get the local direction to this python version and put it in the venv creating step
#  C:\Users\luisf\AppData\Local\Programs\Python\Python39\python.exe -m venv venv39
# 4) pip install psychopy

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# --- Parameters ---
subject_id = "test_subject_ac_demo"
resources_path = 'C:/Users/luisf/git_projects/unicorn_v2/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/resources/'  # Path to the arithmetic QUESTIONS
results_path = 'C:/Users/luisf/git_projects/unicorn_v2/Neuro_Engineering_Dev/neuro_education/unicorn_hybrid_black/results/' # Path to save the data
execution_mode = 'dev' # 'dev' or 'prod'
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


def check_path(path: str, overwrite: bool):
    if os.path.exists(f'{path}'):
        if not overwrite:
            raise FileExistsError(f"Error: The path '{path}' already exists.")
        else:
            print(f"Warning: The path '{path}' exists, but continuing as overwrite is allowed.")
    else:
        print(f"The path '{path}' does not exist. Creating it now.")
        os.makedirs(path, exist_ok=True)



if __name__ == '__main__':
    
    with open("psychopy closed.txt", "w") as file:
            file.write("0")
    
    if (execution_mode == "dev") | (execution_mode == "prod") | (execution_mode == "demo"):
        try:
            check_path(f'{results_path}/{subject_id}/', overwrite=(execution_mode=='dev'))
        except FileExistsError as e:
            print(e)
            exit(1)
    else:
        print("ERROR: PLEASE USE A VALID EXECUTION TYPE")
        with open("psychopy closed.txt", "w") as psychopy_flag_file:
            psychopy_flag_file.write("1")
        exit(1)

    # Create a shared value for synchronized start time
    start_time = mup.Value("d", 0.0)

    # Start the Unicorn acquisition in a separate process
    p1 = mup.Process(target=upc.unicorn_process, args=(subject_id, 
                                                       results_path,
                                                       start_time))
    p2 = mup.Process(target=psy_ui.psychopy_process, args=(subject_id,
                                                           resources_path,
                                                           results_path,
                                                           start_time,
                                                           execution_mode))
    
    p1.start()
    p2.start()

    # Set the reference start time
    time.sleep(10)  # Ensure processes are ready
    start_time.value = time.time()

    print('Synchronization time passed\n')

    # Ensure Unicorn acquisition process ends
    p1.join()
    p2.join()

    print("\nProcesses finished.")