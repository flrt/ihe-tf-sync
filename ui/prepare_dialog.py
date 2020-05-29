# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prepare_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrepareDialog(object):
    def setupUi(self, PrepareDialog):
        PrepareDialog.setObjectName("PrepareDialog")
        PrepareDialog.resize(397, 170)
        self.verticalLayoutWidget = QtWidgets.QWidget(PrepareDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelPrepare = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelPrepare.setObjectName("labelPrepare")
        self.verticalLayout.addWidget(self.labelPrepare)
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
        self.abortButton = QtWidgets.QPushButton(PrepareDialog)
        self.abortButton.setGeometry(QtCore.QRect(150, 130, 89, 25))
        self.abortButton.setObjectName("abortButton")

        self.retranslateUi(PrepareDialog)
        QtCore.QMetaObject.connectSlotsByName(PrepareDialog)

    def retranslateUi(self, PrepareDialog):
        _translate = QtCore.QCoreApplication.translate
        PrepareDialog.setWindowTitle(_translate("PrepareDialog", "Dialog"))
        self.labelPrepare.setText(_translate("PrepareDialog", "TextLabel"))
        self.labelFilename.setText(_translate("PrepareDialog", "TextLabel"))
        self.abortButton.setText(_translate("PrepareDialog", "Abort !"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PrepareDialog = QtWidgets.QDialog()
    ui = Ui_PrepareDialog()
    ui.setupUi(PrepareDialog)
    PrepareDialog.show()
    sys.exit(app.exec_())
