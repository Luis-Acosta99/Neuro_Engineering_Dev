import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5 import QtCore
import board_handler

class PlotUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG electrodes");
        self.setGeometry(100, 100, 800, 600);

        self.central_widget = QWidget();
        self.setCentralWidget(self.central_widget);

        self.layout = QVBoxLayout();
        self.central_widget.setLayout(self.layout);

        self.fig, self.ax = plt.subplots();
        self.canvas = FigureCanvas(self.fig);
        self.layout.addWidget(self.canvas);

        # initiate connection to board and begin acquisition
        self.openbci = board_handler.brainflow_board_object();
        
        self.x = np.zeros(1);  # assuming 1000 samples initially
        self.y = np.zeros(1);  # assuming 1000 samples initially

        #initializes the plot, and intializes the self.line attribute, which is the function line itself 
        self.line, = self.ax.plot(self.x, self.y);
        # Initialize the timer attribute
        self.animation_timer = QtCore.QTimer(self);

        time.sleep(2)
        # THE FOLLOWING TWO LINES COMPRISE THE CORE LOOP OF THE CLASS TO KEEP UPDATING THE PLOT
        # Set a reaction for the flag of timeout for the attribute timer
        self.animation_timer.timeout.connect(self.update_plot);
        # Begin an arbitrary timer. Upon ending, it flags for timeout, returning to the previous line.
        self.animation_timer.start(500);  # Update plot every 50 milliseconds

        # Connect aboutToQuit signal to cleanup method
        app.aboutToQuit.connect(self.cleanup);

    def cleanup(self):
        # Cleanup before exiting the application
        self.openbci.close_board();

    def update_plot(self):
        # Get new data from the sensor
        new_data = self.openbci.get_signal();  # Get 100 new samples (adjust as needed)
        # Append new data to the existing data
        try:
            self.y = np.append(self.y,new_data);
        except TypeError:
            self.y = np.append(self.y, np.array([new_data]));
        try:
            self.x = np.arange(0, len(self.y) * 0.5, 0.5);
            #self.x  = np.arange(0, self.y.shape[1] * 0.5, 0.5)
        except IndexError:
            self.x = np.arange(0, len(self.y) * 0.5, 0.5);
        # Update the data of the line plot
        self.line.set_ydata(self.y);
        self.line.set_xdata(self.x);

        # Adjust plot limits to keep the signal visible
        self.ax.set_xlim(1, len(self.y) * 0.5)  # adjust x-limit based on the length of data
    # Adjust y-limit according to the range of data, you may customize this according to your data
        self.ax.set_ylim(self.y.min()-self.y.min()*0.1, self.y.max()+self.y.min()*0.1)

        # Redraw the plot
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotUpdater()
    window.show()
    sys.exit(app.exec_())

