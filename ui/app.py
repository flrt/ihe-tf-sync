from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import sys
import os

import session
import helpers
import ui.ihesync_app
import ui.prepare_dialog

from ui.dialogs import SyncDialog
from ui import documents_model

from ui import sync_worker, dialogs
import logging

import sync

VERSION = 1.0
DOMAIN_DICT = {'CARD': 'Cardiology', 'DENT': 'Dental', 'ENDO': 'Endoscopy', 'EYECARE': 'Eye Care',
               'ITI': 'IT Infrastructure', 'LAB': 'Laboratory (obsolete see PALM)',
               'PALM': 'Pathology and Laboratory Medicine',
               'PAT': 'Anatomic Pathology', 'PCC': 'Patient Care Coordination', 'PCD': 'Patient Care Device',
               'PHARMACY': 'Pharmacy', 'PHDSC': '', 'QRPH': 'Quality, Research and Public Health',
               'QUALITY': '', 'RAD': 'Radiology', 'RO': 'Radiation Oncology', 'SUPPL': 'Supplements', 'TF': 'other'}


class Ui(QtWidgets.QMainWindow, ui.ihesync_app.Ui_MainWindow):
    def __init__(self, context, parent=None):
        super(Ui, self).__init__(parent)
        self.logger = logging.getLogger()

        self.setupUi(self)
        self.context = context
        self.changed = False
        # self.model = QtGui.QStandardItemModel(self.domainsView)
        self.label_ihewebsite.setText('Visit IHE Website : <a href="https://wwW.ihe.net">tech</a>')
        self.label_ihewebsite.setOpenExternalLinks(True)
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(4)

        self.doc_model = documents_model.DocumentsModel([])
        self.tableView.setModel(self.doc_model)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.logger.info("Starts with %d threads" % self.threadpool.maxThreadCount())

    def main(self):
        self.refresh_configuration()
        self.refresh_counts()
        self.show()

        if self.context.local_file_count_ondisk != self.context.local_file_count:
            msg = QMessageBox.about(self, "Information...",
                                    (f"Out of sync ! Local files on disk {self.context.local_file_count_ondisk}"
                                     f" vs in configuration {self.context.local_file_count}\n"
                                     f" Sync needed"))
            # msg.setIcon(QMessageBox.Warning)

    def refresh_public_comment(self):
        state = QtCore.Qt.Checked if self.context.sync.public_comment else QtCore.Qt.Unchecked
        self.checkComments.setCheckState(state)

    def refresh_last_checked(self):
        if self.context.sync.last_check:
            self.labelLastCheckDate.setText(self.context.sync.last_check.strftime("%Y-%m-%d %H:%M"))

    def refresh_domain_list(self):
        self.labelDomainCountValue.setText(str(len(self.context.domains)))

        self.doc_model.set_documents(None)

        domains = sorted(self.context.domains, key=lambda v: v['name'])
        data = []
        for domain in domains:
            data.append({
                "checked": domain["selected"],
                "domain": domain['name'],
                "title": DOMAIN_DICT[domain['name']] if domain['name'] in DOMAIN_DICT else '',
                "down": domain['downloaded'],
                "total": domain['files']
            })

        self.logger.info(data)
        self.doc_model.set_documents(data)
        self.tableView.model().layoutChanged.emit()

    def refresh_configuration(self):
        self.textConfDir.setText(str(self.context.conf_directory))
        self.textDocDir.setText(str(self.context.doc_directory))

    def refresh_counts(self):
        self.refresh_last_checked()
        self.labelDocumentCountValue.setText(str(self.context.file_count))
        self.labelLocalFilesCountValue.setText(str(self.context.local_file_count))
        self.refresh_domain_list()

    @pyqtSlot()
    def on_textConfDir_textChanged(self):
        self.context.conf_directory = self.textConfDir.toPlainText()

    @pyqtSlot()
    def on_textDocDir_textChanged(self):
        self.context.doc_directory = self.textDocDir.toPlainText()

    @pyqtSlot()
    def on_confSelectButton_clicked(self):
        self.context.conf_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textConfDir.setText(self.context.conf_directory)
        self.changed = True

    @pyqtSlot()
    def on_docSelectButton_clicked(self):
        self.context.doc_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textDocDir.setText(self.context.doc_directory)
        self.changed = True

    @pyqtSlot()
    def on_reloadConfButton_clicked(self):
        self.context.load_configuration()
        self.refresh_counts()

    @pyqtSlot()
    def on_remoteCheckButton_clicked(self):
        self.context.check_remote()
        self.refresh_counts()

    def synchronize_dialog(self):
        sd = SyncDialog(parent=self)
        sd.confirm_signal.connect(self.on_synchronize_confirmed)
        sd.reject_signal.connect(self.on_synchronize_rejected)

        sd.old_domains = self.context.infos['old_domain']
        sd.new_domains = self.context.infos['new_domain']
        sd.old_docs = self.context.infos['to_del']
        sd.new_docs = self.context.infos['to_download']
        if len(sd.old_domains) > 0 or len(sd.new_docs) > 0:
            self.changed = True
        sd.main()

    @pyqtSlot()
    def on_syncButton_clicked(self):
        # get selected domains
        domains = self.doc_model.checked()
        self.logger.info(domains)
        self.context.prepare_sync(domains)

        pd = dialogs.ProgressSyncDialog(dialogs.ProgressSyncDialog.REMOTE_INFO_TEXT, parent=self)
        worker = sync_worker.PrepareWorker(self.context)
        worker.signals.finished.connect(pd.accept)
        worker.signals.finished.connect(self.synchronize_dialog)
        worker.signals.aborted.connect(pd.reject)
        pd.main(worker)
        self.threadpool.start(worker)

    @pyqtSlot()
    def on_synchronize_confirmed(self):
        self.context.sync.display_available_docs()
        sd = dialogs.ProgressSyncDialog(dialogs.ProgressSyncDialog.SYNC_INFO_TEXT, parent=self)
        worker = sync_worker.SyncWorker(self.context)

        worker.signals.finished.connect(sd.accept)
        # worker.signals.finished.connect()
        worker.signals.aborted.connect(sd.reject)
        sd.main(worker)
        self.threadpool.start(worker)

        self.context.confirm_sync()
        self.refresh_counts()

    @pyqtSlot()
    def on_synchronize_rejected(self):
        self.context.revert_sync()

    def closeEvent(self, event):
        # save new data
        self.logger.info(f'Close - change ? {self.changed}')
        if self.changed or self.context.no_config_file:
            self.logger.info(self.context.sync.domain_filter)
            # helpers.save_json("/tmp/refdoc.conf", self.config.sy.refdoc)
            # helpers.save_json("/tmp/doc.conf", self.config.sy.doc)

            self.context.sync.save_infos()
            self.context.sync.save_configuration()
        else:
            self.logger.info("No changes")
        event.accept()


if __name__ == '__main__':
    if not os.path.exists(sync.DEFAULT_CONF_DIR):
        os.makedirs(sync.DEFAULT_CONF_DIR)
    logging.basicConfig(filename=str(sync.DEFAULT_CONF_DIR / 'ihe-sync.log'), level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    ctx = session.Context()
    ctx.load_configuration()
    iheui = Ui(ctx)
    iheui.main()
    app.exec_()
