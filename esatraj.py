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
from connection import Connection
from esatraj_ui import Ui_ESATrajWindow
from qtrangeslider import QLabeledRangeSlider

# update 3d/2d plots period (ms)
PLOT_UPDATE_PERIOD = 500
DEFAUTL_CONNECTION_TYPE = "COM"
DEFAULT_MAC_ADDRESS = "E4:5F:01:2B:FA:73"

FILTER_PLOT = True

class Canvas3d(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig = plt.figure(figsize=[14.4, 10.8])
        self.ax = fig.add_subplot(projection="3d")
        self.ax.set_xlabel('X')
        
        # y up
        # if self.axis_up == "Y":
        #     self.ax.set_ylabel('Z')
        #     self.ax.set_zlabel('Y')
        # # z up
        # else:
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

class ESATraj(Ui_ESATrajWindow):

    def __init__(self):
        super().__init__()
    
    def init(self):
        self.initVariables()
        self.showComMacInput()
        self.initPlot()
        self.updateCom()
        self.buttonEvents()

 #----------- initiazation ----------
    def initVariables(self):
        self.connection_type = DEFAUTL_CONNECTION_TYPE
        self.com_port_name = ""
        self.connection_mac_address = DEFAULT_MAC_ADDRESS
        self.InputMacAddress.setText(DEFAULT_MAC_ADDRESS)
        self.raw_data = []
        self.trajectory3d = np.empty([0,3])
        self.plot_trajectory = np.empty([0,3])
        # self.enable_plot2d = False
        # self.enable_plot3d = False
        self.enable_log = False
        self.connected = False
        self.drawing = False
        self.data_count = 0
        self.axis_up = "Z"
        self.animation_speed =10
        self.playing_animation = False

        # self.current_x =0
        # self.current_y = 0
        # self.current_z = 0

    def showComMacInput(self):
        if self.connection_type == "COM":
            self.LabelComMac.setText("COM Port")
            self.InputMacAddress.hide()
            self.ComPortSelect.show()
        elif self.connection_type == "MAC":
            self.LabelComMac.setText("MAC Address")
            self.InputMacAddress.show()
            self.ComPortSelect.hide()

    def initPlot(self):
        self.plot3d_canvas = Canvas3d(self.centralwidget)
        geo = self.PlotPosition.geometry()
        self.plot3d_canvas.setGeometry(geo)
        # y up
        if self.axis_up == "Y":
            self.plot3d_line = self.plot3d_canvas.ax.plot(self.plot_trajectory[:,0], self.plot_trajectory[:,2], self.plot_trajectory[:,1], color = 'b', linewidth=2.0)
        # z up 
        else:
            self.plot3d_line = self.plot3d_canvas.ax.plot(self.plot_trajectory[:,0], self.plot_trajectory[:,1], self.plot_trajectory[:,2], color = 'b', linewidth=2.0)
        self.plot3d_toolbar = NavigationToolbar2QT(self.plot3d_canvas,self.centralwidget)
        geo = self.PlotNavPosition.geometry()
        self.plot3d_toolbar.setGeometry(geo)

        # add range slider even        
        
        
    # add button events
    def buttonEvents(self):
        self.ConnectButton.clicked.connect(self.connectPort)
        self.ClearPlotButton.clicked.connect(self.clearPlot)
        self.StartCSVButton.clicked.connect(self.saveCSV)
        self.LoadCSVButton.clicked.connect(self.loadCSV)

        self.Enable_ConnectByCOM.clicked.connect(self.EnableCom)
        self.Enable_ConnectByMAC.clicked.connect(self.EnableMac)

        self.Enable_YUp.clicked.connect(self.SetYUp)
        self.Enable_ZUp.clicked.connect(self.SetZUp)

        self.PlotRangeFrom.valueChanged.connect(self.PlotRangeFromChanged)
        self.PlotRangeTo.valueChanged.connect(self.PlotRangeToChanged)
        # self.PlotRangeFrom.sliderReleased.connect(self.updatePlotRange)
        # self.PlotRangeTo.sliderReleased.connect(self.updatePlotRange)
        self.PlotRangeFromInput.editingFinished.connect(self.PlotRangeFromInputChanged)
        self.PlotRangeToInput.editingFinished.connect(self.PlotRangeToInputChanged)

        self.AnimationSpeed.valueChanged.connect(self.AnimationSpeedChanged)
        self.AnimationSpeedInput.editingFinished.connect(self.AnimationSpeedInputChanged)
        self.PlayAnimationButton.clicked.connect(self.PlayAnimation)


    # update com port list
    def updateCom(self):
        ports = list_ports.comports()
        portnames=[]
        for p in ports:
            portnames.append(p.name)
        self.ComPortSelect.addItems(portnames)
        self.ComPortSelect.addItem("Dummy")

    #------------------ events ---------------------

    def EnableCom(self):
        self.connection_type = "COM"
        self.showComMacInput()

    def EnableMac(self):
        self.connection_type = "MAC"
        self.showComMacInput()

    
    def update_axis_range(self):
        if self.plot_trajectory.shape[0] >= 1:
            min_x = np.amin(self.plot_trajectory[:, 0])
            min_y = np.amin(self.plot_trajectory[:, 1])
            min_z = np.amin(self.plot_trajectory[:, 2])
            max_x = np.amax(self.plot_trajectory[:, 0])
            max_y = np.amax(self.plot_trajectory[:, 1])
            max_z = np.amax(self.plot_trajectory[:, 2])
            range_x = np.absolute(max_x - min_x)
            range_y = np.absolute(max_y - min_y)
            range_z = np.absolute(max_z - min_z)
            max_range = np.maximum(np.maximum(range_x, range_y), range_z)
            self.plot3d_canvas.ax.set_xlim(min_x, min_x + max_range)
            if self.axis_up == "Y":
                self.plot3d_canvas.ax.set_zlim(min_y, min_y + max_range)
                self.plot3d_canvas.ax.set_ylim(min_z, min_z + max_range)
            else:
                self.plot3d_canvas.ax.set_ylim(min_y, min_y + max_range)
                self.plot3d_canvas.ax.set_zlim(min_z, min_z + max_range)

    def update_3d_plot(self):
        if self.plot_trajectory.shape[0] >= 1:
            self.plot3d_canvas.ax.clear()

            # y up
            if self.axis_up == "Y":
                self.plot3d_canvas.ax.plot(self.plot_trajectory[:,0], self.plot_trajectory[:,2], self.plot_trajectory[:,1], color = 'b', linewidth=2.0)
            # z up
            else:
                self.plot3d_canvas.ax.plot(self.plot_trajectory[:,0], self.plot_trajectory[:,1], self.plot_trajectory[:,2], color = 'b', linewidth=2.0)
        
            
        self.plot3d_canvas.draw()
    

    def connectPort(self):
        # self.enable_plot2d = self.Enable2DPlot.isChecked()
        # self.enable_plot3d = True
        self.enable_log = self.EnableLog.isChecked()
        self.com_port_name = self.ComPortSelect.currentText()
        self.connection_mac_address = self.InputMacAddress.text()
        self.ComStatusDisplay.setText("Connecting...") 
        self.data_count = 0   
        self.clearPlot()  

        def update_3dplot_process():
            if self.drawing:
                try:
                    self.updatePlotRange(update_axis_range=True)
                except:
                    pass

        
        if self.connection_type=="COM" and self.com_port_name == 'Dummy':
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
                    # if self.enable_plot2d:
                    #     self.trajectory2d = np.append(self.trajectory2d,[[self.current_x,self.current_y]],axis=0)
                    # if self.enable_plot3d:
                    self.trajectory3d = np.append(self.trajectory3d,[[self.current_x,self.current_y,self.current_z]],axis=0)
                        
                        # self.fig3d= px.line_3d(data_frame=self.trajectory3d, x=0, y=1, z=2)

                    self.data_count += 1
                    self.DataCountDisplay.setText(str(self.data_count))

                    # log trajectory
                    if self.enable_log:
                        # if self.enable_plot3d and self.trajectory3d.shape[0] >= 1:
                        if self.trajectory3d.shape[0] >= 1:
                            print(self.trajectory3d[-1])
                        # elif self.enable_plot2d and self.trajectory2d.shape[0] >= 1:
                        #     print(self.trajectory2d[-1])
                            

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
            
            self.connection = Connection(type=self.connection_type, port=self.com_port_name, baud=9600)

            if self.connection_type == "COM":
                self.connection = Connection(type=self.connection_type, port=self.com_port_name, baud=9600)
            elif self.connection_type == "MAC":
                self.connection = Connection(type=self.connection_type, address=self.connection_mac_address, port="0")

            self.connection.connect()
           
            # self.serial = Serial(self.com_port_name,9600)
         
            # change status to connected
            self.connected = True
            # display connected
            self.displayConnected()
            
            time.sleep(0.1)
            
            # receive and draw
            self.connection.send(b'esatraj_start')
            # self.serial.write(b'esatraj_start')

            def receive_traj():
                while self.connected:
                    try:
                        data_raw = self.connection.read()
                        # data_raw = self.serial.readline()
                        data = data_raw.decode()

                        if self.enable_log:
                            print(data)

                        point = data.split('/')
                        x = float(point[0])
                        y = float(point[1])
                        z = float(point[2])

                        self.data_count += 1
                        self.DataCountDisplay.setText(str(self.data_count))

                        # if self.enable_plot2d:
                        #     self.trajectory2d = np.append(self.trajectory2d,[[x,y]],axis=0)
                        # if self.enable_plot3d:
                        self.trajectory3d = np.append(self.trajectory3d,[[x,z,y]],axis=0)

                        if self.data_count %10 == 0:
                            self.update_3d_plot()
                            self.updatePlotRange(True,0,True,self.trajectory3d.shape[0])
                        

                    except:
                        pass      
                try:
                    self.connection.send(b'esatraj_stop')
                    # self.serial.write(b'esatraj_stop')
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

        # y up
        if self.axis_up == "Y":
            self.plot3d_canvas.ax.set_ylabel('Z')
            self.plot3d_canvas.ax.set_zlabel('Y')

        # z up
        else:
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
                self.connection.disconnect()
                # self.serial.close()
            except:
                pass
            self.connected = False
            
        
        # display disconnected
        if not self.connected:
            self.displayDisconnected()


    def displayConnected(self):
        if self.connection_type == "COM":
            self.ComStatusDisplay.setText(self.com_port_name +" Connected")
        elif self.connection_type == "MAC":
            self.ComStatusDisplay.setText(self.connection_mac_address +" Connected")
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
            self.trajectory3d = np_array[:,0:3]
            print(self.trajectory3d)
            self.data_count = np_array.shape[0]
            self.DataCountDisplay.setText(str(self.data_count))
            self.plot3d_canvas.ax.set_title(path)
            self.PlotRangeFrom.setValue(0)
            self.PlotRangeTo.setValue(self.data_count)
            self.updatePlotRange(True, 0, True, self.data_count, True)
        except:
            if self.enable_log:
                print("Unable to open CSV file")

        # print(path)
        # print(np_array)


    def SetYUp(self):
        self.axis_up = "Y"
        self.clearPlot()
        self.updatePlotRange(update_axis_range=True)

    def SetZUp(self):
        self.axis_up = "Z"
        self.clearPlot()
        self.updatePlotRange(update_axis_range=True)

    def updatePlotRange(self,set_start=False, start=0,  set_end=False, end=0, update_axis_range=False):
        to_traj_end = False
        if set_start:
            plot_start=start
        else:
            plot_start = self.PlotRangeFrom.value() 
        
        if set_end:
            plot_end = end
        else:
            plot_end = self.PlotRangeTo.value()
        traj_length = self.trajectory3d.shape[0]

        # if range to is in maximum value, keep extend plot
        if self.PlotRangeTo.value() >= self.PlotRangeTo.maximum():
            to_traj_end = True


        self.PlotRangeFrom.setMaximum(traj_length)
        self.PlotRangeTo.setMaximum(traj_length)

        if to_traj_end:
            self.PlotRangeTo.setValue(traj_length)


        if plot_start >= traj_length:
            plot_start = traj_length -1

        if plot_start < 0:
            plot_start = 0

        if plot_start > plot_end:
            plot_end = plot_start
        

        if plot_end < plot_start:
            plot_start = plot_end

        self.PlotRangeFrom.setValue(plot_start)
        self.PlotRangeTo.setValue(plot_end)
        self.PlotRangeFromInput.setText(str(plot_start))
        self.PlotRangeToInput.setText(str(plot_end))


        if plot_end-plot_start >= 1:
            self.plot_trajectory = self.trajectory3d[plot_start:plot_end,:]
        else:
            self.plot_trajectory = np.empty((0,3))

        if update_axis_range:
            self.update_axis_range()
        self.update_3d_plot()
    
    def updateAnimationSpeed(self,speed):
        if speed < 1:
            speed = 1

        if speed > 1000:
            speed = 1000

        self.animation_speed = speed
        self.AnimationSpeedInput.setText(str(speed))
        self.AnimationSpeed.setValue(speed)


    def PlayAnimation(self):
        if not self.playing_animation:
            def play():
                start_pos = self.PlotRangeFrom.value()
                traj_length = self.trajectory3d.shape[0]

                if self.PlotRangeTo.value() >= traj_length:
                    end_pos = start_pos
                else:
                    end_pos = self.PlotRangeTo.value()


                interval = self.animation_speed
                while end_pos < traj_length:
                    end_pos += interval
                    if end_pos > traj_length:
                        end_pos = traj_length
                    self.updatePlotRange(True,start_pos,True,end_pos)
                    time.sleep(0.05)
                    if not self.playing_animation:
                        break
                self.PlayAnimationButton.setText("Play Animation")
                

            self.playing_animation = True
            self.PlayAnimationButton.setText("Stop Animation")
            threading.Thread(target=play).start()
        
        else:
            self.playing_animation = False
            self.PlayAnimationButton.setText("Play Animation")


    def PlotRangeFromChanged(self):
        # self.PlotRangeFromInput.setText(str(self.PlotRangeFrom.value()))
        self.updatePlotRange(True,self.PlotRangeFrom.value())

    def PlotRangeToChanged(self):
        # self.PlotRangeToInput.setText(str(self.PlotRangeTo.value()))
        self.updatePlotRange(False,0,True,self.PlotRangeTo.value())
    
    def PlotRangeFromInputChanged(self):
        self.updatePlotRange(True,int(self.PlotRangeFromInput.text()))

    def PlotRangeToInputChanged(self):
        self.updatePlotRange(False,0,True,int(self.PlotRangeToInput.text()))

    def AnimationSpeedChanged(self):
        self.updateAnimationSpeed(self.AnimationSpeed.value())

    def AnimationSpeedInputChanged(self):
        self.updateAnimationSpeed(int(self.AnimationSpeedInput.text()))
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = ESATraj()
    ui.setupUi(window)
    ui.init()
    # window.closeEvent = ui.close
    window.show()
    sys.exit(app.exec_())
