from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog 

import sys
import os.path
import json
import pathlib
from datetime import datetime
import helpers
import ui.ihesync_app
import ui.sync_dialog

import sync

class Configuration():
    def __init__(self):
        self.doc_directory = sync.DEFAULT_DOC_DIR
        self.conf_directory = sync.DEFAULT_CONF_DIR
        self.conf_file = sync.DOC_INFO_FILENAME
        self.sy = None
        self.domains = []
        self.selected_domains = []
        self.file_count = 0
        self.local_file_count = 0
    
    def load_configuration(self):
        """
            Load configuration form local config file.
            If the directory does not exists : create it
            Get some count informations
        """

        conf = {}
        if not(os.path.exists(self.conf_directory)):
            os.mkdir(self.conf_directory)
        
        self.sy = sync.Synchro(self.doc_directory, self.conf_directory, conf)
        self.sy.load_configuration()
        self.sy.doc_cartography()

        if len(self.sy.refdoc.keys())<2:
            self.sy.duplicate_docs(source_ref=False)
        if len(self.sy.doc.keys())<2:
            self.sy.duplicate_docs(source_ref=True)


        counts=[len(list(v.values())) for k,v in self.sy.refdoc.items()]
        self.file_count = sum(counts)

        counts=[len(list(filter(lambda x: "etag" in x, v.values()))) for k,v in self.sy.refdoc.items()]
        self.local_file_count = sum(counts)

        # build domain list. From reference map (saved) + remote map
        self.domains = self.domains_info(self.sy.refdoc)

        ref_domains=[x['name'] for x in self.domains]
        print(ref_domains)
        # search new domain in remote map
        for dom in self.domains_info(self.sy.doc):
            if dom['name'] not in ref_domains:
                self.domains.append(dom)

    def check_remote(self):
        self.sy.doc_cartography()
        
        counts=[len(v) for k,v in self.sy.doc.items()]
        self.file_count = sum(counts)

    def domains_info(self, conf):
        """
            Build an information dict by analyzing the whole configuration (documents)
            Get the domain names, the files available count, and the downloaded files count
        """
        dom = []
        for k in sorted(conf.keys()):
            downloaded = len(list(filter(lambda x: "etag" in x, conf[k].values())))
            dom.append(dict(name=k, selected = downloaded>0,
                    files = len(conf[k]), downloaded=downloaded))
        return dom
    
    def sync(self, domains=[]):
        print(f"Actuel {self.sy.domain_filter}")
        print(f"nouveaux {domains}")

        infos = dict(old_domain=self.sy.domain_filter[:], new_domain=domains[:])
        self.sy.domain_filter = domains
        infos['to_del'], infos['to_download'] = self.sy.prepare_sync()

        #for d in to_del:
        #    print(f"-- {d['filename']}")
        #for d in to_download:
        #    print(f"++ {d['filename']}")
        return infos
        

class SyncDialog(QtWidgets.QDialog, ui.sync_dialog.Ui_SyncDialog):
    confirm_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(SyncDialog, self).__init__(parent)
        self.setupUi(self)
        self.old_domains = []
        self.new_domains = []
        self.old_docs = []
        self.new_docs = [] 
    
    def accept(self):
        print("GO")
        self.confirm_signal.emit()
        super().accept()

    def main(self):
        txt = "<p>No domain to synchronize</p>"
        
        if len(self.new_domains)>0:
            newd = ', '.join(self.new_domains) if self.new_domains else '<i>none</i>'
            oldd = ', '.join(self.old_domains) if self.old_domains else '<i>none</i>'
            if len(set(self.old_domains)-set(self.new_domains)) > 0 \
                or len(set(self.new_domains)-set(self.old_domains)) > 0:
                txt = f"<p>Previous domains: <code>{oldd}</code><br/>New domains <code>{newd}</code></p>"
            else:
                txt = f"<p>Keep domains {newd} synchronized</p>"

        addd=list(set(self.new_domains)-set(self.old_domains))
        if len(addd) > 0:
            txt += '<p>Add {} to the synchronize process'.format(', '.join(addd))
        deld=list(set(self.old_domains)-set(self.new_domains))
        if len(deld) > 0:
            txt += '<p>Delete {} to the synchronize process'.format(', '.join(deld))

        self.textDomainBrowser.setText(txt)

        txt = "Nothing to do :)" if len(self.new_docs)+len(self.old_domains)==0 else ""

        if len(self.new_docs)>0:
            txt += f"<h1>Download documents ({len(self.new_docs)}):</h1>"
            txt += "<ul><li>{}</li></ul>".format( "</li><li>".join(list(map(lambda x: x['filename'], self.new_docs))))

        if len(self.old_docs)>0:
            txt += f"<h1>Delete documents {len(self.old_docs)}:</h1>"
            txt += "<ul><li>{}</li></ul>".format( "</li><li>".join(list(map(lambda x: x['filename'], self.old_docs))))

        self.textDocumentsBrowser.setText(txt)

        self.show()

