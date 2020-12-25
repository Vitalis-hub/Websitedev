# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 14:03:59 2020

@author: miche
"""

import sys
from PyQt5.QtWidgets import QDockWidget, QTextEdit, QFormLayout, QCheckBox, QApplication, QWidget, QFileDialog, QPushButton, QDialog, QDialogButtonBox, QMainWindow, QAction, QLineEdit, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QIcon,  QTextCursor, QKeySequence, QTextDocument
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal

from Calculator import main

class SearchWidget(QWidget):
    submitted = pyqtSignal(str, bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QFormLayout())
        self.term_input = QLineEdit()
        self.case_checkbox = QCheckBox('Case Sensitive?')
        self.submit_button = QPushButton('search', clicked = self.on_submit)
        self.layout().addRow('search Term', self.term_input)
        self.layout().addRow('', self.case_checkbox)
        self.layout().addRow('', self.submit_button)
        
    def on_submit(self):
        term = self.term_input.text()
        case_sensitive = (self.case_checkbox.checkState() == Qt.Checked)
        self.submitted.emit(term, case_sensitive)
        #self.submitted.connect(search.Search)
        

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = ('First Pyqt Project Window')
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.textedit = QTextEdit()
        #layout = QVBoxLayout()
        #layout.addWidget(self.textedit)
        #self.setLayout(self.textedit)        
        self.setCentralWidget(self.textedit)
        
        
        mainMenu = self.menuBar()
        
        #filemenu
        fileMenu = mainMenu.addMenu('File')
        openMenu = fileMenu.addAction('Open', self.open_file)
        openMenu.setShortcut(QKeySequence.Open)
        #openMenu.triggered.connect(self.o)
        #openMenu.clicked.connect(self.open_file)
        save_action = fileMenu.addAction('Save', self.save_file)
        save_action.setShortcut(QKeySequence.Save)
        fileMenu.addSeparator()
        #save_action.triggered.connect(self)
        exitMenu = fileMenu.addAction('exit', self.close)
        exitMenu.setShortcut(QKeySequence.Quit)
        #exitMenu.triggered.connect(self.close)
        #fileMenu.addAction(exitMenu)
        
 #-----------------------------------------------------------------------------   
        #editMenu
        editMenubar = mainMenu.addMenu('Edit')
        copyMenu = QAction('copy', self)
        copyMenu.setShortcut('CTRL+O')
        copyMenu.triggered.connect(self.textedit.copy)
        editMenubar.addAction(copyMenu)
        #editMenubar.addAction('cut', self.textedit.cut)
        cutMenu = QAction('cut', self)
        cutMenu.setShortcut('CTRL+X')
        cutMenu.triggered.connect(self.textedit.cut)
        #editMenubar.addAction('undo', self.textedit.undo)
        undoMenu = QAction('undo', self)
        undoMenu.setShortcut('CTRL+Z')
        undoMenu.triggered.connect(self.textedit.undo)
        editMenubar.addAction(undoMenu)
        editMenubar.addAction(cutMenu)
        #editMenubar.addAction('redo', self.textedit.redo)
        redoMenu = QAction('redo', self)
        redoMenu.setShortcut('CTRL+SHIFT+Z')
        redoMenu.triggered.connect(self.textedit.redo)
        editMenubar.addAction(redoMenu)
#----------------------------------------------------------------------------
       
        #search menu
        searchMenu = mainMenu.addMenu('Search')
        
        toolMenu = mainMenu.addMenu('Tools')
        viewMenu = mainMenu.addMenu('View')
        
        helpMenu = mainMenu.addMenu('Help')
        questionMenu = helpMenu.addMenu('Report Issue')
        #calculator = helpMenu.addMenu('Calculator')
        #calculator.triggered.connect(main())
    
        
        #questionPage = helpMenu.questionMenu.
        '''
        self.questionBox = QLineEdit(self)
        self.questionBox.title('Type in the issue you will like us to assist you with.')
        self.questionBox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.questionBox.resize(460,400)
        '''
        
#------------------------------------------------------------------------------
        search_dock = QDockWidget('Search')
        search_widget= SearchWidget()
        search_dock.setWidget(search_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, search_dock)
        search_widget.submitted.connect(self.search)
        self.show()
      
    #save file
    def save_file(self):
        text = self.textedit.toPlainText()
        filename, _ = QFileDialog.getSaveFileName()
        if filename:
            with open(filename, 'w') as file:
                file.write(text)
                self.statusBar().showMessage(f'saved to {filename}')
                
    #open in file
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            with open(filename , 'r') as file:
                text = file.read()
            self.textedit.clear()
            self.textedit.insertPlainText(text)
            self.textedit.moveCursor(QTextCursor.Start)
            self.statusBar().showMessage(f'Editing {filename}')
    
    def search(self, term, case_sensitive = False):
        if case_sensitive:
            cor = self.textedit.find(term, QTextDocument.FindCaseSensitively)
        else:
            cor = self.textedit.find(term)
        if not cor:
            self.statusBar().showMessage('No matches Found', 2000)

        
class Dialog(QDialog):
    def __init__(self):
        
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.ok | QDialogButtonBox.cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())