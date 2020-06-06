# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ihesync_app.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 780, 630))
        self.tabWidget.setObjectName("tabWidget")
        self.tabDomains = QtWidgets.QWidget()
        self.tabDomains.setObjectName("tabDomains")
        self.checkComments = QtWidgets.QCheckBox(self.tabDomains)
        self.checkComments.setGeometry(QtCore.QRect(10, 260, 210, 30))
        self.checkComments.setObjectName("checkComments")
        self.groupBox = QtWidgets.QGroupBox(self.tabDomains)
        self.groupBox.setGeometry(QtCore.QRect(10, 90, 241, 150))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 29, 221, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelDocumentCount = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelDocumentCount.setObjectName("labelDocumentCount")
        self.gridLayout.addWidget(self.labelDocumentCount, 1, 0, 1, 1)
        self.labelDomainCountValue = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelDomainCountValue.setText("")
        self.labelDomainCountValue.setObjectName("labelDomainCountValue")
        self.gridLayout.addWidget(self.labelDomainCountValue, 0, 1, 1, 1)
        self.labelLocalFilesCount = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLocalFilesCount.setObjectName("labelLocalFilesCount")
        self.gridLayout.addWidget(self.labelLocalFilesCount, 2, 0, 1, 1)
        self.labelDomainCount = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelDomainCount.setObjectName("labelDomainCount")
        self.gridLayout.addWidget(self.labelDomainCount, 0, 0, 1, 1)
        self.labelDocumentCountValue = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelDocumentCountValue.setText("")
        self.labelDocumentCountValue.setObjectName("labelDocumentCountValue")
        self.gridLayout.addWidget(self.labelDocumentCountValue, 1, 1, 1, 1)
        self.labelLocalFilesCountValue = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLocalFilesCountValue.setText("")
        self.labelLocalFilesCountValue.setObjectName("labelLocalFilesCountValue")
        self.gridLayout.addWidget(self.labelLocalFilesCountValue, 2, 1, 1, 1)
        self.syncButton = QtWidgets.QPushButton(self.tabDomains)
        self.syncButton.setGeometry(QtCore.QRect(70, 310, 120, 40))
        self.syncButton.setObjectName("syncButton")
        self.tableView = QtWidgets.QTableView(self.tabDomains)
        self.tableView.setGeometry(QtCore.QRect(280, 20, 491, 571))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabDomains)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 241, 51))
        self.groupBox_2.setObjectName("groupBox_2")
        self.labelLastCheckDate = QtWidgets.QLabel(self.groupBox_2)
        self.labelLastCheckDate.setGeometry(QtCore.QRect(10, 25, 221, 20))
        self.labelLastCheckDate.setText("")
        self.labelLastCheckDate.setObjectName("labelLastCheckDate")
        self.tabWidget.addTab(self.tabDomains, "")
        self.tabConf = QtWidgets.QWidget()
        self.tabConf.setObjectName("tabConf")
        self.textConfDir = QtWidgets.QTextEdit(self.tabConf)
        self.textConfDir.setGeometry(QtCore.QRect(10, 60, 410, 30))
        self.textConfDir.setObjectName("textConfDir")
        self.labelConfDirectory = QtWidgets.QLabel(self.tabConf)
        self.labelConfDirectory.setGeometry(QtCore.QRect(10, 30, 410, 20))
        self.labelConfDirectory.setObjectName("labelConfDirectory")
        self.labelConfOutputdir = QtWidgets.QLabel(self.tabConf)
        self.labelConfOutputdir.setGeometry(QtCore.QRect(10, 150, 410, 20))
        self.labelConfOutputdir.setObjectName("labelConfOutputdir")
        self.textDocDir = QtWidgets.QTextEdit(self.tabConf)
        self.textDocDir.setGeometry(QtCore.QRect(10, 180, 410, 30))
        self.textDocDir.setObjectName("textDocDir")
        self.confSelectButton = QtWidgets.QPushButton(self.tabConf)
        self.confSelectButton.setGeometry(QtCore.QRect(420, 60, 50, 30))
        self.confSelectButton.setObjectName("confSelectButton")
        self.docSelectButton = QtWidgets.QPushButton(self.tabConf)
        self.docSelectButton.setGeometry(QtCore.QRect(420, 180, 50, 30))
        self.docSelectButton.setObjectName("docSelectButton")
        self.reloadConfButton = QtWidgets.QPushButton(self.tabConf)
        self.reloadConfButton.setGeometry(QtCore.QRect(10, 110, 220, 30))
        self.reloadConfButton.setObjectName("reloadConfButton")
        self.tabWidget.addTab(self.tabConf, "")
        self.label_ihewebsite = QtWidgets.QLabel(self.centralwidget)
        self.label_ihewebsite.setGeometry(QtCore.QRect(20, 10, 601, 21))
        self.label_ihewebsite.setObjectName("label_ihewebsite")
        self.remoteCheckButton = QtWidgets.QPushButton(self.centralwidget)
        self.remoteCheckButton.setGeometry(QtCore.QRect(440, 10, 120, 40))
        self.remoteCheckButton.setObjectName("remoteCheckButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkComments.setText(_translate("MainWindow", "Public comments"))
        self.groupBox.setTitle(_translate("MainWindow", "Informations"))
        self.labelDocumentCount.setText(_translate("MainWindow", "Remote documents"))
        self.labelLocalFilesCount.setText(_translate("MainWindow", "Local files"))
        self.labelDomainCount.setText(_translate("MainWindow", "Domains"))
        self.syncButton.setText(_translate("MainWindow", "Synchronize"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Last check"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDomains), _translate("MainWindow", "domains"))
        self.labelConfDirectory.setText(_translate("MainWindow", "configuration directory"))
        self.labelConfOutputdir.setText(_translate("MainWindow", "documents directory"))
        self.confSelectButton.setText(_translate("MainWindow", "..."))
        self.docSelectButton.setText(_translate("MainWindow", "..."))
        self.reloadConfButton.setText(_translate("MainWindow", "reload configuration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConf), _translate("MainWindow", "configuration"))
        self.label_ihewebsite.setText(_translate("MainWindow", "TextLabel"))
        self.remoteCheckButton.setText(_translate("MainWindow", "Remote Check"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
