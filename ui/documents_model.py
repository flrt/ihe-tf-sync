import typing

from PyQt5.Qt import *
from PyQt5 import QtCore

import logging


class DocumentsModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.logger = logging.getLogger()

        self.docs = data
        self.headers = ['Domain', 'Local', 'Total', 'Title']
        self.datakeys = ['domain', 'down', 'total', 'title']

    def log(self):
        for d, i in enumerate(self.docs):
            self.logger.info(f"{d[i]['domain']} = {d[i]['checked']}")

    def checked(self) -> list:
        return list(map(lambda doc: doc['domain'], filter(lambda d: d['checked'], self.docs)))

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.docs)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 4

    def set_documents(self, data):
        if data is not None and len(data):
            self.docs = data
        else:
            self.docs = []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        val = self.docs[index.row()][self.datakeys[index.column()]]
        if role == Qt.DisplayRole:
            if not index.isValid():
                return QVariant()
            if role == Qt.EditRole:
                return None
            return str(val)
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                #self.logger.info(f"data {index.row()} = {self.docs[index.row()]['checked']} ")
                return Qt.Checked if self.docs[index.row()]["checked"] else Qt.Unchecked
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            self.logger.info(f"setData {index.row()} = {self.docs[index.row()]['checked']} - value {value}")
            self.docs[index.row()]["checked"] = (value == QtCore.Qt.Checked)
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
