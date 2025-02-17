from psychopy import visual, core, gui, event
import pandas as pd
import random
import os
import time

# --- Helper Functions ---
def log_message(message):
    """Helper function to log messages for debugging."""
    print(f"[DEBUG]: {message}")

def save_data(data, subject_id,results_path, module_name):
    """Saves the collected data to a CSV file for a specific module."""
    if not data:
        log_message(f"No data to save for module: {module_name}")
        return

    if not os.path.exists('data'):
        os.makedirs('data')
    
    filename = f'{results_path}/{subject_id}/{module_name}_responses.csv'
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    log_message(f"Data saved to '{filename}'.")
# --- Function Definitions ---
def display_image(win, image_path, duration):
    """Displays an initial image for a set duration."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        image = visual.ImageStim(win, image=image_path)
        image.draw()
        win.flip()
        log_message(f"Displaying image for {duration} seconds.")
        core.wait(duration)
    except Exception as e:
        log_message(f"Error in 'display_image': {e}")

def display_questions(win, duration, cycle_number, cycle_type, question_list, global_start_time):
    """Displays arithmetic questions for a given cycle."""
    start_time = core.getTime()
    responses = []

    # Filter questions for the current cycle type
    filtered_questions = [q for q in question_list if q['type'].lower() == cycle_type.lower()]
    if not filtered_questions:
        log_message(f"No questions available for type '{cycle_type}'. Skipping cycle.")
        return responses

    while core.getTime() - start_time < duration:
        question = random.choice(filtered_questions)
        question_text = visual.TextStim(win, text=question['question'], font='Arial', color='white', height=0.1, wrapWidth=1.5)
        question_text.draw()
        win.flip()
        q_appearance = time.time() - global_start_time.value

        participant_answer = ''
        timer = core.CountdownTimer(duration - (core.getTime() - start_time))

        while timer.getTime() > 0:
            keys = event.waitKeys(keyList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'backspace', 'return', 'escape', '-', 'minus'],
                maxWait=timer.getTime()
            )
            if not keys:
                break

            for key in keys:
                if key == 'return':  # Save the answer
                    responses.append({
                        'ID': question['id'],
                        'Correct_Answer': question['c'],
                        'Participant_Answer': participant_answer,
                        'Question_appearance':q_appearance,
                        'Answer_time':time.time() - global_start_time.value
                    })
                    break
                elif key == 'escape':  # Exit the experiment
                    core.quit()
                elif key == 'backspace':  # Erase the last character
                    participant_answer = participant_answer[:-1]
                elif key.isdigit():  # Handle digits
                    participant_answer += key
                elif key in ['-', 'minus']:  # Add hyphen for negative numbers
                    participant_answer += '-'

            # Update the display with the participant's answer
            question_text.draw()
            answer_preview = visual.TextStim(win, text=participant_answer, color='yellow', height=0.08, pos=(0, -0.4))
            answer_preview.draw()
            win.flip()

            if 'return' in keys:
                break

        if timer.getTime() <= 0:
            log_message("Time expired for this question.")
            break

    return responses

def take_break(win, duration):
    """Displays a break screen."""
    break_text = visual.TextStim(win, text=f"Break for {duration} seconds.", color='white', height=0.1)
    break_text.draw()
    win.flip()
    core.wait(duration)

def display_programming_questions(win, duration, question_list,global_start_time):
    """Displays programming-related questions with a slider for rating."""
    start_time = core.getTime()
    responses = []

    # Shuffle questions
    random.shuffle(question_list)

    for question in question_list:
        if core.getTime() - start_time >= duration:
            log_message("Time expired for the programming cycle.")
            break

        question_text = visual.TextStim(win, text=question['question'], color='white', height=0.1, wrapWidth=1.5)
        slider = visual.Slider(
            win, ticks=[1, 2, 3, 4, 5], labels=['Nada', 'Muy Poco', 'Neutral', 'Mucho', 'Completamente'],
            granularity=1, style='rating', size=(1.0, 0.1), pos=(0, -0.3), color='White'
        )

        # Display question and slider
        while core.getTime() - start_time < duration:
            question_text.draw()
            slider.draw()
            win.flip()
            q_appearance = time.time() - global_start_time.value

            # Check if a response was made (slider rating)
            if slider.getRating() is not None:
                responses.append({
                    'ID': question['id'],
                    'Rating': slider.getRating(),
                    'Global_time':time.time() - global_start_time.value,
                    'Question_appearance':q_appearance,
                    'Answer_time':time.time() - global_start_time.value
                    })
                break  # Once the participant responds, break out of the loop for this question

            # Check if time is up for the current question
            if core.getTime() - start_time >= duration:
                log_message("Time expired for the programming cycle.")
                break

    return responses

def display_question_with_image_and_buttons(win, image_path, question_text, duration, question_id, global_start_time):
    """Displays an image and a question with clickable buttons, with click debouncing."""
    # Ensure the image retains its aspect ratio
    image = visual.ImageStim(win, image=image_path, pos=(0, 0), size=(0.6, 0.6), units="height")

    # Question Text
    question = visual.TextStim(win, text=question_text, pos=(0, 0.70), color='white', height=0.08, wrapWidth=1.5)

    # Buttons (smaller size, all light-colored)
    button_color = 'lightgray'
    button_a = visual.Rect(win, width=0.2, height=0.1, pos=(-0.8, -0.8), fillColor=button_color)
    button_b = visual.Rect(win, width=0.2, height=0.1, pos=(-0.4, -0.8), fillColor=button_color)
    button_c = visual.Rect(win, width=0.2, height=0.1, pos=(0.4, -0.8), fillColor=button_color)
    button_d = visual.Rect(win, width=0.2, height=0.1, pos=(0.8, -0.8), fillColor=button_color)
    
    # Button labels
    text_a = visual.TextStim(win, text="A", pos=(-0.8, -0.8), color='black', height=0.04)
    text_b = visual.TextStim(win, text="B", pos=(-0.4, -0.8), color='black', height=0.04)
    text_c = visual.TextStim(win, text="C", pos=(0.4, -0.8), color='black', height=0.04)
    text_d = visual.TextStim(win, text="D", pos=(0.8, -0.8), color='black', height=0.04)

    # Mouse object for detecting clicks
    mouse = event.Mouse(visible=True, win=win)
    participant_answer = None
    responses = []

    start_time = core.getTime()
    while core.getTime() - start_time < duration:
        # Draw all elements
        image.draw()
        question.draw()
        button_a.draw()
        button_b.draw()
        button_c.draw()
        button_d.draw()
        text_a.draw()
        text_b.draw()
        text_c.draw()
        text_d.draw()
        win.flip()
        q_appearance = time.time() - global_start_time.value

        # Check for mouse clicks
        if mouse.isPressedIn(button_a):
            participant_answer = 'A'
            core.wait(0.5)  # Debounce delay
            break
        elif mouse.isPressedIn(button_b):
            participant_answer = 'B'
            core.wait(0.5)  # Debounce delay
            break
        elif mouse.isPressedIn(button_c):
            participant_answer = 'C'
            core.wait(0.5)  # Debounce delay
            break
        elif mouse.isPressedIn(button_d):
            participant_answer = 'D'
            core.wait(0.5)  # Debounce delay
            break

    if participant_answer:
        responses.append({
            'ID': question_id,
            'Participant_Answer': participant_answer,
            'Global_time':time.time() - global_start_time.value,
            'Question_appearance':q_appearance,
            'Answer_time':time.time() - global_start_time.value
                    })
    return responses

def arithmetic_questions_flow(win, math_csv, num_cycles, trial_duration, break_duration, cycle_types, global_start_time):
    """Handles the flow of displaying arithmetic questions."""
    responses = []
    if os.path.exists(math_csv):
        questions_df = pd.read_csv(math_csv)
        questions_list = questions_df.to_dict(orient='records')

        for cycle in range(num_cycles):
            cycle_type = cycle_types[cycle]  # Determine the cycle type
            log_message(f"Starting cycle {cycle + 1} with type '{cycle_type}'.")
            cycle_responses = display_questions(win, trial_duration, cycle + 1, cycle_type, questions_list, global_start_time)
            responses.extend(cycle_responses)

            if cycle < num_cycles - 1:  # Break after each cycle except the last one
                take_break(win, break_duration)
    else:
        log_message(f"Arithmetic questions CSV not found: {math_csv}")
    return responses

def programming_questions_flow(win, programming_csv, duration,global_start_time):
    """Handles the flow of displaying programming questions."""
    responses = []
    if os.path.exists(programming_csv):
        programming_df = pd.read_csv(programming_csv)
        programming_questions = programming_df.to_dict(orient='records')
        responses = display_programming_questions(win, duration, programming_questions,global_start_time)
    else:
        log_message(f"Programming CSV not found: {programming_csv}")
    return responses

def spatial_abilities_flow(win, image_bank_path, sa_csv, trial_duration,global_start_time):
    """Handles the flow of displaying spatial abilities questions."""
    responses = []
    if os.path.exists(sa_csv):
        questions_df = pd.read_csv(sa_csv)
        questions_list = questions_df.to_dict(orient='records')
        random.shuffle(questions_list)  # Randomize questions

        start_time = core.getTime()
        while core.getTime() - start_time < trial_duration and questions_list:
            question = questions_list.pop(0)  # Get the next question
            image_path = image_bank_path + question['image-name']
            response = display_question_with_image_and_buttons(win, image_path, question['question'], trial_duration, question['id'],global_start_time)
            responses.extend(response)

            if not questions_list:  # All questions answered, break out of the loop
                break
    else:
        log_message(f"SA questions CSV not found: {sa_csv}")
    return responses

def psychopy_process(subject_id, resources_path, results_path, start_time, execution_mode) :
    if execution_mode == "dev":
        IMAGE_DURATION = 1  # Initial image duration (seconds) BASAL
        TRIAL_DURATION_ARITHMETIC = 5  # Duration for each arithmetic cycle (seconds)
        BREAK_DURATION = 2  # Duration of the break between arithmetic cycles (seconds)
        NUM_CYCLES = 1  # Number of cycles arithmetic cycles
        CYCLE_TYPES = ['add', 'substraction', 'multiplication', 'division']  # Order of question types for Arithmetic cycles
        PROGRAMMING_DURATION = 5  # Duration for the programming cycle (seconds)
        TRIAL_DURATION_SA = 5  # Duration for each trial cycle (seconds) for Spatial abilities cycle 
        MATH_QUESTION_CSV = f'{resources_path}math_test.csv'  # Path to the arithmetic QUESTIONS
        DISPLAY_IMAGE_PATH = f'{resources_path}image_bank/1x/estado_basal.png'  # Path to the initial image BASAL
        SA_QUESTION_CSV = f'{resources_path}sa.csv'  # Path to the SA questions CSV
        PROGRAMMING_CSV = f'{resources_path}coding_questions.csv'  # Path to the programming questions CSV file
        image_bank_path = f'{resources_path}image_bank/1x/'
        interstage_break = 3
    elif execution_mode =="prod":
        IMAGE_DURATION = 120 # Initial image duration (seconds) BASAL
        TRIAL_DURATION_ARITHMETIC = 120  #120  Duration for each arithmetic cycle (seconds)
        BREAK_DURATION = 30  # Duration of the break between arithmetic cycles (seconds)
        NUM_CYCLES = 4  # Number of cycles arithmetic cycles
        CYCLE_TYPES = ['add', 'substraction', 'multiplication', 'division']  # Order of question types for Arithmetic cycles
        PROGRAMMING_DURATION = 200  # Duration for the programming cycle (seconds)
        TRIAL_DURATION_SA = 30  # Duration for each trial cycle (seconds) for Spatial abilities cycle 
        MATH_QUESTION_CSV = f'{resources_path}math_test.csv'  # Path to the arithmetic QUESTIONS
        DISPLAY_IMAGE_PATH = f'{resources_path}image_bank/1x/estado_basal.png'  # Path to the initial image BASAL
        SA_QUESTION_CSV = f'{resources_path}sa.csv'  # Path to the SA questions CSV
        PROGRAMMING_CSV = f'{resources_path}coding_questions.csv'  # Path to the programming questions CSV file
        image_bank_path = f'{resources_path}image_bank/1x/'
        interstage_break = 30
    elif execution_mode== "demo":
        IMAGE_DURATION = 15 # Initial image duration (seconds) BASAL
        TRIAL_DURATION_ARITHMETIC = 30  #120  Duration for each arithmetic cycle (seconds)
        BREAK_DURATION = 10  # Duration of the break between arithmetic cycles (seconds)
        NUM_CYCLES = 4  # Number of cycles arithmetic cycles
        CYCLE_TYPES = ['add', 'substraction', 'multiplication', 'division']  # Order of question types for Arithmetic cycles
        PROGRAMMING_DURATION = 20  # Duration for the programming cycle (seconds)
        TRIAL_DURATION_SA = 20  # Duration for each trial cycle (seconds) for Spatial abilities cycle 
        MATH_QUESTION_CSV = f'{resources_path}math_test.csv'  # Path to the arithmetic QUESTIONS
        DISPLAY_IMAGE_PATH = f'{resources_path}image_bank/1x/estado_basal.png'  # Path to the initial image BASAL
        SA_QUESTION_CSV = f'{resources_path}sa.csv'  # Path to the SA questions CSV
        PROGRAMMING_CSV = f'{resources_path}coding_questions.csv'  # Path to the programming questions CSV file
        image_bank_path = f'{resources_path}image_bank/1x/'
        interstage_break = 10
    

    '''info = {'Participant ID': ''}
    dlg = gui.DlgFromDict(info)
    if not dlg.OK or not info['Participant ID']:
        core.quit()
    participant_id = info['Participant ID']'''

    while start_time.value == 0:
        pass  # Wait for synchronization

    win = visual.Window(fullscr=False, size=(1440, 900), color='black') #window specifications
    all_arithmetic_responses = []  # To store all arithmetic responses
    programming_responses = []     # To store all programming responses
    sa_responses = []  # To store all SA responses

    

    try:
        log_message("Starting experiment.")

        # Step 1: Display initial image BASAL
        display_image(win, DISPLAY_IMAGE_PATH, IMAGE_DURATION)
        # Step 2: arithmetic cycle display function
        all_arithmetic_responses = arithmetic_questions_flow(win, MATH_QUESTION_CSV, 
                                                             NUM_CYCLES, TRIAL_DURATION_ARITHMETIC, 
                                                             BREAK_DURATION, CYCLE_TYPES,
                                                             start_time)
        save_data(all_arithmetic_responses, subject_id,results_path,'arithmetic')

        # Step 3: programming cycle display function
        take_break(win, interstage_break)
        programming_responses = programming_questions_flow(win, 
                                                           PROGRAMMING_CSV, 
                                                           PROGRAMMING_DURATION,
                                                           start_time)
        save_data(programming_responses, subject_id,results_path, 'programming')

        # Step 4: programming cycle display function
        take_break(win, interstage_break)
        sa_responses = spatial_abilities_flow(win, 
                                              image_bank_path, 
                                              SA_QUESTION_CSV, 
                                              TRIAL_DURATION_SA,
                                              start_time)
        save_data(sa_responses, subject_id,results_path, "spatial_abilities")

    except Exception as e:
        log_message(f"Unhandled error: {e}")
    finally:
        win.close()
        with open("psychopy closed.txt", "w") as psychopy_flag_file:
            psychopy_flag_file.write("1")
        core.quit()

