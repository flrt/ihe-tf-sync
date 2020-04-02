#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    helpers functions
    
"""

__author__ = "Frederic Laurent"
__version__ = "1.0"
__copyright__ = "Copyright 2018, Frederic Laurent"
__license__ = "MIT"


import os.path
import json
import sys
from json.decoder import JSONDecodeError
from datetime import datetime, date
import io
import requests
import shutil

def save_json(filename, data):
    bdir = os.path.dirname(filename)
    if not os.path.exists(bdir):
        os.makedirs(bdir)

    with io.open(filename, "w") as fout:
        fout.write(json.dumps(data, sort_keys=True, indent=4, default=json_encoder))

def load_json(filename):
    """
    Lecture d'un fichier de configuration au format JSON
    Produit un dictionnaire python

    :param config_filename: nom du fichier
    :return: données lues dans 1 dictionnaire
    """
    data = {}

    if not os.path.exists(filename):
        return data
    else:
        with io.open(filename, "r", encoding="utf-8") as fin:
            try:
                udata = fin.read()
                data = json.loads(udata.encode("utf-8"))
            except TypeError as msg_e:
                sys.stderr.write("load_json_config typeError :%s" % msg_e)
            except JSONDecodeError as msg_j:
                sys.stderr.write("load_json_config JSONdecode :%s" % msg_j)
    return data

def download(url, filename):
    """
        Telechargement de l'URL dans le fichier destination
    :param url: URL a telecharger
    :param filename: fichier de destination
    """

    try:
        req = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            shutil.copyfileobj(req.raw, f)
    except Exception as ex:
        sys.stderr.writelines([f"Error while downloading {url}", str(ex), "\n"])
    return filename

def json_encoder(obj):
    """JSON encoder for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))