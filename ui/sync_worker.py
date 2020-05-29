from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from config import Configuration

import logging

class BasicSignals(QObject):
    finished = pyqtSignal()
    aborted = pyqtSignal()
    progress = pyqtSignal(tuple)


class BasicWorker(QRunnable):
    def __init__(self, model):
        super().__init__()
        #super(QRunnable, self).__init__()
        self.signals = BasicSignals()
        self.model = model
        self.aborted = False

    def abort(self):
        self.aborted = True
        self.signals.aborted.emit()


class PrepareWorker(BasicWorker):
    def __init__(self, model):
        super().__init__(model)

    def doc_count(self):
        return len(self.model.sy.get_document_tocheck_list())

    @pyqtSlot()
    def run(self):
        doclist = self.model.sy.get_document_tocheck_list()

        idx = 0
        while (idx < len(doclist)) and self.aborted is False:
            self.model.sy.get_document_characteristics(doclist[idx])
            self.signals.progress.emit((idx + 1, doclist[idx]))
            idx += 1
        if self.aborted is False:
            self.signals.finished.emit()


class SyncWorker(BasicWorker):
    def __init__(self, model):
        #super(BasicWorker, self).__init__(model)
        super().__init__(model)
        self.logger = logging.getLogger()

    def doc_count(self):
        return len(self.model.infos['to_del']) + len(self.model.infos['to_download'])

    @pyqtSlot()
    def run(self):
        self.logger.info("\nWorker : Clean documents not in sync...")
        idx = 0
        while (idx < len(self.model.infos['to_del'])) and self.aborted is False:
            self.logger.info(f"W Obsolete document {self.model.infos['to_del'][idx]['filename']} found: delete it...")
            self.model.sync.delete(self.model.infos['to_del'][idx])
            self.signals.progress.emit((idx + 1, 'DEL', self.model.infos['to_del'][idx]))
            idx += 1

        while (idx < len(self.model.infos['to_download'])) and self.aborted is False:
            self.logger.info(f"W Newer document {self.model.infos['to_download'][idx]['filename']}  found: download it...")
            self.model.sync.download(self.model.infos['to_download'][idx]['filename'])
            self.signals.progress.emit((idx + 1, 'DOWN', self.model.infos['to_download'][idx]))
            idx += 1

        if self.aborted is False:
            self.signals.finished.emit()
