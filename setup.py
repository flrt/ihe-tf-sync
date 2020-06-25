#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

import sys, os
from cx_Freeze import setup, Executable

APPNAME = 'ihesync'
APPDESCR = 'Synchronize published documents on ihe.net website locally.'
MAIN = 'ihesync/ui/app.py'
__version__ = '2.0'
__author__ = "Frederic Laurent"
#############################################################################
# preparation des options
 
# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path + ["ihesync", "ihesync/ui"]
 
# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = []
packages = []  # nommer les packages utilises

buildOptions = dict(packages=["multiprocessing"], excludes=["tkinter"])


winOptions = {"upgrade-code": "44aad47f-38bd-4fcf-b70c-b0b4cf3f246b",
              "initial_target_dir": r'[ProgramFilesFolder]\%s' % APPNAME,
              "install_icon": "assets/icon.ico",
              "target_name": APPNAME}

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = []

base = None

if sys.platform == "win32":
    base = "Win32GUI"
    # includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici
 
# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
 
# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True
 
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "create_shared_zip": False,  # <= ne pas generer de fichier zip
           "include_in_shared_zip": False,  # <= ne pas generer de fichier zip
           "compressed": False,  # <= ne pas generer de fichier zip
           "optimize": optimize,
           "silent": silent
           }
 
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True
 
#############################################################################
# preparation des cibles

target_app = [Executable(
    script=MAIN,
    base=base,
    targetName=APPNAME,
    icon="assets/icon.ico"
    )]


#############################################################################
# creation du setup
if sys.platform == "win32":
    setup(
    name=APPNAME,
    version=__version__,
    description=APPDESCR,
    packages=[APPNAME],
    options={"build_exe": buildOptions, "sdist_msi": winOptions},
    executables=target_app,
    author=__author__,
    )
elif sys.platform == "linux":
    setup(
    name=APPNAME,
    version=__version__,
    description=APPDESCR,
    packages=[APPNAME],
    options={"build_exe": buildOptions, "sdist_msi": winOptions},
    executables=target_app,
    author=__author__,
    )
