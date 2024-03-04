import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5 import QtCore
import board_handler

class PlotUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG electrodes")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # initiate connection to board and begin acquisition
        self.openbci = board_handler.brainflow_board_object()
        
        self.x = np.linspace(0, 2 * np.pi, 1000)
        self.y = np.sin(self.x)


        #initializes the plot, and intializes the self.line attribute, which is the function line itself 
        self.line, = self.ax.plot(self.x, self.y)
        # Initialize the timer attribute
        self.animation_timer = QtCore.QTimer(self)

        # THE FOLLOWING TWO LINES COMPRISE THE CORE LOOP OF THE CLASS TO KEEP UPDATING THE PLOT
        # Set a reaction for the flag of timeout for the attribute timer
        self.animation_timer.timeout.connect(self.update_plot)
        # Begin an arbitrary timer. Upon ending, it flags for timeout, returning to the previous line.
        self.animation_timer.start(250)  # Update plot every 50 milliseconds

        self.openbci.close_board()
        
    def update_plot(self):
        # Shift the sine wave to the right
        self.x += 0.1
        self.y = np.sin(self.x)
        print(self.y)
        # Update the data of the line plot
        self.line.set_xdata(self.x)
        self.line.set_ydata(self.y)

        # Adjust plot limits to keep the sine wave visible
        self.ax.set_xlim(self.x.max()-5, self.x.max())
        self.ax.set_ylim(-1.1, 1.1)

        # Redraw the plot
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotUpdater()
    window.show()
    sys.exit(app.exec_())

