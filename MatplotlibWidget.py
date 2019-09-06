import sys
import matplotlib
import csv

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget,QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        # self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''启动绘制网络流量图'''

    def start_static_plot1(self,b):

        filename = b
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)
            '''读取.csv文件'''
            dates, allbyte = [], []
            tempdatef = datetime.strptime(next(reader)[2], "%Y/%m/%d %H:%M:%S")
            '''统一将.csv文件中与时间相关的字符串格式化为时间格式'''
            tempbytes = 0
            for row in reader:
                nowdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
                if nowdatef.minute != tempdatef.minute:
                    '''非同一分钟内跳转到下一分钟'''
                    allbyte.append(tempbytes)
                    dates.append(tempdatef)
                    tempdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
                    tempbytes = int(row[10])
                else:
                    '''同一分钟内数据量累加'''
                    tempbytes = tempbytes + int(row[10])
            '''网络流量判断，将.csv文件中每分钟内的网络流中包含的流量数求和计算每分钟的网络流量情况'''
        self.fig.suptitle('网络流量显示平台', fontsize=20)
        self.axes.plot(dates, allbyte, c='blue')
        self.axes.set_ylabel('网络流量', fontsize=16)
        self.axes.set_xlabel('时间', fontsize=16)
        '''将统计到的结果绘制成图表形式显示'''
    '''启动绘制源端口目的端口比值图'''

    def start_static_plot2(self,b):

        filename = b
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)

            src, des, allsrcdes, dates = [], [], [], []
            tempdatef = datetime.strptime(next(reader)[2], "%Y/%m/%d %H:%M:%S")
            tempbytes = 0

            for row in reader:
                nowdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
                if nowdatef.minute == tempdatef.minute:
                    if row[4] not in src:
                        src.append(row[4])
                    if row[6] not in des:
                        des.append(row[6])
                else:
                    lensrc = len(src)
                    lendes = len(des)
                    if lendes == 0:
                        srcdes = 0
                    else:
                        srcdes = lensrc / lendes
                    allsrcdes.append(srcdes)
                    dates.append(tempdatef)
                    tempdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
                    src, des = [], []

        self.fig.suptitle('源端口目的端口比值显示平台', fontsize=20)
        self.axes.plot(dates, allsrcdes, c='red')
        self.axes.set_ylabel('源端口目的端口比值', fontsize=16)
        self.axes.set_xlabel('时间', fontsize=16)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)

