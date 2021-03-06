# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ihesync\ui\progress_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(397, 170)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/3_books_64x64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProgressDialog.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(ProgressDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelProgress = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelProgress.setObjectName("labelProgress")
        self.verticalLayout.addWidget(self.labelProgress)
        self.labelFilename = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelFilename.setObjectName("labelFilename")
        self.verticalLayout.addWidget(self.labelFilename)
        self.progressBarPrepare = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.progressBarPrepare.setFont(font)
        self.progressBarPrepare.setProperty("value", 24)
        self.progressBarPrepare.setObjectName("progressBarPrepare")
        self.verticalLayout.addWidget(self.progressBarPrepare)
        self.abortButton = QtWidgets.QPushButton(ProgressDialog)
        self.abortButton.setGeometry(QtCore.QRect(150, 130, 89, 25))
        self.abortButton.setObjectName("abortButton")

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Dialog"))
        self.labelProgress.setText(_translate("ProgressDialog", "TextLabel"))
        self.labelFilename.setText(_translate("ProgressDialog", "TextLabel"))
        self.abortButton.setText(_translate("ProgressDialog", "Abort !"))
from ihesync.ui import resources_rc
