import os.path
import logging

import sync

class Context:
    """
    Context for the synchronization process

    2 scopes :
    - initial : read from the local configuration file (preceding options)
    - current : new domains to synchronise

    """
    def __init__(self):
        self.logger = logging.getLogger()
        self.doc_directory = sync.DEFAULT_DOC_DIR
        self.conf_directory = sync.DEFAULT_CONF_DIR
        self.conf_file = sync.DOC_INFO_FILENAME
        self.sync = None
        self.domains = []
        self.initial_domains = []
        self.selected_domains = []
        self.file_count = 0
        self.local_file_count = 0
        self.local_file_count_ondisk = 0
        self.no_config_file = True
        self.infos = {}

    def load_configuration(self):
        """
            Load configuration form local config file.
            If the directory does not exists : create it
            Get some count informations
        """

        conf = {}
        if not (os.path.exists(self.conf_directory)):
            os.mkdir(self.conf_directory)

        self.sync = sync.Synchro(self.doc_directory, self.conf_directory, conf)
        self.sync.load_configuration()
        self.initial_domains = self.sync.domain_filter[:]
        self.logger.info(f"Initial domains : {self.initial_domains}")
        self.sync.doc_cartography()

        # if no previous context exists, copy the current one
        if len(self.sync.refdoc.keys()) < 2:
            self.sync.duplicate_docs(source_ref=False)
        else:
            self.no_config_file = False
        if len(self.sync.doc.keys()) < 2:
            self.sync.duplicate_docs(source_ref=True)

        # scan local directory to get unreferenced documents
        self.local_file_count_ondisk = self.sync.scan_local_dir()

        self.refresh_counts_ref()

        # build domain list. From reference map (saved) + remote map
        self.domains = self.domains_info(self.sync.refdoc)

        ref_domains = [x['name'] for x in self.domains]

        # search new domain in remote map
        for dom in self.domains_info(self.sync.doc):
            if dom['name'] not in ref_domains:
                self.domains.append(dom)

    def refresh_counts_ref(self):
        self.refresh_counts(self.sync.refdoc)

    def refresh_counts_current(self):
        self.refresh_counts(self.sync.doc)

    def refresh_counts(self, src_doc):
        counts = [len(list(v.values())) for k, v in src_doc.items()]
        self.file_count = sum(counts)

        counts = [len(list(filter(lambda x: "size" in x, v.values()))) for k, v in src_doc.items()]
        self.local_file_count = sum(counts)

    def check_remote(self):
        self.sync.doc_cartography()

        counts = [len(v) for k, v in self.sync.doc.items()]
        self.file_count = sum(counts)

    def domains_info(self, conf):
        """
            Build an information dict by analyzing the whole configuration (documents)
            Get the domain names, the files available count, and the downloaded files count
        """
        dom = []
        for k in sorted(conf.keys()):
            downloaded = len(list(filter(lambda x: "size" in x, conf[k].values())))
            dom.append(dict(name=k, selected=downloaded > 0,
                            files=len(conf[k]), downloaded=downloaded))
        return dom

    def prepare_sync(self, domains=[]):
        self.selected_domains = domains
        self.infos = dict(old_domain=self.initial_domains[:], new_domain=domains[:])
        self.sync.domain_filter = domains
        self.infos['to_del'], self.infos['to_download'] = self.sync.prepare_sync(remote_check=False)

    def revert_sync(self):
        self.sync.domain_filter = self.initial_domains

    def confirm_sync(self):
        self.initial_domains = self.selected_domains[:]

    def log(self):
        self.logger.info(f'sync - original domains {self.initial_domains} | '
              f'sync - selected domains {self.selected_domains}'
              )
        self.logger.info(f'sync -> {self.infos}')
        #        helpers.save_json("/tmp/refdoc_sync2.conf", self.sy.refdoc)
        #        helpers.save_json("/tmp/doc_sync2.conf", self.sy.doc)
        [self.logger.info(f"-- {d['filename']}") for d in self.infos['to_del']]
        [self.logger.info(f"++ {d['filename']}") for d in self.infos['to_download']]

    def local_path_domain(self, domain):
        return os.path.join(self.sync.outputdir, domain)