# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sync_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SyncDialog(object):
    def setupUi(self, SyncDialog):
        SyncDialog.setObjectName("SyncDialog")
        SyncDialog.resize(527, 619)
        SyncDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(SyncDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.domainLabel = QtWidgets.QLabel(SyncDialog)
        self.domainLabel.setObjectName("domainLabel")
        self.verticalLayout.addWidget(self.domainLabel)
        self.textDomainBrowser = QtWidgets.QTextBrowser(SyncDialog)
        self.textDomainBrowser.setObjectName("textDomainBrowser")
        self.verticalLayout.addWidget(self.textDomainBrowser)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.docLabel = QtWidgets.QLabel(SyncDialog)
        self.docLabel.setObjectName("docLabel")
        self.verticalLayout.addWidget(self.docLabel)
        self.textDocumentsBrowser = QtWidgets.QTextBrowser(SyncDialog)
        self.textDocumentsBrowser.setObjectName("textDocumentsBrowser")
        self.verticalLayout.addWidget(self.textDocumentsBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SyncDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SyncDialog)
        self.buttonBox.accepted.connect(SyncDialog.accept)
        self.buttonBox.rejected.connect(SyncDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SyncDialog)

    def retranslateUi(self, SyncDialog):
        _translate = QtCore.QCoreApplication.translate
        SyncDialog.setWindowTitle(_translate("SyncDialog", "Confirm actions..."))
        SyncDialog.setToolTip(_translate("SyncDialog", "Confirm files to download and/or to delete"))
        self.domainLabel.setText(_translate("SyncDialog", "IHE domains"))
        self.docLabel.setText(_translate("SyncDialog", "Documents"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SyncDialog = QtWidgets.QDialog()
    ui = Ui_SyncDialog()
    ui.setupUi(SyncDialog)
    SyncDialog.show()
    sys.exit(app.exec_())
