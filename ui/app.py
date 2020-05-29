from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import sys

import config
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
    def __init__(self, config, parent=None):
        super(Ui, self).__init__(parent)
        self.logger = logging.getLogger()

        self.setupUi(self)
        self.config = config
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

        if self.config.local_file_count_ondisk != self.config.local_file_count:
            msg = QMessageBox.about(self, "Information...",
                                    (f"Out of sync ! Local files on disk {self.config.local_file_count_ondisk}"
                                     f" vs in configuration {self.config.local_file_count}\n"
                                     f" Sync needed"))
            # msg.setIcon(QMessageBox.Warning)

    def refresh_public_comment(self):
        state = QtCore.Qt.Checked if self.config.sy.public_comment else QtCore.Qt.Unchecked
        self.checkComments.setCheckState(state)

    def refresh_last_checked(self):
        if self.config.sy.last_check:
            self.labelLastCheckDate.setText(self.config.sy.last_check.strftime("%Y-%m-%d %H:%M"))

    # def refresh_domain_list_old(self):
    #     self.labelDomainCountValue.setText(str(len(self.config.domains)))
    #
    #     if self.model.rowCount() > 0:
    #         self.model.clear()
    #
    #     domains = sorted(self.config.domains, key=lambda v: v['name'])
    #     longuest_domain = max(map(lambda x: x['name'], domains), key=len)
    #     font = QtGui.QFont('Mono', 10, QtGui.QFont.Light)
    #     color = QtGui.QBrush(QtGui.QColor("darkblue"))
    #
    #     for domain in domains:
    #         t, d, f = domain['name'], domain['downloaded'], domain['files']
    #         item_text = f"{t:{len(longuest_domain)}}  {d:>3} / {f}"
    #
    #         item = QtGui.QStandardItem(item_text)
    #         item.setCheckable(True)
    #         if domain["selected"]:
    #             item.setCheckState(QtCore.Qt.Checked)
    #         else:
    #             item.setCheckState(QtCore.Qt.Unchecked)
    #
    #         item.setFont(font)
    #         item.setForeground(color)
    #         self.model.appendRow(item)
    #
    #     self.domainsView.setModel(self.model)

    def refresh_domain_list(self):
        self.labelDomainCountValue.setText(str(len(self.config.domains)))

        self.doc_model.set_documents(None)

        domains = sorted(self.config.domains, key=lambda v: v['name'])
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

    # def checked_domain_list(self):
    #     domains = []
    #     for index in range(self.model.rowCount()):
    #         item = self.model.item(index)
    #         if item.checkState() == QtCore.Qt.Checked:
    #             domains.append(self.config.domains[index]["name"])
    #     return domains

    def refresh_configuration(self):
        self.textConfDir.setText(str(self.config.conf_directory))
        self.textDocDir.setText(str(self.config.doc_directory))

    def refresh_counts(self):
        self.refresh_last_checked()
        self.labelDocumentCountValue.setText(str(self.config.file_count))
        self.labelLocalFilesCountValue.setText(str(self.config.local_file_count))
        self.refresh_domain_list()

    @pyqtSlot()
    def on_textConfDir_textChanged(self):
        self.config.conf_directory = self.textConfDir.toPlainText()

    @pyqtSlot()
    def on_textDocDir_textChanged(self):
        self.config.doc_directory = self.textDocDir.toPlainText()

    @pyqtSlot()
    def on_confSelectButton_clicked(self):
        self.config.conf_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textConfDir.setText(self.config.conf_directory)
        self.changed = True

    @pyqtSlot()
    def on_docSelectButton_clicked(self):
        self.config.doc_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textDocDir.setText(self.config.doc_directory)
        self.changed = True

    @pyqtSlot()
    def on_reloadConfButton_clicked(self):
        self.config.load_configuration()
        self.refresh_counts()

    @pyqtSlot()
    def on_remoteCheckButton_clicked(self):
        self.config.check_remote()
        self.refresh_counts()

    def sync_me(self):
        sd = SyncDialog(parent=self)
        sd.confirm_signal.connect(self.on_synchronize_confirmed)
        sd.reject_signal.connect(self.on_synchronize_rejected)

        sd.old_domains = self.config.infos['old_domain']
        sd.new_domains = self.config.infos['new_domain']
        sd.old_docs = self.config.infos['to_del']
        sd.new_docs = self.config.infos['to_download']
        if len(sd.old_domains) > 0 or len(sd.new_docs) > 0:
            self.changed = True
        sd.main()

    @pyqtSlot()
    def on_syncButton_clicked(self):
        # get selected domains
        domains = self.doc_model.checked()
        self.logger.info(domains)
        self.config.prepare_sync(domains)

        pd = dialogs.PrepareSyncDialog(parent=self)
        worker = sync_worker.PrepareWorker(self.config)
        worker.signals.finished.connect(pd.accept)
        worker.signals.finished.connec(self.sync_me())
        worker.signals.aborted.connect(pd.reject)
        pd.main(worker)
        self.threadpool.start(worker)

    @pyqtSlot()
    def on_synchronize_confirmed(self):
        self.config.sy.display_available_docs()
        sd = dialogs.PrepareSyncDialog(parent=self)
        worker = sync_worker.SyncWorker(self.config)

        worker.signals.finished.connect(sd.accept)
        worker.signals.aborted.connect(sd.reject)
        sd.main(worker)
        self.threadpool.start(worker)

        self.config.confirm_sync()
        self.refresh_counts()

    @pyqtSlot()
    def on_synchronize_rejected(self):
        self.config.revert_sync()

    def closeEvent(self, event):
        # save new data
        self.logger.info(f'Close - change ? {self.changed}')
        if self.changed or self.config.no_config_file:
            self.logger.info(self.config.sy.domain_filter)
            #helpers.save_json("/tmp/refdoc.conf", self.config.sy.refdoc)
            #helpers.save_json("/tmp/doc.conf", self.config.sy.doc)

            self.config.sy.save_infos()
            self.config.sy.save_configuration()
        else:
            self.logger.info("No changes")
        event.accept()


if __name__ == '__main__':
    logging.basicConfig(filename=str(sync.DEFAULT_CONF_DIR / 'ihe-sync.log'), level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    conf = config.Configuration()
    conf.load_configuration()
    iheui = Ui(conf)
    iheui.main()
    app.exec_()
