#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Synchronize locally all (or part of) documents available 
    on IHE.net

"""

__author__ = "Frederic Laurent"
__version__ = "1.1"
__copyright__ = "Copyright 2018, Frederic Laurent"
__license__ = "MIT"

import os
import os.path
import sys
from pathlib import Path
import argparse
import datetime
import locale
import copy
import requests
from bs4 import BeautifulSoup
from ihesync import helpers
import logging

IHE_URL = "https://www.ihe.net"
IHE_TF_URL = f"{IHE_URL}/resources/technical_frameworks/"
IHE_COMMENT_URL = f"{IHE_URL}/resources/public_comment/"
DATA_ROOTDIR = "data"
DOC_INFO_FILENAME = "docs.json"
GENERAL_INFO_FILENAME = "infos.txt"
DEFAULT_CONF_DIR = Path.home() / '.ihe-sync'
DEFAULT_DOC_DIR = Path.home() / 'Documents' / 'ihe-documents'
DEFAULT_LOG_FILENAME = "ihe-sync.log"
DEFAULT_LOG_LEVEL = "ERROR"
DEFAULT_PING_DELAY = 30
META_TAG = "__meta__"


class Synchro:
    def __init__(self, outputdir, configdir, refdoc={}, console=False):
        """
        Constructor

        :param str outputdir: directory (root) containing downloaded files
        :param dict refdoc: dictionnary containing reference
            configuration (previous)
        """
        if sys.platform == "win32":
            locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        elif sys.platform == "darwin":
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        self.logger = logging.getLogger()
        self.log_filename = str(DEFAULT_CONF_DIR / DEFAULT_LOG_FILENAME)
        self.log_level = DEFAULT_LOG_LEVEL
        self.refdoc = refdoc
        self.doc = {}
        self.outputdir = outputdir
        self.configdir = configdir
        self.console = console
        self.last_check = None
        self.domain_filter = []
        self.public_comment = False
        self.ping_delay = DEFAULT_PING_DELAY
        self.geometry = (0, 0)
        self.proxy = dict(address='', port='', active=False)

    def config_logging(self):
        logging.basicConfig(filename=str(DEFAULT_CONF_DIR / self.log_filename),
                            level=self.log_level)

    def update_logger_config(self, level=None, filename=None):
        if level is not None:
            self.log_level = level
        if filename is not None:
            if logging.getLogger().hasHandlers():
                for h in logging.getLogger().handlers:
                    if isinstance(h, logging.FileHandler) and h.baseFilename.endswith(self.log_filename):
                        logging.getLogger().removeHandler(h)
            self.log_filename = filename
        if level or filename:
            self.config_logging()

    def load_configuration(self):
        """
            Load previous configuration if present
        :return: -
        """

        filename = os.path.join(self.configdir, DOC_INFO_FILENAME)
        self.refdoc = helpers.load_json(filename)
        self.get_meta()
        self.logger.debug(f"AFTER get_meta {self.domain_filter}")
        self.config_logging()

    def save_configuration(self):
        filename = os.path.join(self.configdir, DOC_INFO_FILENAME)
        self.logger.info(filename)
        self.save(filename)

    def duplicate_docs(self, source_ref=True):
        if source_ref:
            self.doc = copy.deepcopy(self.refdoc)
        else:
            self.refdoc = copy.deepcopy(self.doc)

    def get_all_domains(self):
        """
            Get IHE domains
        :return: list of domains
        """
        if self.doc:
            return list(self.doc.keys())
        elif self.refdoc:
            return list(self.refdoc.keys())
        else:
            return ['TF', 'PAT', 'CARD', 'DENT', 'ENDO', 'EYECARE',
                    'ITI', 'SUPPL', 'LAB', 'PALM', 'PCC', 'PHDSC', 'PCD',
                    'PHARMACY', 'QRPH', 'QUALITY', 'RO', 'RAD']

    def get_meta(self):
        """
            Extract metadata from configuration
        :return: -
        """
        if self.refdoc:
            if META_TAG in self.refdoc:
                self.last_check = datetime.datetime.strptime(self.refdoc[META_TAG]["last_check"],
                                                             "%Y-%m-%dT%H:%M:%S.%f")
                self.domain_filter = self.refdoc[META_TAG]["domains"]
                self.public_comment = self.refdoc[META_TAG]["public_comment"]
                if "outputdir" in self.refdoc[META_TAG]:
                    self.outputdir = self.refdoc[META_TAG]["outputdir"]
                else:
                    self.outputdir = str(DEFAULT_DOC_DIR)
                if "logfile" in self.refdoc[META_TAG]:
                    self.log_filename = self.refdoc[META_TAG]["logfile"]
                if "loglevel" in self.refdoc[META_TAG]:
                    self.log_level = self.refdoc[META_TAG]["loglevel"]
                if "ping" in self.refdoc[META_TAG]:
                    if "delay" in self.refdoc[META_TAG]["ping"]:
                        self.ping_delay = self.refdoc[META_TAG]["ping"]["delay"]
                    else:
                        self.ping_delay = DEFAULT_PING_DELAY
                if "proxy" in self.refdoc[META_TAG]:
                    self.proxy = self.refdoc[META_TAG]["proxy"]

                if "geometry" in self.refdoc[META_TAG]:
                    self.geometry = self.refdoc[META_TAG]["geometry"]

                del self.refdoc[META_TAG]
                self.logger.debug(self.refdoc.keys())

            else:
                # config not explicit, guess it
                ddocs = [list(filter(lambda x: "etag" in x, v.values())) for k, v in self.refdoc.items()]
                domains = set()

                # iterate through downloaded docs (ddocs = list by domain)
                for doclist in ddocs:
                    for doc in doclist:
                        domains.add(doc['domain'])

                        parsed = None
                        try:
                            parsed = datetime.datetime.strptime(str(doc['last-modified']), '%a, %d %b %Y %H:%M:%S %Z')
                            if (self.last_check and parsed < self.last_check) or self.last_check is None:
                                self.last_check = parsed
                        except:
                            pass

                self.domain_filter = list(domains)

    def get_infos(self, title, href, doc_class):
        """
        get infos on document via URL
        retrieve domain name (e.g. RAD, ITI, etc.)
        make an HEAD request to get meta data on document (size, etag, etc.)

        :param str title: Title of the document
        :param str href: URL of the document
        :return dict: dict with informations about the resource
        """

        docname = os.path.basename(href)
        # suppress IHE_ or IHE- at the beginning, split the name
        parts = docname[4:].split("_")

        _href = href
        if not href.startswith("http") and href.startswith("/"):
            _href = f"{IHE_URL}{href}"

        # keep RAD, ITI even if it's labelled RAD-TF
        # e.g. keep first part of the domain name

        return {
            "domain": parts[0].upper().split("-")[0],
            "typedoc": parts[1],
            "filename": docname,
            "href": _href,
            "title": title,
            "class": doc_class
        }

    def get_document_tocheck_list(self):
        result_docs = []
        for domain, docs in self.doc.items():
            for doc in docs.values():
                if "title" in doc and doc["domain"] in self.domain_filter:
                    result_docs.append(doc)
        return result_docs

    def get_document_characteristics(self, doc):
        """
        get infos on document by making an HEAD request to get meta data on document (size, etag, etc.)

        :param dict doc: Title of the document
        :param str href: URL of the document
        :return dict: dict with informations about the resource
        """

        if doc["domain"] in self.domain_filter:
            if self.console:
                print(".", end="", flush=True)

            # get more info with a HEAD request
            self.logger.debug(f"get_document_characteristics {str(doc)}")
            try:
                headreq = requests.head(doc['href'], proxies=helpers.get_proxies(self.proxy))

                if headreq.status_code == 301:
                    # get the new location
                    # Assume only one redirection happens...
                    doc['href'] = headreq.headers['Location']
                    headreq = requests.head(doc['href'], proxies=helpers.get_proxies(self.proxy))

                if headreq.status_code == 200:
                    doc["last-modified"] = headreq.headers["Last-Modified"]
                    doc["size"] = int(headreq.headers["Content-Length"])
                    doc["etag"] = headreq.headers["Etag"]
                else:
                    self.logger.error(f"Error {headreq.status_code} - URL={doc['href']}\n")
            except Exception as ex:
                self.logger.error(f"Error HEAD request {doc['href']} exception {str(ex)}")

        return doc

    def doc_cartography(self):
        """
        Load IHE html pages 
            Technical Framework
            Public comments if set
        """
        retcode = self.load_ihe_page(IHE_TF_URL)
        if self.public_comment:
            retcode &= self.load_ihe_page(IHE_COMMENT_URL)
        self.last_check = datetime.datetime.now()

        return retcode

    def load_ihe_page(self, webpage=IHE_TF_URL):
        """
        Load IHE html page
        Find documents
        Classify them
        """

        unsorted_docs = {}
        retcode = True
        try:
            req = requests.get(webpage, proxies=helpers.get_proxies(self.proxy))
            doc_class = webpage.split('/')[-2]

            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html5lib")
                links = list(filter(lambda x: x.get("href"), soup.find_all("a")))
                pdf_list = list(filter(lambda x: x.get("href").endswith(".pdf"), links))

                self.logger.info("Get information about documents")
                for link in pdf_list:
                    docinfo = self.get_infos(link.text, link.get("href"), doc_class)
                    unsorted_docs[docinfo["filename"]] = docinfo

            self.logger.info(f"\n{len(unsorted_docs)} documents found in IHE website : {doc_class}")
            self.classify(unsorted_docs)
            self.logger.debug(f"IHE category keys {self.doc.keys()}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Error while loading remote IHE page {conn_err.errno}:{conn_err.strerror}")
            retcode = False
        return retcode

    def display_available_docs(self):
        """
        Display how many documents are available in each domain.
        """
        disp = ["Available documents :"]
        [disp.append(f"{key}: {len(value)} documents") for key, value in self.doc.items()]

        if self.console:
            [print(s) for s in disp]
        [self.logger.info(s) for s in disp]

    def classify(self, unsorted_docs):
        """
        Classify docs into domains (ITI, CARD, etc.)
        Get the list of doc and keep the configuration
        in the self.doc dictionnary

        :param dict unsorted_docs: dict of record about documents
        """

        # iterate on docs and put them into domains
        for key, value in unsorted_docs.items():
            if value["domain"] not in self.doc:
                self.doc[value["domain"]] = {}
            self.doc[value["domain"]][value["filename"]] = value

        # move documents when keys are similar (PHARM/PHARMACY, EYE/EYECARE)
        keys = list(self.doc.keys())[:]
        for k in keys:
            for k2 in keys:
                if k != k2 and k.startswith(k2):
                    self.logger.debug(f"Moving documents from {k2} to {k}")
                    for keydoc, docinfo in self.doc[k2].items():
                        self.doc[k][keydoc] = docinfo
                        docinfo["domain"] = k
                    self.doc[k2] = {}
        # delete empty domains
        for k in keys:
            if not len(self.doc[k]):
                self.logger.debug(f"Delete {k} category from doc repo")
                del self.doc[k]

    def save(self, filename):
        sdoc = copy.deepcopy(self.doc)
        sdoc[META_TAG] = dict(last_check=self.last_check, public_comment=self.public_comment,
                              domains=self.domain_filter, outputdir=self.outputdir,
                              logfile=self.log_filename, loglevel=self.log_level,
                              ping=dict(delay=self.ping_delay),
                              geometry=self.geometry, proxy=dict(address=self.proxy['address'],
                                                                 port=self.proxy['port'],
                                                                 active=self.proxy['active']))

        helpers.save_json(filename, sdoc)

    def save_infos(self):
        """
        Save global informations about IHE documents

        :param list domains: list of domain to take into account

        """
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)

        infofn = os.path.join(self.outputdir, GENERAL_INFO_FILENAME)
        with open(infofn, "w") as fout:
            fout.write(f"Last checked : {datetime.datetime.now().isoformat()}\n")
            if self.domain_filter:
                fout.write(f"Checked {','.join(self.domain_filter)} domains.\n\n")
            for d, v in self.doc.items():
                # produce TOC for the current domain
                fout.write(f"domain {d} : {len(v)} documents\n")

    def is_different(self, domain, keydoc):
        """
        Test if the current document is different from the local
        (already downloaded) document
        It compares the etag metadata and the size of the document

        :param str domain: domain of the document (ITI, RAD, etc.)
        :param str keydoc: name of the document

        :return : True if documents are different
        """
        self.logger.debug(f"is_different : {keydoc}")
        try:
            if not ("etag" in self.refdoc[domain][keydoc] and "etag" in self.doc[domain][keydoc]):
                return False
            if not ("size" in self.refdoc[domain][keydoc] and "size" in self.doc[domain][keydoc]):
                return False
            return (
                    self.doc[domain][keydoc]["etag"] != self.refdoc[domain][keydoc]["etag"]
                    and self.doc[domain][keydoc]["size"] != self.refdoc[domain][keydoc]["size"]
            )
        except KeyError as kerr:
            self.logger.warning(f"is_different {keydoc}: key {kerr} not found -> different")
            return True

    def prepare_sync(self, remote_check=True):
        self.logger.info(f"sync : prepare-sync : {self.domain_filter} remote check {remote_check}")
        if remote_check:
            [self.get_document_characteristics(doc) for doc in self.get_document_tocheck_list()]

        to_del = []
        to_download = []

        # if more recent doc repo has not been synchronized, copy the reference one (the last one)
        if len(self.doc.keys()) == 0:
            self.doc = copy.deepcopy(self.refdoc)

        self.logger.debug(f"Ref doc keys {self.refdoc.keys()}")
        self.logger.debug(f" doc keys {self.doc.keys()}")

        # looking for obsolete documents
        for domain, docs in self.refdoc.items():
            for keydoc, docinfo in self.refdoc[domain].items():
                if 'title' not in docinfo:
                    # local file, no more available on ihe website
                    self.logger.info(f"Obsolete {keydoc} : mark to delete.")
                    to_del.append(docinfo)
                elif docinfo['domain'] not in self.domain_filter:
                    if os.path.exists(self.document_path(docinfo)):
                        self.logger.info("document present localy : delete")
                        to_del.append(docinfo)

        # looking for new documents
        for domain, docs in self.doc.items():
            if domain in self.domain_filter:
                self.logger.info(f"prepare_sync : domain {domain}")
                # domain to sync
                for keydoc, docinfo in self.doc[domain].items():
                    if 'title' in docinfo and (self.is_different(domain, keydoc) \
                                               or not self.check_local(docinfo)):
                        to_download.append(docinfo)
        return to_del, to_download

    def sync_all(self, to_del, to_download, confirm=True):
        """

        Sync documents : 
        - suppress all documents that are obsolete : not concerned aka not in domain_filter
        - test if a new document has to be download : new document available or new version of the document

        """
        disp = ["\nClean documents not in sync..."]

        for doc in to_del:
            disp.append(f"Obsolete document {doc['filename']} found: delete it...")
            if confirm:
                self.delete(doc)

        for doc in to_download:
            disp.append(f"Newer document {doc['filename']} found: download it...")
            if confirm:
                self.download(doc)

        [self.logger.info(s) for s in disp]
        if self.console:
            [print(s) for s in disp]

    def document_path(self, docinfo, createpath=False):
        """
        Build the path of the document, stored locally

        ;param dict docinfo: information about record describing the document
        """

        rootdir = os.path.join(self.outputdir, docinfo["domain"])
        self.logger.debug(f"document path {rootdir} [{docinfo['filename']}]")
        if not os.path.exists(rootdir) and createpath:
            os.makedirs(rootdir)

        return os.path.join(rootdir, docinfo["filename"])

    def download(self, docinfo):
        """
        Download the document from the IHE website locally
        The document is located in the domain it belongs to

        ;param dict docinfo: information about record describing the document

        """

        filename = self.document_path(docinfo, createpath=True)
        return helpers.download(docinfo["href"], filename, proxies=helpers.get_proxies(self.proxy))

    def delete(self, docinfo):
        """
        Delete the local files, previously downloaded, because
        these document is now obsolete e.g. nore longer linked
        into the IHE web page.

        :param dict docinfo: information about record to
        delete. delete the local file
        """

        filename = self.document_path(docinfo, createpath=True)
        dirname = os.path.dirname(filename)
        sucess, error = True, ''

        try:
            os.remove(filename)
            # remove dir if empty
            if not len(os.listdir(dirname)):
                os.removedirs(dirname)

            # suppress metatags also : etag, last-modified, size
            d = self.doc[docinfo['domain']][docinfo['filename']]
            self.logger.info(f"sync::delete d={d}")
            for key in ['etag', 'last-modified', 'size']:
                if key in d:
                    del d[key]

        except OSError as err:
            error = f"Error while deleting {filename} {str(err)}"
            sucess = False

        return sucess, error, filename

    def check_local(self, docinfo):
        """
        Check if the document is present locally
        Test if present and if sizes match

        :param dict docinfo: information about the doc
        :return bool: True if doc is up to date, False otherwise
        """
        filename = self.document_path(docinfo)

        if 'size' in docinfo and os.path.exists(filename):
            r = os.stat(filename)
            self.logger.info(f"check local {str(r.st_size)} / {str(docinfo['size'])}")
            return r.st_size == docinfo["size"]

        return False

    def scan_local_dirs(self) -> int:
        """
        Scan local repository and set information about documents already downloaded
        Update selected domain if necessary (a local file already present : domain selected)
        :return int: files count

        """

        # clean previous informations about local files
        for domain in list(filter(lambda k: k != "__meta__", self.doc.keys())):
            for doc in self.doc[domain]:
                if 'size' in self.doc[domain][doc].keys():
                    del self.doc[domain][doc]['size']
                if 'last-modified' in self.doc[domain][doc].keys():
                    del self.doc[domain][doc]['last-modified']

        total = 0
        for root, dirs, files in os.walk(self.outputdir):
            relative_path = root[len(str(self.outputdir)) + 1:]
            for name in files:
                if len(relative_path) and relative_path in self.doc:
                    r = os.stat(os.path.join(root, name))
                    self.logger.info(f'scan_local_dir : {name} [{r.st_size}] - relative_path {relative_path}')
                    if name not in self.doc[relative_path]:
                        self.doc[relative_path][name] = {"domain": relative_path,
                                                         "filename": name,
                                                         "size": r.st_size,
                                                         "last-modified": r.st_mtime}

                    self.doc[relative_path][name]["size"] = r.st_size
                    self.doc[relative_path][name]["last-modified"] = r.st_mtime

                    if relative_path not in self.domain_filter:
                        self.domain_filter.append(relative_path)

                    # copy the etag metadata of the previous downloaded file
                    try:
                        if self.doc[relative_path][name]["size"] == self.refdoc[relative_path][name]["size"]:
                            self.doc[relative_path][name]["etag"] = self.refdoc[relative_path][name]["etag"]
                    except KeyError as kerr:
                        self.logger.warning(f"Unkown local file {name} ({relative_path} : error {kerr})")

                    total += 1

        self.logger.info(f"END scan_local_dirs {self.domain_filter} - total found = {total}")
        return total

    def count_local_files(self, domain) -> int:
        """
            Return the files count that has been downloaded
            A file is said dowlooded if the meta size/last-modified are set in the dictionary
            :return int: count
        """
        count = len(list(filter(lambda x: 'size' in self.doc[domain][x] or 'last-modified' in self.doc[domain][x],
                                self.doc[domain])))
        self.logger.debug(f"sync:count_local_files domain {domain} = {count}")
        return count


def main():
    """
        Main 

        - argument parsing
        - process : load information, synchonize documents
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        help="output directory in wich the documents will be downloaded",
        default=str(DEFAULT_DOC_DIR),
    )
    parser.add_argument(
        "--confdir",
        help="directory containing the meta data about the documents",
        default=str(DEFAULT_CONF_DIR),
    )
    parser.add_argument(
        "--comment",
        help="get documents in public comments",
        action="store_true"
    )
    parser.add_argument(
        "--nosync",
        help="skip the download step",
        action="store_true"
    )
    parser.add_argument("--domain", help="specify domain(s)", default='')
    args = parser.parse_args()

    if not os.path.exists(args.confdir):
        os.makedirs(args.confdir)

    sy = Synchro(args.output, args.confdir, {}, console=True)
    sy.load_configuration()

    # if documents in public comment have to be downloaded
    # IHE Technical Framework Documents for Public Comment
    if args.comment:
        sy.public_comment = True

    # find all available documents
    sy.doc_cartography()

    # define domains to take into account
    # ALL means all domains
    if args.domain == 'ALL':
        sy.domain_filter = sy.get_all_domains()
    else:
        sy.domain_filter = args.domain.split(",") if len(args.domain) > 0 else []

    sy.display_available_docs()

    to_del, to_download = sy.prepare_sync()
    # sync with local directory
    sy.sync_all(to_del, to_download, confirm=not args.nosync)

    # save new data
    sy.save_infos()
    sy.save_configuration()


if __name__ == "__main__":
    main()
