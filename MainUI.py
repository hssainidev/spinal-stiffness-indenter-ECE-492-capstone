from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import time

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

class MainWindow(QMainWindow):
    
    def __init__(self, UIFileName):
        QMainWindow.__init__(self)
        loadUi(UIFileName,self)
        self.setWindowTitle("Indenter Control Panel")
        self.pushButton_generate_random_signal.clicked.connect(self.updateGraph)
        self.pushButton_clear_graph.clicked.connect(self.clearGraph)
        self.LoadButton.clicked.connect(self.loadFile)
        self.SaveButton.clicked.connect(self.saveFile)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.spinBox.valueChanged.connect(self.show_result)
        self.setButton.clicked.connect(self.display_force)
        
        self.forwardButton.clicked.connect(self.jogForward)
        self.forwardButton.toggle()
        # setting auto repeat
        self.forwardButton.setAutoRepeat(True)
        # setting interval time 500 milliseconds
        self.forwardButton.setAutoRepeatInterval(1)
        
        self.backwardButton.clicked.connect(self.jogBack)
        # setting auto repeat
        self.backwardButton.setAutoRepeat(True)
        # setting interval time 500 milliseconds
        self.backwardButton.setAutoRepeatInterval(1)
        self.backwardButton.toggle()


        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)



    def updateGraph(self):
        f = random.randint(1, 50)
        length_of_signal = 10000
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosine', 'sine'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.figure.tight_layout()
        self.MplWidget.canvas.draw()
        

    def clearGraph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.legend(('cosine', 'sine'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.draw()
        self.forceTextEdit.setText('Cleared graph')


    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV File (*.csv)", options=options)
        if fileName:
            print(fileName)


    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            print(fileName)

    def show_result(self):
        value = self.spinBox.value()
        
    def display_force(self):
        self.forceTextEdit.setText('Applying force of: ' + str(self.spinBox.value()) + ' N')
    
    def jogForward(self):
        print("being moved forward")
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(8, GPIO.HIGH) # Turn on
        time.sleep(.001) # Sleep for 1 second
        GPIO.output(8, GPIO.LOW) # Turn off
        time.sleep(.001) # Sleep for 1 second

    def jogBack(self):  
        print("being moved backward")
        GPIO.setup(10, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(8, GPIO.HIGH) # Turn on
        time.sleep(.001) # Sleep for 1 second
        GPIO.output(8, GPIO.LOW) # Turn off
        time.sleep(.001) # Sleep for 1 second

    

        
        

        