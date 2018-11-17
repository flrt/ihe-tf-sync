#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Synchronize locally all (or part of) documents available 
    on IHE.net

"""

__author__ = "Frederic Laurent"
__version__ = "1.0"
__copyright__ = "Copyright 2018, Frederic Laurent"
__license__ = "MIT"

import os.path
import sys
import requests
import json
import argparse
import datetime
from bs4 import BeautifulSoup
import helpers


IHE_URL = "https://www.ihe.net"
IHE_TF_URL = f"{IHE_URL}/resources/technical_frameworks/"
DATA_ROOTDIR = "data"
DOC_INFO_FILENAME = "docs.json"
GENERAL_INFO_FILENAME = "infos.txt"


class Synchro:
    def __init__(self, outputdir, refdoc={}):
        """
        Constructor

        :param str outputdir: directory (root) containing downloaded files
        :param dict refdoc: dictionnary containing reference
            configuration (previous)
        """
        self.refdoc = refdoc
        self.doc = {}
        self.outputdir = outputdir

    def get_infos(self, title, href, domain_filter):
        """
        get infos on document via URL
        retrieve domain name (e.g. RAD, ITI, etc.)
        make an HEAD request to get meta data on document (size, etag, etc.)

        :param str title: Title of the document
        :param str href: URL of the document
        :param list domain_filter: list of domain to take into account
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

        docinfo = {
            "domain": parts[0].upper().split("-")[0],
            "typedoc": parts[1],
            "filename": docname,
            "href": _href,
            "title": title,
        }

        if not domain_filter or (domain_filter and docinfo['domain'] in domain_filter):
            print('.', end='')
            # get more info with a HEAD request
            try:
                headreq = requests.head(_href)

                if headreq.status_code == 200:
                    docinfo["last-modified"] = headreq.headers["Last-Modified"]
                    docinfo["size"] = int(headreq.headers["Content-Length"])
                    docinfo["etag"] = headreq.headers["Etag"]
                else:
                    sys.stderr.write(f"Error {headreq.status_code} - URL={_href}\n")
            except Exception as ex:
                sys.stderr.writelines([f"Error HEAD request {_href}", str(ex), "\n"])

        return docinfo

    def load_main_page(self, domain_filter=None):
        """
        Load main html page
        Find documents
        Classify them

        :param list domain_filter: list of domain to take into account
        """

        unsorted_docs = {}
        req = requests.get(IHE_TF_URL)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html5lib")
            links = list(filter(lambda x: x.get("href"), soup.find_all("a")))
            pdf_list = list(filter(lambda x: x.get("href").endswith(".pdf"), links))

            print("Get information about documents")
            for link in pdf_list:
                docinfo = self.get_infos(link.text, link.get("href"), domain_filter)
                unsorted_docs[docinfo["filename"]] = docinfo
        print(f"\n{len(unsorted_docs)} documents found in IHE website.")
        self.classify(unsorted_docs)

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
                    print(f"Moving documents from {k2} to {k}")
                    for keydoc, docinfo in self.doc[k2].items():
                        self.doc[k][keydoc] = docinfo
                    self.doc[k2] = {}
        # delete empty domains
        for k in keys:
            if not len(self.doc[k]):
                del self.doc[k]

    def save_infos(self, domains):
        """
        Save global informations about IHE documents
        """
        infofn = os.path.join(self.outputdir, GENERAL_INFO_FILENAME)
        with open(infofn, "w") as fout:
            fout.write(f"Last checked : {datetime.datetime.now().isoformat()}\n")
            if domains:
                fout.write(f"Checked {','.join(domains)} domains.\n\n")
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
        return (
            self.doc[domain][keydoc]["etag"] != self.refdoc[domain][keydoc]["etag"]
            and self.doc[domain][keydoc]["size"] != self.refdoc[domain][keydoc]["size"]
        )

    def sync_all(self, domain_filter=None):
        # looking for new documents
        for domain, docs in self.doc.items():
            if domain_filter is None or domain in domain_filter:
                print(f"Syncing {domain} domain...")
                # domain to sync
                for keydoc, docinfo in self.doc[domain].items():
                    if domain not in self.refdoc:
                        self.refdoc[domain] = {}

                    if keydoc in self.refdoc[domain]:
                        # doc already present and verify local copy
                        if self.is_different(domain, keydoc) or not self.check_local(
                            docinfo
                        ):
                            print(f"Newer document {keydoc} found: update it...")
                            self.download(docinfo)

                    else:
                        # doc does not exist
                        print(f"New document {keydoc} found: download it...")
                        self.download(docinfo)
        # looking for obsolete documents
        for domain, docs in self.refdoc.items():
            if domain_filter is None or domain in domain_filter:
                for keydoc, docinfo in self.refdoc[domain].items():
                    if keydoc not in self.doc[domain]:
                        print(f"Obsolete document {keydoc} found: delete it...")
                        self.delete(docinfo)

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
        Delete the localfile, previously downloaded, because
        these document is now obsolete e.g. nore longer linked
        into the IHE web page.

        :param dict docinfo: information about record to
        delete, in the end, delete the local file
        """

        filename = self.document_path(docinfo)
        try:
            os.remove(filename)
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

        if os.path.exists(filename):
            r = os.stat(filename)
            return r.st_size == docinfo["size"]

        return False


def main():
    """
        Programme principal

        - parse les arguments
        - lance les traitements
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        help="output directory in wich the documents will be downloaded",
        default="documents",
    )
    parser.add_argument(
        "--confdir",
        help="directory containing the meta data about the documents",
        default="conf",
    )
    parser.add_argument("--domain", help="specify domain(s)", default=None)
    args = parser.parse_args()

    domains = None
    if args.domain:
        domains = args.domain.split(",")

    confdir = os.path.join(DATA_ROOTDIR, args.confdir)
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    outputdir = os.path.join(DATA_ROOTDIR, args.output)

    # Load previous configuration if presen
    docfilename = os.path.join(confdir, DOC_INFO_FILENAME)
    previous_docs = helpers.load_json(docfilename)

    sy = Synchro(outputdir, previous_docs)
    # find all available documents
    sy.load_main_page(domains)

    # sync with local directory
    sy.sync_all(domains)

    # save new data
    sy.save_infos(domains)
    helpers.save_json(docfilename, sy.doc)


if __name__ == "__main__":
    main()
