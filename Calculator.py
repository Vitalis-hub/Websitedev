# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:52:05 2020

@author: miche
"""

import sys
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QMessageBox, QAction, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSlot
from functools import partial

ERROR_MSG = 'ERROR'
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyCalc'
        self.left = 20
        self.top = 30
        self.width = 400
        self.height = 600
        
        self.initUI()
        
    def initUI(self):
        self._centralWidget = QWidget(self)
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(350,550)
        self.setCentralWidget(self._centralWidget)
        self.layout = QVBoxLayout()
        self._centralWidget.setLayout(self.layout)
        self._displayCal()
        self._pyButtons()
        #self._setDisplayText(self.text)

        
    def _displayCal(self):
        self.display = QLineEdit()
        self.text = self.display.text()
        #self.display.move(100,1000)
        self.display.setFixedHeight(70)
        self.display.setAlignment(Qt.AlignRight)
        #self.display.setGeometry(10, 50, 50, 50)
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)
        
    def _pyButtons(self):
        self.buttons = {}
        buttonLayout = QGridLayout()
        buttons = {
            'x^-1' : (0,0),
            'sin'  : (0,1),
            'cos'  : (0,2),
            'tan'  : (0,3),
            'clear': (0,4),
            "^"    : (1,0),
            'x^2'  : (1,1),
            ','    : (1,2),
            '('    : (1,3),
            ')'    : (1,4),
            'log'  : (2,0),
            '7'    : (2,1),
            '8'    : (2,2),
            '9'    : (2,3),
            '/'    : (2,4),
            'ln'   : (3,0),
            '4'    : (3,1),
            '5'    : (3,2),
            '6'    : (3,3),
            '*'    : (3,4),
            '1'    : (4,0),
            '2'    : (4,1),
            '3'    : (4,2),
            '-'    : (4,3),
            '+'    : (4,4),
            'ON'   : (5,0),
            '0'    : (5,1),
            '.'    : (5,2),
            '(-)'  : (5,3),
            '='    : (5,4),
            }
        
        for text, pos in buttons.items():
            self.buttons[text] = QPushButton(text)
            self.buttons[text].setFixedSize(50,50)
            #self.button[text].resize(100,100)
            buttonLayout.addWidget(self.buttons[text], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.layout.addLayout(buttonLayout)
    
    def _setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()
        
    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self._setDisplayText('')
    

def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
        
    return result

class CalCtrl:
    '''Calculator controller class'''
    '''
    def _setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()
        
    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText('')
    '''
    
    def __init__(self, model ,view):
        self._evaluate = model
        self._view = view
        self._signalConnection()
        
    def _calculateResult(self):
        'Evaluate Expression'
        result = self._evaluate(expression = self._view.displayText())
        self._view._setDisplayText(result)
        
    def _expression(self, txt):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + txt
        self._view._setDisplayText(expression)
        
    def _signalConnection(self):
        for text, btn in self._view.buttons.items():
            if text not in {'=', 'clear'}:
                btn.clicked.connect(partial(self._expression, text))
        
        self._view.buttons['='].clicked.connect(self._calculateResult)        
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['clear'].clicked.connect(self._view.clearDisplay)
            
                
        
         
def main():
    pycalc = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    model = evaluateExpression
    CalCtrl(model = model, view = ex)
    sys.exit(pycalc.exec_())
        
if __name__ == '__main__':
    main()