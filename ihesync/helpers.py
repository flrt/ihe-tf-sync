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
from json.decoder import JSONDecodeError
from datetime import datetime, date
import io
import requests
import shutil
import pathlib
import logging

logger = logging.getLogger()


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
                logger.error("load_json_config typeError :%s" % msg_e)
            except JSONDecodeError as msg_j:
                logger.error("load_json_config JSONdecode :%s" % msg_j)
    return data


def download(url, filename, proxies=None):
    """
        Telechargement de l'URL dans le fichier destination
    :param url: URL a telecharger
    :param filename: fichier de destination
    """
    error = ''

    try:
        req = requests.get(url, proxies=proxies, stream=True)

        with open(filename, "wb") as f:
            shutil.copyfileobj(req.raw, f)
    except FileNotFoundError as fnf:
        error = f"Error while downloading {url} - I/O Problem with {filename} : FileNotFound -> check path"
    except Exception as ex:
        error = f"Error while downloading {url}. {str(ex)}"

    return len(error) == 0, error, filename


def json_encoder(obj):
    """JSON encoder for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, pathlib.Path):
        return str(obj)

    raise json.JSONEncoder.default(obj)
