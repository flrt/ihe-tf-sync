from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import logging
import socket
import time
import datetime
import ihesync.helpers as helpers
import requests

WORKER_ACTION_DOWN = 'Download'
WORKER_ACTION_DEL = 'Delete'
WORKER_ACTION_ERR = 'Error'


class BasicSignals(QObject):
    finished = pyqtSignal()
    aborted = pyqtSignal()
    progress = pyqtSignal(tuple)


class BasicWorker(QRunnable):
    def __init__(self, context):
        super().__init__()
        self.signals = BasicSignals()
        self.context = context
        self.aborted = False
        self.logger = logging.getLogger()

    def abort(self):
        self.aborted = True
        self.signals.aborted.emit()


class PrepareWorker(BasicWorker):
    def __init__(self, context):
        super().__init__(context)

    def doc_count(self):
        return len(self.context.sync.get_document_tocheck_list())

    @pyqtSlot()
    def run(self):
        doclist = self.context.sync.get_document_tocheck_list()

        idx = 0
        while (idx < len(doclist)) and self.aborted is False:
            self.context.sync.get_document_characteristics(doclist[idx])
            self.signals.progress.emit((idx + 1, "", doclist[idx], 0))
            idx += 1

        if self.aborted is False:
            self.signals.finished.emit()


class SyncWorker(BasicWorker):
    def __init__(self, context):
        super().__init__(context)

    def doc_count(self):
        return len(self.context.infos["to_del"]) + len(self.context.infos["to_download"])

    @pyqtSlot()
    def run(self):
        idx = 0
        while (idx < len(self.context.infos["to_del"])) and self.aborted is False:
            self.logger.info(
                f"W Obsolete document {self.context.infos['to_del'][idx]['filename']} found: delete it..."
            )
            success, error, filename = self.context.sync.delete(self.context.infos["to_del"][idx])
            if not success:
                self.logger.error(f"Worker error : {error}")
            self.signals.progress.emit(
                (idx + 1, WORKER_ACTION_DEL if success else WORKER_ACTION_ERR,
                 self.context.infos["to_del"][idx],
                 self.context.sync.count_local_files(self.context.infos["to_del"][idx]['domain']))
            )
            idx += 1

        idx = 0
        while (idx < len(self.context.infos["to_download"])) and self.aborted is False:
            self.logger.info(
                f"W Newer document {self.context.infos['to_download'][idx]}  found: download it..."
            )
            success, error, filename = self.context.sync.download(self.context.infos["to_download"][idx])
            if not success:
                self.logger.error(f"Worker error : {error}")
            self.signals.progress.emit((idx + 1, WORKER_ACTION_DOWN if success else WORKER_ACTION_ERR,
                                        self.context.infos["to_download"][idx],
                                        self.context.sync.count_local_files(
                                            self.context.infos["to_download"][idx]['domain'])))
            idx += 1

        if self.aborted is False:
            self.signals.finished.emit()


class NetworkWorker(BasicWorker):
    def __init__(self, url, proxy, delay):
        super().__init__(None)
        self.url = url
        self.proxies = helpers.get_proxies(proxy)
        self.delay = delay

    def set_proxy(self, proxy):
        self.logger.debug(f"Update proxy in network watchdog {proxy}")
        self.proxies = helpers.get_proxies(proxy)

    def run(self):
        self.logger.info(f"Start Network watchdog url={self.url} / proxy={self.proxies}")
        while not self.aborted:
            self.signals.progress.emit((self.url, self.is_connected()))
            for tick in range(self.delay):
                time.sleep(1)
                if self.aborted:
                    break

    def is_connected(self):
        try:
            # connect to the host -- tells us if the host is actually reachable
            r = requests.head(self.url, proxies=self.proxies)
            return r.status_code == 200
        except OSError:
            return False
