# PyQt5 GUI / interface for MAX7219 LED Matrices
# www.scienceexposure.com

import sys
import math
from datetime import date

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

try:
    from LEDController.functions import MatrixFunctions
    led_matrix = MatrixFunctions()
except ImportError:
    led_matrix = None
    print('MAX7219 module or LEDController module missing. Program continuing...')

from gui_matrix import Ui_Form


class LedMatrixUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, matrixSize=64):
        super(LedMatrixUI, self).__init__()

        # Set up the user interface from Designer
        self.setupUi(self)

        self.matrixSize = matrixSize

        # Connect up the buttons
        self.pushButton.clicked.connect(self.updateMatrix)
        self.pushButton_2.clicked.connect(self.generateMatrix)

    def updateMatrix(self):
        arr = np.array(np.zeros(self.matrixSize))
        orientation = int(self.comboBox.currentText())
        led_matrix.setOrientation(orientation)

        for i in range(1, self.matrixSize + 1):
            method = getattr(self, "radioButton_%s" % i)
            a = method.isChecked()
            if a == True:
                arr[i - 1] = 1
            else:
                pass
        matrix = arr.reshape(math.sqrt(self.matrixSize),
            math.sqrt(self.matrixSize))
        led_matrix.updateMatrix(matrix)


    def generateMatrix(self):
        arr = np.array(np.zeros(self.matrixSize))

        for i in range(1, self.matrixSize + 1):
            method = getattr(self, "radioButton_%s" % i)
            a = method.isChecked()
            if a == True:
                arr[i - 1] = 1
            else:
                pass
        mx = arr.reshape(math.sqrt(self.matrixSize),
            math.sqrt(self.matrixSize))
        today = date.today()
        d = today.strftime('%d%m%Y')
        np.savetxt('%s_led_matrix.txt' % d, mx, fmt='%d', newline=',',
            delimiter=',')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LedMatrixUI()
    ui.show()
    sys.exit(app.exec_())
