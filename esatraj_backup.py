# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'esatraj.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from serial import Serial
from serial.tools import list_ports
import threading
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT 

# update 3d/2d plots period (ms)
PLOT_UPDATE_PERIOD = 500

class Canvas3d(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig = plt.figure(figsize=[14.4, 10.8])
        self.ax = fig.add_subplot(projection="3d")
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # self.ax.axis('equal')
        super().__init__(fig)
        self.timer = self.new_timer(PLOT_UPDATE_PERIOD)
        self.setParent(parent)

class Canvas2d(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig = plt.figure(figsize=[14.4, 10.8])
        self.ax = fig.add_subplot(projection="rectilinear")
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.axis('equal')
        super().__init__(fig)
        self.timer = self.new_timer(PLOT_UPDATE_PERIOD)
        self.setParent(parent)


class Ui_ESATrajWindow(object):
    def setupUi(self, ESATrajWindow):
        ESATrajWindow.setObjectName("ESATrajWindow")
        # ESATrajWindow.resize(1382, 619)
        ESATrajWindow.resize(800, 619)
        self.centralwidget = QtWidgets.QWidget(ESATrajWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ComPortSelect = QtWidgets.QComboBox(self.centralwidget)
        self.ComPortSelect.setGeometry(QtCore.QRect(20, 30, 111, 22))
        self.ComPortSelect.setObjectName("ComPortSelect")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        # self.Enable2DPlot = QtWidgets.QCheckBox(self.centralwidget)
        # self.Enable2DPlot.setGeometry(QtCore.QRect(20, 100, 73, 16))
        # self.Enable2DPlot.setObjectName("Enable2DPlot")

        # enable 3d plot
        self.Enable3DPlot = QtWidgets.QCheckBox(self.centralwidget)
        self.Enable3DPlot.setGeometry(QtCore.QRect(20, 70, 73, 16))
        self.Enable3DPlot.setChecked(True)
        self.Enable3DPlot.setObjectName("Enable3DPlot")


        # connect
        self.ConnectButton = QtWidgets.QPushButton(self.centralwidget)
        self.ConnectButton.setGeometry(QtCore.QRect(20, 170, 111, 23))
        self.ConnectButton.setObjectName("ConnectButton")
        # self.SavePlotButton = QtWidgets.QPushButton(self.centralwidget)
        # self.SavePlotButton.setGeometry(QtCore.QRect(20, 550, 111, 23))
        # self.SavePlotButton.setObjectName("SavePlotButton")

        # start plot
        self.StartPlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartPlotButton.setGeometry(QtCore.QRect(20, 510, 111, 23))
        self.StartPlotButton.setObjectName("StartPlotButton")


        # clear plot
        self.ClearPlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.ClearPlotButton.setGeometry(QtCore.QRect(20, 550, 111, 23))
        self.ClearPlotButton.setObjectName("ClearPlotButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)


        self.label_2.setGeometry(QtCore.QRect(410, 10, 47, 12))
        self.label_2.setObjectName("label_2")
        # self.label_3 = QtWidgets.QLabel(self.centralwidget)
        # self.label_3.setGeometry(QtCore.QRect(1080, 10, 47, 12))
        # self.label_3.setObjectName("label_3")
        self.ComStatusDisplay = QtWidgets.QLabel(self.centralwidget)
        self.ComStatusDisplay.setGeometry(QtCore.QRect(20, 210, 111, 16))
        self.ComStatusDisplay.setObjectName("ComStatusDisplay")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 240, 111, 16))
        self.label_5.setObjectName("label_5")
        self.DataCountDisplay = QtWidgets.QLineEdit(self.centralwidget)
        self.DataCountDisplay.setEnabled(True)
        self.DataCountDisplay.setGeometry(QtCore.QRect(20, 260, 111, 20))
        self.DataCountDisplay.setReadOnly(False)
        self.DataCountDisplay.setObjectName("DataCountDisplay")

        # enable log
        self.EnableLog = QtWidgets.QCheckBox(self.centralwidget)
        self.EnableLog.setGeometry(QtCore.QRect(20, 130, 121, 16))
        self.EnableLog.setObjectName("EnableLog")

        # save csv
        self.StartCSVButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartCSVButton.setGeometry(QtCore.QRect(20, 300, 111, 23))
        self.StartCSVButton.setObjectName("StartCSVButton")

        # load csv
        self.LoadCSVButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadCSVButton.setGeometry(QtCore.QRect(20, 340, 111, 23))
        self.LoadCSVButton.setObjectName("LoadCSVButton")

        self.PlotPlaneSelect = QtWidgets.QComboBox(self.centralwidget)
        self.PlotPlaneSelect.setGeometry(QtCore.QRect(20, 470, 111, 22))
        self.PlotPlaneSelect.setObjectName("PlotPlaneSelect")
        self.PlotPlaneSelect.addItem("")
        self.PlotPlaneSelect.addItem("")
        self.PlotPlaneSelect.addItem("")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 450, 101, 16))
        self.label_4.setObjectName("label_4")
        # self.PlotLayout3d = QtWidgets.QVBoxLayout(self.centralwidget)
        # self.PlotLayout3d.setGeometry(QtCore.QRect(170, 30, 591, 551))
        # self.PlotLayout3d.setObjectName("PlotLayout3d")
        # self.PlotLayout2d = QtWidgets.QVBoxLayout(self.centralwidget)
        # self.PlotLayout2d.setGeometry(QtCore.QRect(780, 30, 591, 551))
        # self.PlotLayout2d.setObjectName("PlotLayout2d")
        ESATrajWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ESATrajWindow)
        self.statusbar.setObjectName("statusbar")
        ESATrajWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ESATrajWindow)
        self.initVariables()
        self.initPlot()
        self.updateCom()
        self.buttonEvents()
        QtCore.QMetaObject.connectSlotsByName(ESATrajWindow)

    def retranslateUi(self, ESATrajWindow):
        _translate = QtCore.QCoreApplication.translate
        ESATrajWindow.setWindowTitle(_translate("ESATrajWindow", "ESATraj Plotter"))
        self.label.setText(_translate("ESATrajWindow", "COM Port"))
        # self.Enable2DPlot.setText(_translate("ESATrajWindow", "2D Plot"))
        self.Enable3DPlot.setText(_translate("ESATrajWindow", "3D Plot"))
        self.ConnectButton.setText(_translate("ESATrajWindow", "Connect"))
        # self.SavePlotButton.setText(_translate("ESATrajWindow", "Save Plot"))
        self.StartPlotButton.setText(_translate("ESATrajWindow", "Start Plot"))
        self.ClearPlotButton.setText(_translate("ESATrajWindow", "Clear Plot"))
        self.label_2.setText(_translate("ESATrajWindow", "3D"))
        # self.label_3.setText(_translate("ESATrajWindow", "2D"))
        self.ComStatusDisplay.setText(_translate("ESATrajWindow", "Disconnected"))
        self.label_5.setText(_translate("ESATrajWindow", "Data Received "))
        self.DataCountDisplay.setText(_translate("ESATrajWindow", "0"))
        self.EnableLog.setText(_translate("ESATrajWindow", "Terminal Log"))
        self.StartCSVButton.setText(_translate("ESATrajWindow", "Save CSV"))
        self.LoadCSVButton.setText(_translate("ESATrajWindow", "Load CSV"))
        self.PlotPlaneSelect.setItemText(0, _translate("ESATrajWindow", "XY"))
        self.PlotPlaneSelect.setItemText(1, _translate("ESATrajWindow", "XZ"))
        self.PlotPlaneSelect.setItemText(2, _translate("ESATrajWindow", "YZ"))
        self.label_4.setText(_translate("ESATrajWindow", "2D Plot Plane"))



 #----------- initiazation ----------
    def initVariables(self):
        self.com_port_name = ""
        self.raw_data = []
        self.trajectory3d = np.empty([0,3])
        self.trajectory2d = np.empty([0,2])
        self.enable_plot2d = False
        self.enable_plot3d = False
        self.enable_log = False
        self.connected = False
        self.drawing = False
        self.data_count = 0

        # self.current_x =0
        # self.current_y = 0
        # self.current_z = 0

    def initPlot(self):
        self.plot3d_canvas = Canvas3d(self.centralwidget)
        self.plot3d_canvas.setGeometry(QtCore.QRect(170, 30, 590, 520))
        self.plot3d_line = self.plot3d_canvas.ax.plot(self.trajectory3d[:,0], self.trajectory3d[:,1], self.trajectory3d[:,2], color = 'b', linewidth=2.0)
        self.plot3d_toolbar = NavigationToolbar2QT(self.plot3d_canvas,self.centralwidget)
        self.plot3d_toolbar.setGeometry(QtCore.QRect(170, 550, 590, 50))
        
    # add button events
    def buttonEvents(self):
        self.ConnectButton.clicked.connect(self.connectPort)
        self.ClearPlotButton.clicked.connect(self.clearPlot)
        self.StartCSVButton.clicked.connect(self.saveCSV)
        self.LoadCSVButton.clicked.connect(self.loadCSV)
        # self.SavePlotButton.clicked.connect(self.savePlot)

    # update com port list
    def updateCom(self):
        ports = list_ports.comports()
        portnames=[]
        for p in ports:
            portnames.append(p.name)
        self.ComPortSelect.addItems(portnames)
        self.ComPortSelect.addItem("Dummy")

    #------------------ events ---------------------
    def update_3d_plot(self):
        self.plot3d_canvas.ax.plot(self.trajectory3d[:,0], self.trajectory3d[:,1], self.trajectory3d[:,2], color = 'b', linewidth=2.0)
        min_x = np.amin(self.trajectory3d[:, 0])
        min_y = np.amin(self.trajectory3d[:, 1])
        min_z = np.amin(self.trajectory3d[:, 2])
        max_x = np.amax(self.trajectory3d[:, 0])
        max_y = np.amax(self.trajectory3d[:, 1])
        max_z = np.amax(self.trajectory3d[:, 2])
        range_x = np.absolute(max_x - min_x)
        range_y = np.absolute(max_y - min_y)
        range_z = np.absolute(max_z - min_z)
        max_range = np.maximum(np.maximum(range_x, range_y), range_z)
        self.plot3d_canvas.ax.set_xlim(min_x, min_x + max_range)
        self.plot3d_canvas.ax.set_ylim(min_y, min_y + max_range)
        self.plot3d_canvas.ax.set_zlim(min_z, min_z + max_range)
        self.plot3d_canvas.draw()
    

    def connectPort(self):
        # self.enable_plot2d = self.Enable2DPlot.isChecked()
        self.enable_plot3d = self.Enable3DPlot.isChecked()
        self.enable_log = self.EnableLog.isChecked()
        self.com_port_name = self.ComPortSelect.currentText()
        self.ComStatusDisplay.setText("Connecting...") 
        self.data_count = 0   
        self.clearPlot()  

        def update_3dplot_process():
            if self.drawing:
                try:
                    self.update_3d_plot()
                except:
                    pass

        
        if self.com_port_name == 'Dummy':
            # change status to connected
            self.connected = True
            # create dummy trajectory
            self.plot3d_canvas.ax.set_title(self.com_port_name+' - 3D Trajectory')
            self.current_x =0
            self.current_y = 0
            self.current_z = 0

            def dummy_traj():
                while self.connected:
                    # draw spiral

                    self.current_z += 0.01
                    self.current_x = np.sin(self.current_z)*50
                    self.current_y = np.cos(self.current_z)*50

                    # receive trajectory
                    if self.enable_plot2d:
                        self.trajectory2d = np.append(self.trajectory2d,[[self.current_x,self.current_y]],axis=0)
                    if self.enable_plot3d:
                        self.trajectory3d = np.append(self.trajectory3d,[[self.current_x,self.current_y,self.current_z]],axis=0)
                        
                        # self.fig3d= px.line_3d(data_frame=self.trajectory3d, x=0, y=1, z=2)

                    self.data_count += 1
                    self.DataCountDisplay.setText(str(self.data_count))

                    # log trajectory
                    if self.enable_log:
                        if self.enable_plot3d and self.trajectory3d.shape[0] >= 1:
                            print(self.trajectory3d[-1])
                        elif self.enable_plot2d and self.trajectory2d.shape[0] >= 1:
                            print(self.trajectory2d[-1])
                            

                    time.sleep(0.01)

                # disconnect
                self.current_x =50
                self.current_y =-50
                self.current_z = 100


            # run dummy process
            dummy_process = threading.Thread(target=dummy_traj)
            dummy_process.start()
            
        else:
            # connect to com port
            self.serial = Serial(self.com_port_name,9600)
         
            # change status to connected
            self.connected = True
            # display connected
            self.displayConnected()
            
            time.sleep(0.1)
            
            # receive and draw
            self.serial.write(b'esatraj_start')

            def receive_traj():
                while self.connected:
                    try:
                        data_raw = self.serial.readline()
                        data = data_raw.decode()

                        if self.enable_log:
                            print(data)

                        point = data.split('/')
                        x = float(point[0])
                        y = float(point[1])
                        z = float(point[2])

                        self.data_count += 1
                        self.DataCountDisplay.setText(str(self.data_count))

                        if self.enable_plot2d:
                            self.trajectory2d = np.append(self.trajectory2d,[[x,y]],axis=0)
                        if self.enable_plot3d:
                            self.trajectory3d = np.append(self.trajectory3d,[[x,y,z]],axis=0)
                    except:
                        pass      
                try:
                    self.serial.write(self.serial.write(b'esatraj_stop'))
                except:
                    pass      
            # run receiving process
            receive_process = threading.Thread(target=receive_traj)
            receive_process.start()

        # display connected
        if self.connected:
            self.displayConnected()
            self.plot3d_canvas.timer.add_callback(update_3dplot_process)
            self.plot3d_canvas.timer.start()


    def clearPlot(self):
        if self.enable_log:
            print("clear plot")
        self.trajectory3d = np.empty([0,3])
        self.trajectory2d = np.empty([0,2])
        self.plot3d_canvas.timer.stop()
        self.plot3d_canvas.ax.clear()
        self.plot3d_canvas.ax.set_xlabel('X')
        self.plot3d_canvas.ax.set_ylabel('Y')
        self.plot3d_canvas.ax.set_zlabel('Z')
        self.plot3d_canvas.draw()
        # self.update_3d_plot()

    def disconnectPort(self):
        if self.com_port_name != 'dummy':
            # change status to disconnect
            self.connected = False
        else:
            # send stop when disconnecting
            try:
                time.sleep(5)
                self.serial.close()
            except:
                pass
            self.connected = False
            
        
        # display disconnected
        if not self.connected:
            self.displayDisconnected()


    def displayConnected(self):
        self.ComStatusDisplay.setText(self.com_port_name +" Connected")
        self.drawing = True
        self.ConnectButton.clicked.disconnect()
        self.ConnectButton.setText("Disconnect")
        self.ConnectButton.clicked.connect(self.disconnectPort)
        self.StartPlotButton.setText("Stop Plot")

    
    def displayDisconnected(self):
        self.drawing = False
        self.ComStatusDisplay.setText("Disconnected")
        self.ConnectButton.clicked.disconnect()
        self.ConnectButton.setText("Connect")
        self.ConnectButton.clicked.connect(self.connectPort)


    def saveCSV(self):
        options = QtWidgets.QFileDialog.Options()
        
        path = QtWidgets.QFileDialog.getSaveFileName(None, "Select destination folder and file name", "", "CSV files (*.csv)",
                                    options=options)[0]
        try:
            np.savetxt(path,self.trajectory3d,delimiter=',')
            # csv_data = pd.DataFrame(self.trajectory3d)
            # csv_data.to_csv(path)
        except:
            if self.enable_log:
                print("Unable to save CSV file")
        # print(path)

    def loadCSV(self):
        options = QtWidgets.QFileDialog.Options()
        path = QtWidgets.QFileDialog.getOpenFileName(None, "Select destination folder and file name", "", "CSV files (*.csv)", options=options)[0]
        self.clearPlot()

        try:
            # csv_data = pd.read_csv(path)
            # np_array = csv_data.to_numpy()[:,1:]
            np_array = np.genfromtxt(path, delimiter=',')
            self.trajectory3d = np_array
            self.data_count = np_array.shape[0]
            self.DataCountDisplay.setText(str(self.data_count))
            self.plot3d_canvas.ax.set_title(path)
            self.update_3d_plot()
        except:
            if self.enable_log:
                print("Unable to open CSV file")

        # print(path)
        # print(np_array)
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ESATrajWindow = QtWidgets.QMainWindow()
    ui = Ui_ESATrajWindow()
    ui.setupUi(ESATrajWindow)
    ESATrajWindow.show()
    sys.exit(app.exec_())

