@echo off
setlocal

:: Define virtual environment directory
set VENV_DIR=my_venv
set PYTHON_PATH="C:\Users\luisf\AppData\Local\Programs\Python\Python39\python.exe"

:: Step 1: Create virtual environment using a specific Python installation
%PYTHON_PATH% -m venv %VENV_DIR%

:: Step 2: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

:: Step 3: Install libraries A, B, and C
pip install numpy==1.23.0
pip install pandas==1.4.3
pip install psychopy==2022.2.0
pip install python-vlc==3.0.11115

:: Step 4: Uninstall library A
pip uninstall -y numpy

:: Step 5: Reinstall library A
pip install numpy==1.23.0

:: Deactivate virtual environment
deactivate

echo Script execution completed successfully.
endlocal
