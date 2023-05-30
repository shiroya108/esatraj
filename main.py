from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from esatraj import Ui_ESATrajWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_ESATrajWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())