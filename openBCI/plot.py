import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5 import QtCore
import board_handler
import matplotlib
matplotlib.use('QtAgg')

#from PyQt6 import QtCore, QtWidgets
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        # generate axes for each subplot
        self.axes1 = fig.add_subplot(311)
        self.axes2 = fig.add_subplot(312)
        super(MplCanvas, self).__init__(fig)

class PlotUpdater(QMainWindow):
    def __init__(self):
        super(PlotUpdater, self).__init__()
        self.setWindowTitle("EEG electrodes");
        self.setGeometry(100, 100, 800, 600);

        self.fig, self.ax = plt.subplots();
        ###self.canvas = FigureCanvas(self.fig);
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        # initiate connection to board and begin acquisition
        self.openbci = board_handler.brainflow_board_object();
        
        self.x = np.zeros(50);  # assuming 1000 samples initially
        self.y1 = np.zeros(50);  # assuming 1000 samples initially
        self.y2 = np.zeros(50);  # assuming 1000 samples initially

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref1 = None
        self._plot_ref2 = None

        self.update_plot()

        self.show()
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
        batch_samples, new_data = self.openbci.get_signal();  # Get 100 new samples (adjust as needed)

        # select the corresponding channel data
        self.y1 = np.append(self.y1[1:], [new_data[0]]);
        self.y2 = np.append(self.y2[1:], [new_data[1]]);

        self.x = np.append(self.x[1:], [self.x[-1]+(batch_samples/125)]);

        #print("after updating X",np.shape(self.x), self.x)
        #print("after updating Y",np.shape(self.y1), self.y1)

        # Plotting signals
        if self._plot_ref1 is None:
            plot_refs = self.canvas.axes1.plot(self.x, self.y1, 'r')
            self._plot_ref1 = plot_refs[0]
            plot_refs = self.canvas.axes2.plot(self.x, self.y2, 'b')
            self._plot_ref2 = plot_refs[0]
            
        else:
            self._plot_ref1.set_xdata(self.x)
            self._plot_ref1.set_ydata(self.y1)
            self._plot_ref2.set_xdata(self.x)
            self._plot_ref2.set_ydata(self.y2)

        # Adjust plot limits for subplots
        self.canvas.axes1.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes1.set_ylim(self.y1.min() * 1.15, self.y1.max() * 1.15)
        self.canvas.axes2.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes2.set_ylim(self.y2.min() * 1.15, self.y2.max() * 1.15)
        
        # Redraw the plot
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotUpdater()
    window.show()
    sys.exit(app.exec_())

