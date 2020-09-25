import typing

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui
from ihesync.ui import sync_worker

import logging

DOWNLOADED_BACKGROUND_COLOR = QtGui.QColor(214, 234, 248)
ERR_COUNT_BACKGROUND_COLOR = QtGui.QColor(255, 165, 0)


class DocumentsModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.logger = logging.getLogger()

        self.docs = data
        self.headers = ["Domain", "Local", "Total", "Title", "Link"]
        self.datakeys = ["domain", "local", "total", "title", "link"]

    def log(self):
        for i, v in enumerate(self.docs):
            self.logger.info(f"model : {i} -> {v}")

    def checked(self) -> list:
        return list(
            map(lambda doc: doc["domain"], filter(lambda d: d["checked"], self.docs))
        )

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.docs)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def update_documents(self, val):
        (idx, action, docinfo, local_count) = val
        self.logger.debug(
            f"update_documents > idx={idx} action={action} local_count= {local_count} docinfo={docinfo}"
        )
        for documents in self.docs:
            if documents["domain"] == docinfo["domain"]:
                if action == sync_worker.WORKER_ACTION_DEL:
                    documents["down"] -= 1
                elif action == sync_worker.WORKER_ACTION_DOWN:
                    documents["down"] += 1
                elif action == sync_worker.WORKER_ACTION_ERR:
                    documents["error"] += 1
                documents["local"] = local_count

                documents["link"] = documents["local"] > 0

    def summary(self):
        error = sum(list(map(lambda x: x["error"], self.docs)))
        downloaded = sum(list(map(lambda x: x["down"], self.docs)))
        return downloaded, error

    def set_documents(self, data):
        if data is not None and len(data):
            self.docs = data
        else:
            self.docs.clear()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        r, c = index.row(), index.column()

        val = self.docs[r][self.datakeys[c]]
        if role == Qt.DisplayRole:
            if not index.isValid() or (c == 4 and not self.docs[r]["link"]):
                return QVariant()
            return str(val)

        if role == Qt.TextAlignmentRole and c in [1, 2]:
            return Qt.AlignCenter

        if role == Qt.BackgroundRole:
            if c == 1 and self.docs[r]["down"] >= 0:
                if self.docs[r]["checked"] and \
                        ((self.docs[r]["down"] != self.docs[r]["local"]) or \
                         (self.docs[r]["local"] != self.docs[r]["total"])):
                    return ERR_COUNT_BACKGROUND_COLOR

        if role == Qt.EditRole:
            return None

        if role == Qt.CheckStateRole:
            if c == 0:
                return Qt.Checked if self.docs[r]["checked"] else Qt.Unchecked

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
            self.logger.debug(
                f"setData {index.row()} = {self.docs[index.row()]['checked']} - value {value}"
            )
            self.docs[index.row()]["checked"] = value == QtCore.Qt.Checked
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
