import typing

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets

import logging

DOWNLOADED_BACKGROUND_COLOR = QtGui.QColor(214, 234, 248)




class DocumentsModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.logger = logging.getLogger()

        self.docs = data
        self.headers = ["Domain", "Local", "Total", "Title", "Link"]
        self.datakeys = ["domain", "down", "total", "title", "link"]

    def log(self):
        for i, v in enumerate(self.docs):
            self.logger.info(f"{v['domain']} = {v['checked']}")

    def checked(self) -> list:
        return list(
            map(lambda doc: doc["domain"], filter(lambda d: d["checked"], self.docs))
        )

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.docs)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def update_documents(self, val):
        (idx, action, docinfo) = val
        self.logger.info(
            f"update_documents > idx={idx} action={action} docinfo={docinfo}"
        )
        for documents in self.docs:
            if documents["domain"] == docinfo["domain"]:
                if action == "DEL":
                    documents["down"] -= 1
                elif action == "DOWN":
                    documents["down"] += 1
                documents["link"] = documents["down"] > 0

    def set_documents(self, data):
        if data is not None and len(data):
            self.docs = data
        else:
            self.docs = []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        val = self.docs[index.row()][self.datakeys[index.column()]]
        if role == Qt.DisplayRole:
            if not index.isValid() or (index.column()==4 and not self.docs[index.row()]["link"]):
                return QVariant()
            return str(val)
        elif role == Qt.TextAlignmentRole and (
                index.column() == 1 or index.column() == 2
        ):
            return Qt.AlignCenter
        elif (
                role == Qt.BackgroundRole
                and index.column() == 1
                and self.docs[index.row()]["down"] > 0
        ):
            return DOWNLOADED_BACKGROUND_COLOR
        elif role == Qt.EditRole:
            return None
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                return Qt.Checked if self.docs[index.row()]["checked"] else Qt.Unchecked
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.column() == 0:
            return (
                    Qt.ItemIsEnabled
                    | Qt.ItemIsEditable
                    | Qt.ItemIsUserCheckable
                    | Qt.ItemIsSelectable
            )
        else:
            return Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            self.logger.info(
                f"setData {index.row()} = {self.docs[index.row()]['checked']} - value {value}"
            )
            self.docs[index.row()]["checked"] = value == QtCore.Qt.Checked
            return True
        return False

    def headerData(
            self, section: int, orientation: Qt.Orientation, role: int = ...
    ) -> typing.Any:
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
