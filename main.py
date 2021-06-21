import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QStandardItem
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QLabel, QWidget, QLineEdit, QGridLayout, \
    QPushButton, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QCheckBox
from ArubaSshModule import ArubaSSH

class ConnectSsh(QThread):
    conResult = pyqtSignal(str)
    def __init__(self, host, uname, pwd):
        super().__init__()
        self._run_flag = True
        self.host = host
        self.uname = uname
        self.pwd = pwd

    def run(self):
        # ssh connection
        try:
            arubaSsh = ArubaSSH(self.host,self.uname, self.pwd)
            print(self.host+self.uname+self.pwd)
            result = arubaSsh.connectSsh()
            self.conResult.emit(result)
            self.stop()
        except:
            print("SSH Error")

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class ConfigWidget(QWidget):
    def __init__(self):
        super(ConfigWidget, self).__init__()
        self.setWindowTitle("Config Manager")
        self.resize(800,400)
        self.setWindowIcon(QIcon("ico.png"))
        # self.setGeometry(400,80,400,400)
        self.hostNameLbl = QLabel("Hostname",self)
        self.hostNameEdit = QLineEdit(self)
        self.hostNameLbl.setBuddy(self.hostNameEdit)
        self.userNameLbl = QLabel("Username", self)
        self.userNameEdit = QLineEdit(self)
        self.userNameLbl.setBuddy(self.userNameEdit)
        self.showLbl = QLabel()
        self.showLbl.setText("output")
        self.pwdLbl = QLabel("Password",self)
        self.pwdEdit = QLineEdit(self)
        self.pwdLbl.setBuddy(self.pwdEdit)
        self.connectBtn = QPushButton("Connect", self)
        self.connectBtn.clicked.connect(self.startSSH)
        self.hostTable = QTableWidget(self)
        self.hostTable.setAlternatingRowColors(True)
        # self.hostTable.setRowCount()
        self.hostTable.rowCount()
        self.colList = ['✔', 'Host','Status','SW Ver','Model','Config','Delete','Backup']
        self.hostTable.setHorizontalHeaderLabels(self.colList)
        self.hostTable.setColumnCount(len(self.colList))

        self.checkBox = QCheckBox()
        self.checkBox.setChecked(False)
        # self.hostTable.set
        row_1 = ['001', 'John', 30, 'Male', 'Street No 2','test1','test2']
        row_2 = ['001', 'John', 30, 'Male', 'Street No 2','test1','test2']
        self.rows = []

        self.addTableRow(self.hostTable, self.rows)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.hostNameLbl,0,0)
        self.mainLayout.addWidget(self.hostNameEdit,1,0)
        self.mainLayout.addWidget(self.userNameLbl, 0, 1)
        self.mainLayout.addWidget(self.userNameEdit, 1, 1)
        self.mainLayout.addWidget(self.pwdLbl, 0, 2)
        self.mainLayout.addWidget(self.pwdEdit, 1, 2)
        self.mainLayout.addWidget(self.connectBtn, 1, 5)
        self.mainLayout.addWidget(self.showLbl, 2, 0)
        self.mainLayout.addWidget(self.hostTable,3,0,5,0)

    def addTableRow(self, table, row_data):
        for row in row_data:
            rowCount = table.rowCount()
            table.setRowCount(rowCount+1)
            col = 1
            for item in row:
                cell = QTableWidgetItem(str(item))
                table.setCellWidget(rowCount, 0, self.checkBox)
                table.setItem(rowCount, col, cell)
                col += 1
    def startSSH(self):
        print("connect")
        try:
            self.sshThread = ConnectSsh(self.hostNameEdit.text(), self.userNameEdit.text(), self.pwdEdit.text())
            self.sshThread.conResult.connect(self.getSshOutput)
            self.sshThread.start()
        except:
            print("start SSH Error")

    @pyqtSlot(str)
    def getSshOutput(self, result):
        host = self.hostNameEdit.text()
        print(result + " " + host)
        new_row = [str(host), result]
        self.rows.append(new_row)
        self.showLbl.setText(result + " " + host)
        self.showLbl.adjustSize()
        self.showResult(result + " " + host)
        self.sshThread.stop()
        self.addTableRow(self.hostTable, self.rows)


    def showResult(self, result):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Result")
        msgBox.setText(result)
        msgBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ConfigWidget()
    ui.show()
    sys.exit(app.exec())
