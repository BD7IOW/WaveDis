import sys
import random

import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget

import numpy as np
from numpy import arange, sin, pi,cos
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # 每次的plot()调用的时候，我们希望原来坐标轴被清除(所以False)
        #
        # FigureCanvas.grid(True)
        #显示图例

        self.compute_initial_figure()


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    """静态画布：一条正弦线"""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        s1 = cos( 2 * pi * t)
        self.axes.plot(t, s,label='sin',color='r')
        # pl.plot( x, y, label='YR', color='red' )
        #
        self.axes.plot( t, s1,label='cos',color='b' )
        self.axes.set_title('time demond')
        self.axes.xaxis.grid(True)
        self.axes.yaxis.grid( True)
        self.axes.legend(loc='upper right')

class MyStaticFFTCan(MyMplCanvas):
    # SR = 8000.0
    N = 512
    def compute_initial_figure(self):
        t = arange(0, 2*np.pi, 2*np.pi/self.N)#/x=np.linspace(0,1,1400)
        s = cos(200*t+pi/2)

        # xf = np.linspace(0,1,self.N)
        y = np.fft.fft(s)
        print(np.array_str(y[:4]))
        # freqs = np.linspace(0,self.sampling_rate/2,self.fft_size/2+1)
        # xfp = 20 * np.log10(np.clip(np.abs(y), 1e-20, 1e100 ) )
        # xf = np.arange(len(t))
        self.axes.plot(abs(y)*2/len(y))
        self.axes.yaxis.grid(True)
        self.axes.set_ylim(0,1.5)
        ang = np.rad2deg(np.angle(y[200]))
        print(ang)
        # print(np.angle(y,deg='True'))

class MyDynamicMplCanvas(MyMplCanvas):
    """动态画布：每秒自动更新，更换一条折线。"""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.hold( False )
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # 构建4个随机整数，位于闭区间[0, 10]
        l = [random.randint(0, 100) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("程序主窗口")

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        ft = MyStaticFFTCan(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)
        l.addWidget(ft)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        # 状态条显示2秒
        self.statusBar().showMessage("matplotlib 万岁!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
        """embedding_in_qt5.py example
        Copyright 2015 BoxControL

        This program is a simple example of a Qt5 application embedding matplotlib
        canvases. It is base on example from matplolib documentation, and initially was
        developed from Florent Rougon and Darren Dale.

        http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

        It may be used and modified with no restriction; raw copies as well as
        modified versions may be distributed without limitation.
        """
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("PyQt5 与 Matplotlib 例子")
    aw.show()
    #sys.exit(qApp.exec_())
    app.exec_()