from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from ihesync.ui import about_dialog
from ihesync.ui import progress_dialog
from ihesync.ui import sync_dialog


class SyncDialog(QtWidgets.QDialog, sync_dialog.Ui_SyncDialog):
    confirm_signal = QtCore.pyqtSignal()
    reject_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SyncDialog, self).__init__(parent)
        self.setupUi(self)
        self.old_domains = []
        self.new_domains = []
        self.old_docs = []
        self.new_docs = []

    def accept(self):
        self.confirm_signal.emit()
        super().accept()

    def reject(self):
        self.reject_signal.emit()
        super().reject()

    def main(self):
        txt = "<p>No domain to synchronize</p>"

        if len(self.new_domains) > 0:
            newd = ", ".join(self.new_domains) if self.new_domains else "<i>none</i>"
            oldd = ", ".join(self.old_domains) if self.old_domains else "<i>none</i>"
            if (
                    len(set(self.old_domains) - set(self.new_domains)) > 0
                    or len(set(self.new_domains) - set(self.old_domains)) > 0
            ):
                txt = (
                    f'<p>Previous domains: <code style="color:purple">{oldd}</code>'
                    f'<br/>New domains: <code style="color:green">{newd}</code></p>'
                )
            else:
                txt = f"<p>Keep domains {newd} synchronized</p>"

        addd = list(set(self.new_domains) - set(self.old_domains))
        if len(addd) > 0:
            txt += "<p>Add {} to the synchronize process".format(", ".join(addd))
        deld = list(set(self.old_domains) - set(self.new_domains))
        if len(deld) > 0:
            txt += "<p>Delete {} to the synchronize process".format(", ".join(deld))

        self.textDomainBrowser.setText(txt)

        txt = (
            "Nothing to do :)"
            if len(self.new_docs) + len(self.old_domains) == 0
            else ""
        )

        if len(self.new_docs) > 0:
            txt += f"<h1>Download documents ({len(self.new_docs)}):</h1>"
            txt += "<ul><li>{}</li></ul>".format(
                "</li><li>".join(list(map(lambda x: x["filename"], self.new_docs)))
            )

        if len(self.old_docs) > 0:
            txt += f"<h1>Delete documents ({len(self.old_docs)}):</h1>"
            txt += "<ul><li>{}</li></ul>".format(
                "</li><li>".join(list(map(lambda x: x["filename"], self.old_docs)))
            )

        self.textDocumentsBrowser.setText(txt)

        self.show()


class ProgressSyncDialog(QtWidgets.QDialog):
    # confirm_signal = QtCore.pyqtSignal(object)
    REMOTE_INFO_TEXT = "Get remote information about document "
    SYNC_INFO_TEXT = "Synchronize ! "

    def __init__(self, text, parent=None):
        super(ProgressSyncDialog, self).__init__(parent)
        self.ui = progress_dialog.Ui_ProgressDialog()
        self.ui.setupUi(self)
        self.text = text
        self.ui.labelProgress.setText(self.text)
        self.ui.labelFilename.setText("")
        self.worker = None
        self.max_doc = 0

    def main(self, worker=None):
        self.worker = worker
        self.worker.signals.progress.connect(self.progress)
        self.max_doc = self.worker.doc_count()
        self.ui.progressBarPrepare.setMaximum(self.max_doc)
        self.show()

    @pyqtSlot()
    def on_abortButton_clicked(self):
        self.worker.abort()

    def progress(self, data):
        index, action, doc, local = data
        self.ui.labelProgress.setText(f"{self.text} {action} {index}/{self.max_doc}")
        self.ui.labelFilename.setText(doc["filename"])
        self.ui.progressBarPrepare.setValue(index)


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = about_dialog.Ui_Dialog()
        self.ui.setupUi(self)

    def main(self, worker=None):
        self.show()
