# PyQt5 GUI / interface for MAX7219 LED Matrices
# www.scienceexposure.com

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
try:
    from LEDController.functions import MatrixFunctions
    led_matrix = MatrixFunctions()
except ImportError:
    print('MAX7219 module or LEDController module missing. Program continuing...')

from datetime import date

from gui_matrix import Ui_Form


class LedMatrixUI(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(LedMatrixUI, self).__init__()

        # Set up the user interface from Designer
        self.setupUi(self)

        # Connect up the buttons
        self.pushButton.clicked.connect(self.updtMat)
        self.pushButton_2.clicked.connect(self.genMatrix)

    def updtMat(self):
        arr = np.array(np.zeros(64))
        orientation = int(self.comboBox.currentText())
        led_matrix.setOrientation(orientation)

        for i in range(1, 65):
            method = getattr(self, "radioButton_%s" % i)
            a = method.isChecked()
            if a == True:
                arr[i - 1] = 1
            else:
                pass
        matrix = arr.reshape(8, 8)
        led_matrix.updateMatrix(matrix)


    def genMatrix(self):
        arr = np.array(np.zeros(64))

        for i in range(1, 65):
            method = getattr(self, "radioButton_%s" % i)
            a = method.isChecked()
            if a == True:
                arr[i-1] = 1
            else:
                pass
        mx = arr.reshape(8, 8)
        today = date.today()
        d = today.strftime('%d%m%Y')
        np.savetxt('%s_led_matrix.txt' % d, mx, fmt='%d', newline=',', delimiter=',')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LedMatrixUI()
    ui.show()
    sys.exit(app.exec_())
