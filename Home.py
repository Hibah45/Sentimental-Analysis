from PyQt5 import QtCore, QtGui, QtWidgets
from TwitterAnalysis import Ui_TwitterAnalysis

class Ui_Dialog(object):

    def logincheck(self):
        try:
            unm = self.unm.text()
            pwd = self.pwd.text()
            if unm == "" or unm == "null" or pwd == "" or pwd == "null":
                self.showMessageBox("Information", "Please fill out all fields")
            else:
                if unm == "admin" and pwd == "admin":
                    self.home = QtWidgets.QDialog()
                    self.ui = Ui_TwitterAnalysis()
                    self.ui.setupUi(self.home)
                    self.home.show()
                    Dialog.hide()
                else:
                    self.showMessageBox("Information", "Invalid Credentials..!")
        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
            print(e)

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(682, 585)
        Dialog.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 591, 91))
        self.label.setStyleSheet("\n"
"font: 20pt \"Franklin Gothic Heavy\";")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 190, 211, 241))
        self.label_3.setStyleSheet("image: url(../Twitter/images/Twitter3.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(440, 180, 141, 50))
        self.label_4.setStyleSheet("font: 14pt \"Franklin Gothic Heavy\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(380, 255, 101, 21))
        self.label_5.setStyleSheet("font: 12pt \"Franklin Gothic Heavy\";")
        self.label_5.setObjectName("label_5")
        self.unm = QtWidgets.QLineEdit(Dialog)
        self.unm.setGeometry(QtCore.QRect(380, 280, 191, 31))
        self.unm.setObjectName("unm")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(380, 331, 91, 20))
        self.label_6.setStyleSheet("font: 12pt \"Franklin Gothic Heavy\";")
        self.label_6.setObjectName("label_6")
        self.pwd = QtWidgets.QLineEdit(Dialog)
        self.pwd.setGeometry(QtCore.QRect(380, 360, 191, 31))
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(420, 410, 101, 31))
        self.pushButton.setStyleSheet("font: 75 14pt \"Tahoma\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.logincheck)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sentiment Analysis"))
        self.label.setText(_translate("Dialog", "Sentiment Analysis using Twitter Dataset"))
        self.label_4.setText(_translate("Dialog", "Admin Login"))
        self.label_5.setText(_translate("Dialog", "User Name"))
        self.label_6.setText(_translate("Dialog", "Password"))
        self.pushButton.setText(_translate("Dialog", "LOGIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

