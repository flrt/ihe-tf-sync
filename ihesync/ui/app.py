import sys
import platform
import os
import logging
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QFrame, QStyleOptionViewItem

from ihesync import session
from ihesync.ui import ihesync_app
from ihesync.ui import documents_model
from ihesync.ui import dialogs
from ihesync.ui import sync_worker
from ihesync import DOMAIN_DICT
from ihesync.ui import STYLES
from ihesync.ui import ICONS

__version__ = 2.0


class Ui(QtWidgets.QMainWindow, ihesync_app.Ui_MainWindow):
    def __init__(self, context, parent=None):
        super(Ui, self).__init__(parent)
        self.logger = logging.getLogger()
        self.network_available = False
        self.network_watchdog = None

        self.setupUi(self)
        self.context = context
        self.changed = False
        self.label_ihewebsite.setText('Visit IHE Website : <a href="http://www.ihe.net">www.ihe.net</a>')
        self.label_ihewebsite.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_ihewebsite.setOpenExternalLinks(True)

        self.modifed_label = QLabel("Status: No change")
        #self.modifed_label.setStyleSheet('border: 0; color:  blue;')
        self.network_label = QLabel("No network!")

        self.statusBar().setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.network_label)
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.modifed_label)

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(4)

        self.doc_model = documents_model.DocumentsModel([])
        self.tableView.setModel(self.doc_model)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        icon_delegate = OpenFolderDelegate(self.tableView)
        self.tableView.setItemDelegateForColumn(4, icon_delegate)
        self.tableView.clicked.connect(self.open_documents_folder)
        self.logger.info("Starts with %d threads" % self.threadpool.maxThreadCount())

        if platform.system() in STYLES:
            self.setStyleSheet(STYLES[platform.system()])


    def main(self):
        conf_loaded = self.context.load_configuration()

        self.show()
        self.start_network_watchdog()

        if not conf_loaded:
            self.change_status("Configuration loading error : check network")

        self.refresh_configuration()
        self.refresh_information_counts()
        self.refresh_domain_list()
        self.refresh_public_comment()

        if self.context.local_file_count_ondisk != self.context.local_file_count:
            self.msgbox_out_of_sync()

    # -- Messages boxes ---
    # ---------------------
    def msgbox_out_of_sync(self):
        msg = QMessageBox.about(
            self,
            "Information...",
            (
                f"Out of sync ! Local files on disk {self.context.local_file_count_ondisk}"
                f" vs in configuration {self.context.local_file_count}\n"
                f" Sync needed"
            ),
        )
        msg.setIcon(QMessageBox.Warning)

    def msgbox_network_unavailable(self):
        QMessageBox.critical(self,
                             "Network unavailable", (
                                 f"No network"
                                 f" Check\n"), )

    # -- Messages boxes ---

    # -- Check Network
    def update_network_status(self, data):
        (ip, self.network_available) = data
        self.logger.debug(f"network status updated availaible = {self.network_available}")
        if self.network_available:
            self.network_label.setText("Connected")
            self.network_label.setStyleSheet('border: 0; color:  green;')
        else:
            self.network_label.setText("no Network!")
            self.network_label.setStyleSheet('border: 0; color:  red;')

    def start_network_watchdog(self):
        (ip, port) = self.context.sync.ping_address
        self.logger.debug(f"Start watchdog ip={ip} port={port} delay={self.context.sync.ping_delay}")
        self.network_watchdog = sync_worker.NetworkWorker(ip, port, self.context.sync.ping_delay)
        self.network_watchdog.signals.progress.connect(self.update_network_status)
        self.threadpool.start(self.network_watchdog)

    def stop_network_watchdog(self):
        self.logger.debug("Stop network watchdog...")
        self.network_watchdog.abort()

    # -- Refresh counts

    def refresh_public_comment(self):
        state = (
            QtCore.Qt.Checked
            if self.context.sync.public_comment
            else QtCore.Qt.Unchecked
        )
        self.checkComments.setCheckState(state)

    def refresh_last_checked(self):
        """
            Refresh date of the last check
        :return: -
        """
        if self.context.sync.last_check:
            self.labelLastCheckDate.setText(
                self.context.sync.last_check.strftime("%Y-%m-%d %H:%M")
            )

    def refresh_domain_list(self) -> None:
        """
            Refresh the domain table
                - sorted by domain name
                - get the count of local files
        :return:
        """
        self.logger.info("refresh_domain_list")
        self.doc_model.log()

        self.labelDomainCountValue.setText(str(len(self.context.domains)))

        self.doc_model.set_documents(None)

        data = []
        for domain in sorted(self.context.domains, key=lambda v: v["name"]):
            local_count = self.context.sync.count_local_files(domain["name"])
            self.logger.debug(f"> domain >> {domain} - local cout = {local_count}")

            data.append(
                {
                    "checked": domain["name"] in self.context.selected_domains or domain["checked"],
                    "domain": domain["name"],
                    "title": DOMAIN_DICT[domain["name"]]
                    if domain["name"] in DOMAIN_DICT
                    else "",
                    "down": local_count,
                    #domain["downloaded"],
                    "total": domain["files"],
                    "link": local_count > 0,
                    "local": local_count,
                    "error": 0
                }
            )

        self.doc_model.set_documents(data)
        self.tableView.model().layoutChanged.emit()

    def refresh_configuration(self) -> None:
        """
            Refresh the configuration tab
        :return: -
        """
        self.textConfDir.setText(str(self.context.conf_directory))
        self.textDocDir.setText(str(self.context.doc_directory))
        self.newDocsGroupBox.setVisible(False)

        self.textLoggingFilename.setText(str(self.context.sync.log_filename))
        rad = dict(INFO=self.infoRadioButton, ERROR=self.errorRadioButton, DEBUG=self.debugRadioButton)
        if self.context.sync.log_level in rad:
            rad[self.context.sync.log_level].setChecked(True)
        (ip, port) = self.context.sync.ping_address
        self.textPingIPaddress.setText(ip)
        self.textPingPort.setText(str(port))
        self.textPingDelay.setText(str(self.context.sync.ping_delay))

    def refresh_information_counts(self) -> None:
        """
            Refresh counters and date last checked
        :return:
        """
        self.logger.debug("refresh_information_counts")
        self.newDocsGroupBox.setVisible(False)
        self.refresh_last_checked()
        self.context.scan_local_dirs()
        self.context.refresh_counts_current()
        self.labelDocumentCountValue.setText(str(self.context.file_count))
        self.labelLocalFilesCountValue.setText(str("{}/{}"
                                                   .format(self.context.local_file_count_ondisk,
                                                           self.context.local_file_count)))
        diff = self.context.check_updates_available()
        if diff > 0:
            self.newDocLabel.setText(f"{diff} document changes")
            self.newDocsGroupBox.setVisible(True)

    def change_status(self, msg=None, changed=None, duration=3000):
        if changed:
            self.changed = changed

        self.modifed_label.setText("Status: Changed !" if self.changed else "Status: No change")

        if msg:
            self.statusbar.showMessage(msg, duration)

    # -- UI callback

    @pyqtSlot()
    def on_checkComments_clicked(self):
        self.context.sync.public_comment = self.checkComments.checkState() == QtCore.Qt.Checked
        self.change_status(changed=True)

    @pyqtSlot()
    def on_aboutPushButton_clicked(self):
        dlg = dialogs.AboutDialog(self)
        dlg.main()

    @pyqtSlot()
    def on_infoRadioButton_clicked(self):
        self.context.sync.update_logger_config(level="INFO")

    @pyqtSlot()
    def on_errorRadioButton_clicked(self):
        self.context.sync.update_logger_config(level="ERROR")

    @pyqtSlot()
    def on_debugRadioButton_clicked(self):
        self.context.sync.update_logger_config(level="DEBUG")

    @pyqtSlot()
    def on_changeLogPushButton_clicked(self):
        self.context.sync.update_logger_config(filename=self.textLoggingFilename.toPlainText())

    @pyqtSlot()
    def on_deleteLogPushButton_clicked(self):
        try:
            os.remove(self.textLoggingFilename.toPlainText())
        except OSError as e:
            self.logger.error(f"Can't remove {self.textLoggingFilename.toPlainText()} : {str(e)}")

    @pyqtSlot()
    def on_openLogPushButton_clicked(self):
        if os.path.exists(self.textLoggingFilename.toPlainText()):
            webbrowser.open_new(f"file://{self.textLoggingFilename.toPlainText()}")
        else:
            self.logger.error(f"Can't open file {self.textLoggingFilename.toPlainText()} which does not exist!")

    @pyqtSlot()
    def on_textConfDir_textChanged(self):
        self.context.conf_directory = self.textConfDir.toPlainText()

    @pyqtSlot()
    def on_textDocDir_textChanged(self):
        self.context.doc_directory = self.textDocDir.toPlainText()

    @pyqtSlot()
    def on_confSelectButton_clicked(self):
        previous = self.textConfDir.toPlainText()
        confdir = QFileDialog.getExistingDirectory(self, "Select Directory", previous, QFileDialog.ShowDirsOnly)
        if len(confdir):
            self.context.conf_directory = str(confdir)
            self.textConfDir.setText(self.context.conf_directory)
            self.change_status(changed=True)

    @pyqtSlot()
    def on_docSelectButton_clicked(self):
        previous = self.textDocDir.toPlainText()
        docdir = QFileDialog.getExistingDirectory(self, "Select Directory", previous, QFileDialog.ShowDirsOnly)
        if len(docdir):
            self.context.doc_directory = str(docdir)
            self.textDocDir.setText(self.context.doc_directory)
            self.change_status(changed=True)

    @pyqtSlot()
    def on_syncButton_clicked(self):
        if self.network_available:
            self.prepare_synchronization()
        else:
            self.msgbox_network_unavailable()

    @pyqtSlot()
    def on_changeConnectionPushButton_clicked(self):
        # get values before change
        (new_ip, new_port) = self.context.sync.ping_address
        new_delay = self.context.sync.ping_delay
        new_ip = self.textPingIPaddress.toPlainText()
        try:
            new_port = int(self.textPingPort.toPlainText())
        except ValueError as p_err:
            self.change_status("Port value must be numeric !!!", )
            self.logger.error(f"Configuration error while setting non numeric value for port {p_err}")
            self.textPingPort.setText(str(new_port))
        try:
            new_delay = int(self.textPingDelay.toPlainText())
        except ValueError as d_err:
            self.change_status("Delay value must be numeric !!!")
            self.logger.error(f"Configuration error while setting non numeric value for delay {d_err}")
            self.textPingDelay.setText(str(new_delay))

        if (new_ip, new_port) != self.context.sync.ping_address or new_delay != self.context.sync.ping_delay:
            self.context.sync.ping_address = (new_ip, new_port)
            self.context.sync.ping_delay = new_delay
            self.stop_network_watchdog()
            self.start_network_watchdog()
            self.change_status("Ping informations changed.")

    @pyqtSlot()
    def on_synchronize_confirmed(self):
        self.logger.debug("on_synchronize_confirmed")
        self.do_synchronization()

    @pyqtSlot()
    def on_synchronize_rejected(self):
        self.context.revert_sync()

    def closeEvent(self, event):
        # save new data
        self.logger.debug(f"Close - change ? {self.changed}")
        if self.changed or self.context.no_config_file:
            self.context.sync.save_infos()
            self.context.sync.save_configuration()
        else:
            self.logger.info("No changes")
        event.accept()
        self.stop_network_watchdog()

    # -- > Actions --
    # --------------

    def prepare_synchronization(self):
        """
            get the selected domains
            prepare elements to sync
            launch the UI dialog showing the compute of sync
        :return:
        """
        # get selected domains
        self.logger.debug("prepare_synchronization")
        domains = self.doc_model.checked()
        self.logger.info(domains)
        self.context.prepare_sync(domains)

        pd = dialogs.ProgressSyncDialog(
            dialogs.ProgressSyncDialog.REMOTE_INFO_TEXT, parent=self
        )
        worker = sync_worker.PrepareWorker(self.context)
        worker.signals.finished.connect(pd.accept)
        worker.signals.finished.connect(self.synchronize_dialog)
        worker.signals.aborted.connect(pd.reject)
        pd.main(worker)
        self.threadpool.start(worker)

    def synchronize_dialog(self):
        """
            Launch UI for synchro
        :return:
        """
        if self.network_available:
            sd = dialogs.SyncDialog(parent=self)
            sd.confirm_signal.connect(self.on_synchronize_confirmed)
            sd.reject_signal.connect(self.on_synchronize_rejected)

            sd.old_domains = self.context.infos["old_domain"]
            sd.new_domains = self.context.infos["new_domain"]
            sd.old_docs = self.context.infos["to_del"]
            sd.new_docs = self.context.infos["to_download"]
            if len(sd.old_domains) > 0 or len(sd.new_docs) > 0:
                self.change_status(changed=True)
            sd.main()
        else:
            self.msgbox_network_unavailable()

    def do_synchronization(self):
        self.doc_model.log()

        self.context.sync.display_available_docs()
        sd = dialogs.ProgressSyncDialog(
            dialogs.ProgressSyncDialog.SYNC_INFO_TEXT, parent=self
        )
        worker = sync_worker.SyncWorker(self.context)

        worker.signals.finished.connect(sd.accept)
        worker.signals.finished.connect(self.sync_finished)
        worker.signals.progress.connect(self.doc_model.update_documents)
        worker.signals.aborted.connect(sd.reject)
        sd.main(worker)
        self.threadpool.start(worker)

        self.context.confirm_sync()

    def sync_finished(self):
        """
            Syncho done.
            - display information in status bar
            - refresh informations counts
            - refresh doc table information
        """
        downloaded, error = self.doc_model.summary()
        self.change_status(f"{downloaded} download(s), {error} error(s)")

        self.refresh_information_counts()
        self.tableView.model().layoutChanged.emit()

    # -- < Actions

    def open_documents_folder(self, index: QtCore.QModelIndex) -> None:
        docinfo = index.model().docs[index.row()]
        if docinfo['link'] and index.column() == 4:
            dom = self.context.local_path_domain(docinfo['domain'])
            webbrowser.open_new(f"file://{dom}")


class OpenFolderDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(OpenFolderDelegate, self).__init__(parent)
        self.icon = QtGui.QIcon(ICONS['files'])

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        if index.model().docs[index.row()]['link']:
            self.icon.paint(painter, option.rect, QtCore.Qt.AlignLeft)
        else:
            super().paint(painter, option, index)


class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctx = session.Context()
    iheui = Ui(ctx)
    iheui.main()
    app.exec_()
