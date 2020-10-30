import os.path
import logging

from ihesync import sync


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
            Check remote, gather informations about available docs.

            Get some count informations
        """
        retcode = True

        conf = {}
        if not (os.path.exists(self.conf_directory)):
            os.mkdir(self.conf_directory)

        self.sync = sync.Synchro(self.doc_directory, self.conf_directory, conf)
        self.sync.load_configuration()

        #self.initial_domains = self.sync.domain_filter[:]
        #self.selected_domains = self.sync.domain_filter[:]
        self.logger.info(f"Initial domains : {self.initial_domains}")
        retcode &= self.sync.doc_cartography()

        self.scan_local_dirs()
        self.initial_domains = self.sync.domain_filter[:]
        self.selected_domains = self.sync.domain_filter[:]
        # if no previous context exists, copy the current one
        if len(self.sync.refdoc.keys()) < 2:
            self.sync.duplicate_docs(source_ref=False)
        else:
            self.no_config_file = False
        if len(self.sync.doc.keys()) < 2:
            self.sync.duplicate_docs(source_ref=True)


        #self.initial_domains = self.sync.domain_filter[:]
        #self.selected_domains = self.sync.domain_filter[:]
        self.refresh_counts_ref()

        # build domain list. From reference map (saved) + remote map
        self.domains = self.domains_info(self.sync.refdoc)

        ref_domains = [x['name'] for x in self.domains]

        # search new domain in remote map
        for dom in self.domains_info(self.sync.doc):
            if dom['name'] not in ref_domains:
                self.domains.append(dom)

        return retcode

    def scan_local_dirs(self):
        # scan local directory to get unreferenced documents
        self.local_file_count_ondisk = self.sync.scan_local_dirs()

    def refresh_counts_ref(self):
        """
            Refresh counts with loaded configuration
        :return:
        """
        self.refresh_counts(self.sync.refdoc)

    def refresh_counts_current(self):
        """
            Refresh counts with current doc dict
        :return:
        """
        self.refresh_counts(self.sync.doc)

    def refresh_counts(self, src_doc):
        """
            Set the count of
            - remote files
            - local files (downloaded files)
        :param src_doc: dict of docs
        :return: -
        """
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
            keys :
                - name,
                - checked
                - downloaded
                - files

        """
        dom = []
        for k in sorted(conf.keys()):
            downloaded = len(list(filter(lambda x: "size" in x, conf[k].values())))
            ref_files = len(list(filter(lambda x: "href" in x and "title" in x, conf[k].values())))

            dom.append(dict(name=k, checked=downloaded > 0,
                            files=ref_files, downloaded=downloaded))
        return dom

    def prepare_sync(self, domains=[]):
        self.selected_domains = domains[:]
        self.infos = dict(old_domain=self.initial_domains[:], new_domain=domains[:])
        self.sync.domain_filter = domains
        self.infos['to_del'], self.infos['to_download'] = self.sync.prepare_sync(remote_check=False)

    def revert_sync(self):
        self.sync.domain_filter = self.initial_domains[:]

    def confirm_sync(self):
        self.initial_domains = self.selected_domains[:]

    def local_path_domain(self, domain):
        return os.path.join(self.sync.outputdir, domain)

    def check_updates_available(self):
        """
            check if some documents are newly available
        :return: change count
        """
        self.logger.debug("check_updates_available")
        change_count = 0
        for domain in self.initial_domains:
            self.logger.info(f"domain={domain} = {len(self.sync.doc[domain])} / {len(self.sync.refdoc[domain])}")
            diff = abs(len(self.sync.doc[domain]) - len(self.sync.refdoc[domain]))
            if diff > 0:
                change_count += diff
        return change_count

    def log(self):
        self.logger.info(f'sync - original domains {self.initial_domains} | '
                         f'sync - selected domains {self.selected_domains}'
                         )
        self.logger.info("Context domains >>")
        for i, v in enumerate(self.domains):
            self.logger.info(f"{i} {v}")
