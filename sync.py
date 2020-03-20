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
import json
import argparse
import datetime
import locale
import copy
import requests
from bs4 import BeautifulSoup
import helpers

IHE_URL = "https://www.ihe.net"
IHE_TF_URL = f"{IHE_URL}/resources/technical_frameworks/"
IHE_COMMENT_URL = f"{IHE_URL}/resources/public_comment/"
DATA_ROOTDIR = "data"
DOC_INFO_FILENAME = "docs.json"
GENERAL_INFO_FILENAME = "infos.txt"
META_TAG = "__meta__"

class Synchro:
    def __init__(self, outputdir, refdoc={}):
        """
        Constructor

        :param str outputdir: directory (root) containing downloaded files
        :param dict refdoc: dictionnary containing reference
            configuration (previous)
        """
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')

        self.refdoc = refdoc
        self.doc = {}
        self.outputdir = outputdir
        self.last_check = None
        self.domain_filter = []
        self.public_comment = False
        self.get_meta()

    def get_all_domains(self):
        if self.doc:
            return list(self.doc.keys())
        elif self.refdoc:
            return list(self.refdoc.keys())
        else:
            return ['TF','PAT','CARD','DENT','ENDO','EYECARE',
                'ITI','SUPPL','LAB','PALM','PCC','PHDSC','PCD',
                'PHARMACY','QRPH','QUALITY','RO','RAD']

    def get_meta(self):
        if self.refdoc:
            if META_TAG in self.refdoc:
                self.last_check = datetime.datetime.strptime(self.refdoc[META_TAG]["last_check"],
                    "%Y-%m-%dT%H:%M:%S.%f")
                self.domain_filter = self.refdoc[META_TAG]["domains"]
                self.public_comment = self.refdoc[META_TAG]["public_comment"]

                del self.refdoc[META_TAG]
            else:
                # config not explicit, guess it
                ddocs=[list(filter(lambda x: "etag" in x, v.values())) for k,v in self.refdoc.items()]
                domains = set()

                # iterate through downloaded docs (ddocs = list by domain)
                for doclist in ddocs:
                    for doc in doclist:
                        domains.add(doc['domain'])

                        parsed=None
                        try:
                            parsed = datetime.datetime.strptime(str(doc['last-modified']),'%a, %d %b %Y %H:%M:%S %Z')
                            if (self.last_check and parsed < self.last_check) or self.last_check is None:
                                self.last_check = parsed
                        except:
                            pass
                
                self.domain_filter=list(domains)
              
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

    def get_document_characteristics(self, doc):
        """
        get infos on document by making an HEAD request to get meta data on document (size, etag, etc.)

        :param dict doc: Title of the document
        :param str href: URL of the document
        :return dict: dict with informations about the resource
        """

        if doc["domain"] in self.domain_filter:
            print(".", end="", flush=True)
            # get more info with a HEAD request
            try:
                headreq = requests.head(doc['href'])

                if headreq.status_code == 200:
                    doc["last-modified"] = headreq.headers["Last-Modified"]
                    doc["size"] = int(headreq.headers["Content-Length"])
                    doc["etag"] = headreq.headers["Etag"]
                else:
                    sys.stderr.write(f"Error {headreq.status_code} - URL={doc['href']}\n")
            except Exception as ex:
                sys.stderr.writelines([f"Error HEAD request {doc['href']}", str(ex), "\n"])

        return doc

    def doc_cartography(self):
        """
        Load IHE html pages 
            Technical Framework
            Public comments if set
        """

        self.load_ihe_page(IHE_TF_URL)
        if self.public_comment:
            self.load_ihe_page(IHE_COMMENT_URL)
        self.last_check = datetime.datetime.now().isoformat()

    def load_ihe_page(self, webpage=IHE_TF_URL):
        """
        Load IHE html page
        Find documents
        Classify them
        """

        unsorted_docs = {}
        req = requests.get(webpage)
        doc_class = webpage.split('/')[-2]

        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html5lib")
            links = list(filter(lambda x: x.get("href"), soup.find_all("a")))
            pdf_list = list(filter(lambda x: x.get("href").endswith(".pdf"), links))

            print("Get information about documents")
            for link in pdf_list:
                docinfo = self.get_infos(link.text, link.get("href"), doc_class)
                unsorted_docs[docinfo["filename"]] = docinfo
        print(f"\n{len(unsorted_docs)} documents found in IHE website : {doc_class}")
        self.classify(unsorted_docs)

        
    def display_available_docs(self):
        """
        Display how many documents are available in each domain.
        """
        print("\nAvailable documents :")
        for key, value in self.doc.items():
            print(f"{key}: {len(value)} documents")


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
                    # print(f"Moving documents from {k2} to {k}")
                    for keydoc, docinfo in self.doc[k2].items():
                        self.doc[k][keydoc] = docinfo
                    self.doc[k2] = {}
        # delete empty domains
        for k in keys:
            if not len(self.doc[k]):
                del self.doc[k]

    def save(self, filename):
        sdoc = copy.deepcopy(self.doc)
        sdoc[META_TAG]=dict(last_check=self.last_check, public_comment=self.public_comment, domains=self.domain_filter)
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
        if not ("etag" in self.refdoc and "etag" in self.doc):
            return False
        if not ("size" in self.refdoc and "size" in self.doc):
            return False
        return (
            self.doc[domain][keydoc]["etag"] != self.refdoc[domain][keydoc]["etag"]
            and self.doc[domain][keydoc]["size"] != self.refdoc[domain][keydoc]["size"]
        )

    def prepare_sync(self):
        for domain, docs in self.doc.items():
            [self.get_document_characteristics(doc) for doc in docs.values()]

        to_del = []
        to_download = []

        # if more recent doc repo has not been synchronized, copy the reference one (the last one)
        if len(self.doc.keys())==0:
            self.doc = copy.deepcopy(self.refdoc)

        # looking for obsolete documents
        for domain, docs in self.refdoc.items():
            for keydoc, docinfo in self.refdoc[domain].items():
                if "etag" in docinfo:
                    # already downloaded

                    if (docinfo['domain'] not in self.domain_filter
                        or
                        keydoc not in self.doc[domain]
                        or "etag" not in self.doc[domain][keydoc]
                    ):
                        to_del.append(docinfo)

        # looking for new documents
        for domain, docs in self.doc.items():
            if domain in self.domain_filter:
                # domain to sync
                for keydoc, docinfo in self.doc[domain].items():
                    if domain not in self.refdoc:
                        self.refdoc[domain] = {}

                    if self.is_different(domain, keydoc) or not self.check_local(
                        docinfo
                    ):
                        to_download.append(docinfo)
        return to_del, to_download

    def sync_all(self, confirm=True):
        """

        Sync documents : 
        - suppress all documents that are obsolete : not concerned aka not in domain_filter
        - test if a new document has to be download : new document available or new version of the document

        """
        to_del, to_download = self.prepare_sync()

        print("\nClean documents not in sync...")
        for doc in to_del:
            print(f"Obsolete document {doc['filename']} found: delete it...")
            if confirm:
                self.delete(doc)

        for doc in to_download:
            print(f"Newer document {doc['filename']} found: download it...")
            if confirm:
                self.download(doc)

    def document_path(self, docinfo):
        """
        Build the path of the document, stored locally

        ;param dict docinfo: information about record describing the document
        """

        rootdir = os.path.join(self.outputdir, docinfo["domain"])
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)

        return os.path.join(rootdir, docinfo["filename"])

    def download(self, docinfo):
        """
        Download the document from the IHE website locally
        The document is located in the domain it belongs to

        ;param dict docinfo: information about record describing the document

        """

        filename = self.document_path(docinfo)
        helpers.download(docinfo["href"], filename)

    def delete(self, docinfo):
        """
        Delete the local files, previously downloaded, because
        these document is now obsolete e.g. nore longer linked
        into the IHE web page.

        :param dict docinfo: information about record to
        delete. delete the local file
        """

        filename = self.document_path(docinfo)
        dirname = os.path.dirname(filename)
        try:
            os.remove(filename)
            # remove dir if empty
            if not len(os.listdir(dirname)):
                os.removedirs(dirname)
        except OSError as err:
            sys.stderr.writelines(
                [f"Error while deleting {filename}\n", str(err), "\n"]
            )

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
            return r.st_size == docinfo["size"]

        return False


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
        default=str(Path(Path.home(), 'ihe_documents')),
    )
    parser.add_argument(
        "--confdir",
        help="directory containing the meta data about the documents",
        default=str(Path(Path.home(), '.ihe-sync')),
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

    # Load previous configuration if presen
    docfilename = os.path.join(args.confdir, DOC_INFO_FILENAME)
    previous_docs = helpers.load_json(docfilename)

    sy = Synchro(args.output, previous_docs)

    # if documents in public comment have to be downloaded
    # IHE Technical Framework Documents for Public Comment
    if args.comment:
        sy.public_comment = True
    
    # find all available documents
    sy.doc_cartography()

    # define domains to take into account
    # ALL means all domains
    if args.domain=='ALL':
        sy.domain_filter = sy.get_all_domains()
    else:
        sy.domain_filter = args.domain.split(",") if len(args.domain)>0 else []

    sy.display_available_docs()

    # sync with local directory
    sy.sync_all(confirm=not args.nosync)
 
    # save new data
    sy.save_infos()
    sy.save(docfilename)


if __name__ == "__main__":
    main()