class Ui(QtWidgets.QMainWindow, ui.ihesync_app.Ui_MainWindow):
    def __init__(self, config, parent=None):
        super(Ui, self).__init__(parent)
        self.setupUi(self)
        self.config=config
        self.changed = False
        self.model = QtGui.QStandardItemModel(self.domainsView)
        self.label_ihewebsite.setText('Visit IHE Website : <a href="https://wwW.ihe.net">tech</a>')
        self.label_ihewebsite.setOpenExternalLinks(True)

    def main(self):
        self.refresh_configuration()
        self.refresh_counts()
        self.show()
    
    def refresh_public_comment(self):
        state = QtCore.Qt.Checked if self.config.sy.public_comment else QtCore.Qt.Unchecked
        self.checkComments.setCheckState(state)
    
    def refresh_last_checked(self):
        if self.config.sy.last_check:
            self.labelLastCheckDate.setText(self.config.sy.last_check.strftime("%Y-%m-%d %H:%M"))

    def refresh_domain_list(self):
        self.labelDomainCountValue.setText(str(len(self.config.domains)))

        if self.model.rowCount()>0:
            self.model.clear()
        
        domains = sorted(self.config.domains, key=lambda v:v['name'])
        longuest_domain = max(map(lambda x: x['name'], domains), key=len)
        font = QtGui.QFont('Mono', 10, QtGui.QFont.Light)
        color = QtGui.QBrush(QtGui.QColor("darkblue"))

        for domain in domains:
            t,d,f = domain['name'],domain['downloaded'],domain['files']
            item_text=f"{t:{len(longuest_domain)}}  {d:>3} / {f}"

            item = QtGui.QStandardItem(item_text)
            item.setCheckable(True)
            if domain["selected"]:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            item.setFont(font)
            item.setForeground(color)
            self.model.appendRow(item)
            
        self.domainsView.setModel(self.model)

    def checked_domain_list(self):
        domains=[]
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                print(f"index selected {index}")
                domains.append(self.config.domains[index]["name"])
                #domains.append(item.text())
        return domains

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
        self.config.conf_directory=self.textConfDir.toPlainText()

    @pyqtSlot()
    def on_textDocDir_textChanged(self):
        self.config.doc_directory=self.textDocDir.toPlainText()

    @pyqtSlot()
    def on_confSelectButton_clicked(self):
        print("on_confSelectButton_clicked")
        self.config.conf_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.textConfDir.setText(self.config.conf_directory)
        self.changed = True

    @pyqtSlot()
    def on_docSelectButton_clicked(self):
        print("on_docSelectButton_clicked")
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

    @pyqtSlot()
    def on_syncButton_clicked(self):
        domains=self.checked_domain_list()
        infos = self.config.sync(domains)
        sd = SyncDialog(parent=self)
        sd.confirm_signal.connect(self.on_synchronize_confirmed)
        sd.old_domains = infos['old_domain']
        sd.new_domains = infos['new_domain']
        sd.old_docs = infos['to_del']
        sd.new_docs = infos['to_download']
        if len(sd.old_domains)>0 or len(sd.new_docs)>0:
            self.changed = True
        sd.main()
    
    @pyqtSlot()
    def on_synchronize_confirmed(self):
        self.config.sy.display_available_docs()
        self.config.sy.sync_all()
        self.refresh_counts()
 
    def closeEvent(self, event):
        # save new data
        print(f'Close - change ? {self.changed}')
        if self.changed:
            print(self.config.sy.domain_filter)
            helpers.save_json("/tmp/refdoc.conf", self.config.sy.refdoc)
            helpers.save_json("/tmp/doc.conf", self.config.sy.doc)

            self.config.sy.save_infos()
            self.config.sy.save_configuration()
        else:
            print("No changes")
        event.accept()
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    conf = Configuration()
    conf.load_configuration()
    iheui = Ui(conf)
    iheui.main()
    app.exec_()

