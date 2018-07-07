# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BioSeq.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from DTran import proteinTranslation
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(642, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 2)
        self.BClear = QtWidgets.QPushButton(self.centralwidget)
        self.BClear.setObjectName("BClear")
        self.gridLayout.addWidget(self.BClear, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 6, 1, 1, QtCore.Qt.AlignRight)
        self.BLFASTA = QtWidgets.QPushButton(self.centralwidget)
        self.BLFASTA.setObjectName("BLFASTA")
        self.gridLayout.addWidget(self.BLFASTA, 2, 2, 1, 1)
        self.BTranslate = QtWidgets.QPushButton(self.centralwidget)
        self.BTranslate.setObjectName("BTranslate")
        self.gridLayout.addWidget(self.BTranslate, 2, 3, 1, 1)
        self.BComposition = QtWidgets.QPushButton(self.centralwidget)
        self.BComposition.setObjectName("BComposition")
        self.gridLayout.addWidget(self.BComposition, 2, 4, 1, 1)
        self.BFind = QtWidgets.QPushButton(self.centralwidget)
        self.BFind.setObjectName("BFind")
        self.gridLayout.addWidget(self.BFind, 2, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.OutSeq = QtWidgets.QTextBrowser(self.centralwidget)
        self.OutSeq.setObjectName("OutSeq")
        self.gridLayout.addWidget(self.OutSeq, 4, 1, 1, 6)
        self.InSeq = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.InSeq.setObjectName("InSeq")
        self.gridLayout.addWidget(self.InSeq, 1, 1, 1, 6, QtCore.Qt.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 642, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.BClear.clicked.connect(self.clearSeq)
        self.BLFASTA.clicked.connect(self.loadFasta)
        self.BTranslate.clicked.connect(self.seqTranslate)
        self.BComposition.clicked.connect(self.seqComposition)
        self.BFind.clicked.connect(self.seqFind)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    
    def clearSeq(self):
        
        self.InSeq.clear()
  
    
    def setSequence(self, text):
        
        self.InSeq.setPlainText(text)
  
  
    def loadFasta(self):
        
        msg = 'Choose a FASTA file'
        filePath, filtr = QtWidgets.QFileDialog.getOpenFileName(MainWindow, msg)

        if filePath: # Something was selected
            fileObj = open(filePath, 'rU')

            from Bio import SeqIO
            for entry in SeqIO.parse(fileObj, 'fasta'):
                self.setSequence(str(entry.seq))
                break

            fileObj.close()
    
    
    def seqTranslate(self):
        
        seq = self.getSequence()    
        self.clearOutput()
        self.showText('DNA sequence')
        self.showText(seq)
        self.showText('\nProtein sequence')
      
        for indent in range(3):
            proteinSeq = proteinTranslation(seq[indent:])
            proteinSeq = ''.join(proteinSeq)
            spaces = ' ' * indent
            text = '\nReading frame %d\n%s%s' % (indent, spaces, proteinSeq)
            self.showText(text)


    def seqComposition(self):
        
        self.clearOutput()
        seq = self.getSequence()
        n = 0.0
        counts = {}
        for letter in seq:
            counts[letter] = counts.get(letter, 0) + 1
            n += 1.0
    
        letters = list(counts.keys())
        letters.sort()
    
        text = "Composition:"
        for letter in letters:
            text += ' %s;%.2f%%' % (letter, counts[letter] * 100 / n)
    
        self.showText(text)
  
  
    def showText(self, text):
        
        self.OutSeq.append(text)
        
    
    def clearOutput(self):

        self.OutSeq.clear()
  
  
    def getSequence(self):
    
        seq = self.InSeq.toPlainText()
        seq = re.sub('\s+','',seq)
        seq = seq.upper()
    
        return seq
    
    
    def seqFind(self):
        
        self.clearOutput()

        query = self.lineEdit.text()
        query = query.strip()

        if not query:
            QtWidgets.QMessageBox.warning(MainWindow, "Warning",
                                          "Search sequence was blank")
            return

        seq = self.getSequence()

        self.InSeq.find(query)

        if query in seq:
            text = "Locations of %s" % (query)
            self.showText(text)
            win = len(query)
            
            for i in range(len(seq)-win):
                if seq[i:i+win] == query:
                    self.showText(' %d' % i)
        else:
            text = "Sub-sequence %s not found" % (query)
            self.showText(text)
                

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Biological sequences"))
        self.label.setText(_translate("MainWindow", "Enter 1-Letter DNA Sequence:"))
        self.BClear.setText(_translate("MainWindow", "Clear"))
        self.BLFASTA.setText(_translate("MainWindow", "Load FASTA"))
        self.BTranslate.setText(_translate("MainWindow", "Translate"))
        self.BComposition.setText(_translate("MainWindow", "Composition"))
        self.BFind.setText(_translate("MainWindow", "Find:"))
        self.label_2.setText(_translate("MainWindow", "Text Output:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

