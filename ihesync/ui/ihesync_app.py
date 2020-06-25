# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ihesync_app.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("IHE TF Synchronizer")
        MainWindow.resize(800, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 780, 630))
        self.tabWidget.setObjectName("tabWidget")
        self.tabDomains = QtWidgets.QWidget()
        self.tabDomains.setObjectName("tabDomains")
        self.checkComments = QtWidgets.QCheckBox(self.tabDomains)
        self.checkComments.setGeometry(QtCore.QRect(10, 250, 210, 30))
        self.checkComments.setObjectName("checkComments")
        self.groupBox = QtWidgets.QGroupBox(self.tabDomains)
        self.groupBox.setGeometry(QtCore.QRect(10, 90, 241, 141))
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
        self.labelDomainCountValue.setIndent(5)
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
        self.labelDocumentCountValue.setIndent(5)
        self.labelDocumentCountValue.setObjectName("labelDocumentCountValue")
        self.gridLayout.addWidget(self.labelDocumentCountValue, 1, 1, 1, 1)
        self.labelLocalFilesCountValue = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLocalFilesCountValue.setText("")
        self.labelLocalFilesCountValue.setIndent(5)
        self.labelLocalFilesCountValue.setObjectName("labelLocalFilesCountValue")
        self.gridLayout.addWidget(self.labelLocalFilesCountValue, 2, 1, 1, 1)
        self.syncButton = QtWidgets.QPushButton(self.tabDomains)
        self.syncButton.setGeometry(QtCore.QRect(70, 310, 120, 40))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/sync.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.syncButton.setIcon(icon)
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
        self.newDocsGroupBox = QtWidgets.QGroupBox(self.tabDomains)
        self.newDocsGroupBox.setGeometry(QtCore.QRect(10, 510, 261, 80))
        self.newDocsGroupBox.setObjectName("newDocsGroupBox")
        self.newDocLabel = QtWidgets.QLabel(self.newDocsGroupBox)
        self.newDocLabel.setGeometry(QtCore.QRect(50, 40, 191, 20))
        self.newDocLabel.setObjectName("newDocLabel")
        self.newDocIcolabel = QtWidgets.QLabel(self.newDocsGroupBox)
        self.newDocIcolabel.setGeometry(QtCore.QRect(10, 40, 31, 20))
        self.newDocIcolabel.setText("")
        self.newDocIcolabel.setPixmap(QtGui.QPixmap(":/img/info2.svg"))
        self.newDocIcolabel.setObjectName("newDocIcolabel")
        self.tabWidget.addTab(self.tabDomains, "")
        self.tabConf = QtWidgets.QWidget()
        self.tabConf.setObjectName("tabConf")
        self.Logging = QtWidgets.QGroupBox(self.tabConf)
        self.Logging.setGeometry(QtCore.QRect(10, 270, 751, 161))
        self.Logging.setFlat(False)
        self.Logging.setObjectName("Logging")
        self.debugRadioButton = QtWidgets.QRadioButton(self.Logging)
        self.debugRadioButton.setGeometry(QtCore.QRect(130, 30, 112, 25))
        self.debugRadioButton.setObjectName("debugRadioButton")
        self.infoRadioButton = QtWidgets.QRadioButton(self.Logging)
        self.infoRadioButton.setGeometry(QtCore.QRect(260, 30, 112, 25))
        self.infoRadioButton.setObjectName("infoRadioButton")
        self.errorRadioButton = QtWidgets.QRadioButton(self.Logging)
        self.errorRadioButton.setGeometry(QtCore.QRect(380, 30, 112, 25))
        self.errorRadioButton.setObjectName("errorRadioButton")
        self.textLoggingFilename = QtWidgets.QTextEdit(self.Logging)
        self.textLoggingFilename.setGeometry(QtCore.QRect(130, 70, 341, 30))
        self.textLoggingFilename.setObjectName("textLoggingFilename")
        self.openLogPushButton = QtWidgets.QPushButton(self.Logging)
        self.openLogPushButton.setGeometry(QtCore.QRect(240, 110, 100, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/edit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openLogPushButton.setIcon(icon1)
        self.openLogPushButton.setObjectName("openLogPushButton")
        self.deleteLogPushButton = QtWidgets.QPushButton(self.Logging)
        self.deleteLogPushButton.setGeometry(QtCore.QRect(130, 110, 100, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteLogPushButton.setIcon(icon2)
        self.deleteLogPushButton.setObjectName("deleteLogPushButton")
        self.labelLogLevel = QtWidgets.QLabel(self.Logging)
        self.labelLogLevel.setGeometry(QtCore.QRect(10, 30, 67, 25))
        self.labelLogLevel.setObjectName("labelLogLevel")
        self.changeLogPushButton = QtWidgets.QPushButton(self.Logging)
        self.changeLogPushButton.setGeometry(QtCore.QRect(490, 70, 120, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/change.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeLogPushButton.setIcon(icon3)
        self.changeLogPushButton.setObjectName("changeLogPushButton")
        self.labelLogLevel_2 = QtWidgets.QLabel(self.Logging)
        self.labelLogLevel_2.setGeometry(QtCore.QRect(10, 70, 111, 25))
        self.labelLogLevel_2.setObjectName("labelLogLevel_2")
        self.directoryGroupBox = QtWidgets.QGroupBox(self.tabConf)
        self.directoryGroupBox.setGeometry(QtCore.QRect(10, 10, 751, 241))
        self.directoryGroupBox.setObjectName("directoryGroupBox")
        self.labelConfDirectory = QtWidgets.QLabel(self.directoryGroupBox)
        self.labelConfDirectory.setGeometry(QtCore.QRect(10, 40, 151, 20))
        self.labelConfDirectory.setObjectName("labelConfDirectory")
        self.textConfDir = QtWidgets.QTextEdit(self.directoryGroupBox)
        self.textConfDir.setGeometry(QtCore.QRect(10, 70, 410, 30))
        self.textConfDir.setObjectName("textConfDir")
        self.reloadConfButton = QtWidgets.QPushButton(self.directoryGroupBox)
        self.reloadConfButton.setGeometry(QtCore.QRect(490, 70, 120, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reloadConfButton.setIcon(icon4)
        self.reloadConfButton.setObjectName("reloadConfButton")
        self.labelConfOutputdir = QtWidgets.QLabel(self.directoryGroupBox)
        self.labelConfOutputdir.setGeometry(QtCore.QRect(10, 120, 410, 20))
        self.labelConfOutputdir.setObjectName("labelConfOutputdir")
        self.textDocDir = QtWidgets.QTextEdit(self.directoryGroupBox)
        self.textDocDir.setGeometry(QtCore.QRect(10, 150, 410, 30))
        self.textDocDir.setObjectName("textDocDir")
        self.confSelectButton = QtWidgets.QPushButton(self.directoryGroupBox)
        self.confSelectButton.setGeometry(QtCore.QRect(420, 70, 50, 30))
        self.confSelectButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.confSelectButton.setIcon(icon5)
        self.confSelectButton.setObjectName("confSelectButton")
        self.docSelectButton = QtWidgets.QPushButton(self.directoryGroupBox)
        self.docSelectButton.setGeometry(QtCore.QRect(420, 150, 50, 30))
        self.docSelectButton.setText("")
        self.docSelectButton.setIcon(icon5)
        self.docSelectButton.setObjectName("docSelectButton")
        self.aboutPushButton = QtWidgets.QPushButton(self.tabConf)
        self.aboutPushButton.setGeometry(QtCore.QRect(660, 550, 100, 30))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutPushButton.setIcon(icon6)
        self.aboutPushButton.setObjectName("aboutPushButton")
        self.tabWidget.addTab(self.tabConf, "")
        self.label_ihewebsite = QtWidgets.QLabel(self.centralwidget)
        self.label_ihewebsite.setGeometry(QtCore.QRect(20, 10, 601, 21))
        self.label_ihewebsite.setObjectName("label_ihewebsite")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
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
        self.newDocsGroupBox.setTitle(_translate("MainWindow", "NEW !"))
        self.newDocLabel.setText(_translate("MainWindow", "x new documents"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDomains), _translate("MainWindow", "domains"))
        self.Logging.setTitle(_translate("MainWindow", "Logging"))
        self.debugRadioButton.setText(_translate("MainWindow", "Debug"))
        self.infoRadioButton.setText(_translate("MainWindow", "Info"))
        self.errorRadioButton.setText(_translate("MainWindow", "Error"))
        self.openLogPushButton.setText(_translate("MainWindow", "open"))
        self.deleteLogPushButton.setText(_translate("MainWindow", "delete"))
        self.labelLogLevel.setText(_translate("MainWindow", "Level"))
        self.changeLogPushButton.setText(_translate("MainWindow", "change"))
        self.labelLogLevel_2.setText(_translate("MainWindow", "Log file name"))
        self.directoryGroupBox.setTitle(_translate("MainWindow", "Directories"))
        self.labelConfDirectory.setText(_translate("MainWindow", "configuration & log"))
        self.reloadConfButton.setText(_translate("MainWindow", "reload"))
        self.labelConfOutputdir.setText(_translate("MainWindow", "documents"))
        self.aboutPushButton.setText(_translate("MainWindow", "About..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConf), _translate("MainWindow", "configuration"))
        self.label_ihewebsite.setText(_translate("MainWindow", "TextLabel"))
from ihesync.ui import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())