import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QLabel, QWidget, QLineEdit, QGridLayout, \
    QPushButton, QMessageBox, QDialog


class ConfigWidget(QWidget):
    def __init__(self):
        super(ConfigWidget, self).__init__()
        self.setWindowTitle("Config Manager")
        self.resize(800,400)
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
        self.connectBtn.clicked.connect(self.connectssh)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.hostNameLbl,0,0)
        self.mainLayout.addWidget(self.hostNameEdit,1,0)
        self.mainLayout.addWidget(self.userNameLbl, 0, 1)
        self.mainLayout.addWidget(self.userNameEdit, 1, 1)
        self.mainLayout.addWidget(self.pwdLbl, 0, 2)
        self.mainLayout.addWidget(self.pwdEdit, 1, 2)
        self.mainLayout.addWidget(self.connectBtn, 1, 5)
        self.mainLayout.addWidget(self.showLbl, 2, 0)

    def connectssh(self):
        print("connect")
        try:
            self.showLbl.setText("Connect")
            self.showLbl.adjustSize()
            self.showResult()
        except:
            print("SSH Error")

    def showResult(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Result")
        msgBox.setText("Connected Successfully!")
        msgBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ConfigWidget()
    ui.show()
    sys.exit(app.exec())

