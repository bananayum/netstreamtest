# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog
from PyQt5.Qt import QStandardItemModel,QStandardItem,QHeaderView
from Ui_matplotlib_pyqt import Ui_MainWindow
import singlecheck
import modecheck
import pymysql

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.matplotlibwidget_dynamic.setVisible(False)
        self.matplotlibwidget_static.setVisible(False)
        self.actionzairu.triggered.connect(self.openMsg)
        self.a=None

        self.actiontuicu.triggered.connect(self.close)
        self.pushButton_3.clicked.connect(self.singlestate)
        self.pushButton_4.clicked.connect(self.modestate)
        self.pushButton_5.clicked.connect(self.displaysql)

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
        # 在状态栏显示文件地址
        self.statusbar.showMessage(file)
        self.a=file
        db = pymysql.connect("localhost", "root", "123456", "flowdata", charset="UTF8")
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS ANOMALYTYPE")
        sql="""CREATE TABLE ANOMALYTYPE(异常发生时间 CHAR(64) NOT NULL,异常流量源地址 CHAR(64),异常流量目的地址 CHAR(64),异常流量类型 CHAR(64))"""
        cursor.execute(sql)
        db.close()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        b=self.a
        self.matplotlibwidget_static.setVisible(True)
        self.matplotlibwidget_static.mpl.start_static_plot1(b)


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        b = self.a
        self.matplotlibwidget_dynamic.setVisible(True)
        self.matplotlibwidget_dynamic.mpl.start_static_plot2(b)

    def singlestate(self):
        b = self.a
        singlecheck.single(b)

    def modestate(self):
        b = self.a
        modecheck.mode(b)

    def displaysql(self):
        db = pymysql.connect("localhost", "root", "123456", "flowdata", charset="UTF8")
        cursor = db.cursor()
        cursor.execute("SELECT *FROM ANOMALYTYPE")
        rows = cursor.fetchall()
        if rows !=():
            row = cursor.rowcount  # 取得记录个数，用于设置表格的行数
            vol = len(rows[0])  # 取得字段数，用于设置表格的列数
            cursor.close()
            db.close()
            self.model = QStandardItemModel()
            self.model.setHorizontalHeaderLabels(['异常发生时间', '异常流量源地址', '异常流量目的地址', '异常流量类型'])
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(row):
                for j in range(vol):
                    temp_data = rows[i][j]
                    data = QStandardItem("%s"%(str(temp_data)))
                    self.model.setItem(i, j,data)
            self.tableView.setModel(self.model)
        else:
            cursor.close()
            db.close()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())