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
        self.axes1 = fig.add_subplot(421)
        self.axes1.set_title('Channel 1')
        self.axes2 = fig.add_subplot(422)
        self.axes2.set_title('Channel 2')
        self.axes3 = fig.add_subplot(423)
        self.axes3.set_title('Channel 3')
        self.axes4 = fig.add_subplot(424)
        self.axes4.set_title('Channel 4')
        self.axes5 = fig.add_subplot(425)
        self.axes5.set_title('Channel 5')
        self.axes6 = fig.add_subplot(426)
        self.axes6.set_title('Channel 6')
        self.axes7 = fig.add_subplot(427)
        self.axes7.set_title('Channel 7')
        self.axes8 = fig.add_subplot(428)
        self.axes8.set_title('Channel 8')

        fig.tight_layout()  # Automatically adjust subplot params to give specified padding

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
        self.y3 = np.zeros(50);
        self.y4 = np.zeros(50);
        self.y5 = np.zeros(50);
        self.y6 = np.zeros(50);
        self.y7 = np.zeros(50);
        self.y8 = np.zeros(50);
        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref1 = None
        self._plot_ref2 = None
        self._plot_ref3 = None
        self._plot_ref4 = None
        self._plot_ref5 = None
        self._plot_ref6 = None
        self._plot_ref7 = None
        self._plot_ref8 = None

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
        self.y3 = np.append(self.y3[1:], [new_data[2]]);
        self.y4 = np.append(self.y4[1:], [new_data[3]]);
        self.y5 = np.append(self.y5[1:], [new_data[4]]);
        self.y6 = np.append(self.y6[1:], [new_data[5]]);
        self.y7 = np.append(self.y7[1:], [new_data[6]]);
        self.y8 = np.append(self.y8[1:], [new_data[7]]);

        self.x = np.append(self.x[1:], [self.x[-1]+(batch_samples/125)]);

        #print("after updating X",np.shape(self.x), self.x)
        #print("after updating Y",np.shape(self.y1), self.y1)

        # Plotting signals
        if self._plot_ref1 is None:
            plot_refs = self.canvas.axes1.plot(self.x, self.y1, 'r')
            self._plot_ref1 = plot_refs[0]
            plot_refs = self.canvas.axes2.plot(self.x, self.y2, 'b')
            self._plot_ref2 = plot_refs[0]
            plot_refs = self.canvas.axes3.plot(self.x, self.y3, 'g')
            self._plot_ref3 = plot_refs[0]
            plot_refs = self.canvas.axes4.plot(self.x, self.y4, 'r')
            self._plot_ref4 = plot_refs[0]
            plot_refs = self.canvas.axes5.plot(self.x, self.y5, 'b')
            self._plot_ref5 = plot_refs[0]
            plot_refs = self.canvas.axes6.plot(self.x, self.y6, 'g')
            self._plot_ref6 = plot_refs[0]
            plot_refs = self.canvas.axes7.plot(self.x, self.y7, 'r')
            self._plot_ref7 = plot_refs[0]
            plot_refs = self.canvas.axes8.plot(self.x, self.y8, 'b')
            self._plot_ref8 = plot_refs[0]
        else:
            self._plot_ref1.set_xdata(self.x)
            self._plot_ref1.set_ydata(self.y1)
            self._plot_ref2.set_xdata(self.x)
            self._plot_ref2.set_ydata(self.y2)
            self._plot_ref3.set_xdata(self.x)
            self._plot_ref3.set_ydata(self.y3)
            self._plot_ref4.set_xdata(self.x)
            self._plot_ref4.set_ydata(self.y4)
            self._plot_ref5.set_xdata(self.x)
            self._plot_ref5.set_ydata(self.y5)
            self._plot_ref6.set_xdata(self.x)
            self._plot_ref6.set_ydata(self.y6)
            self._plot_ref7.set_xdata(self.x)
            self._plot_ref7.set_ydata(self.y7)
            self._plot_ref8.set_xdata(self.x)
            self._plot_ref8.set_ydata(self.y8)

        # Adjust plot limits for subplots
        self.canvas.axes1.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes1.set_ylim(self.y1.min() * 1.15, self.y1.max() * 1.15)
        self.canvas.axes2.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes2.set_ylim(self.y2.min() * 1.15, self.y2.max() * 1.15)
        self.canvas.axes3.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes3.set_ylim(self.y3.min() * 1.15, self.y3.max() * 1.15)
        self.canvas.axes4.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes4.set_ylim(self.y4.min() * 1.15, self.y4.max() * 1.15)
        self.canvas.axes5.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes5.set_ylim(self.y5.min() * 1.15, self.y5.max() * 1.15)
        self.canvas.axes6.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes6.set_ylim(self.y6.min() * 1.15, self.y6.max() * 1.15)
        self.canvas.axes7.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes7.set_ylim(self.y7.min() * 1.15, self.y7.max() * 1.15)
        self.canvas.axes8.set_xlim(self.x.min() - 1, self.x.max() + 1)
        self.canvas.axes8.set_ylim(self.y8.min() * 1.15, self.y8.max() * 1.15)

        # Redraw the plot
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotUpdater()
    window.show()
    sys.exit(app.exec_())

