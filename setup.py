#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

import sys, os
from cx_Freeze import setup, Executable

APPNAME = 'ihesync'
APPDESCR = 'Synchronize published documents on ihe.net website locally.'
MAIN = 'ihesync/ui/app.py'
APP_ICON = f'{APPNAME}/ui/img/ihesync.ico'
APP_ICNS = f'{APPNAME}/ui/img/ihesync.icns'

__version__ = '2.1'
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
              "install_icon": APP_ICON,
              "target_name": APPNAME}
macOptions = {"iconfile": APP_ICNS, "custom_info_plist": "Info.plist"}
dmgOptions = {"volume_label": APPNAME, "applications_shortcut": True}

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = []
binpathincludes = []

if sys.platform == "linux":
    binpathincludes += ["/usr/lib"]

# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

if sys.platform == "win32":
    # options["include_msvcr"] = True
    buildOptions["include_msvcr"] = True
    setup(
        name=APPNAME,
        version=__version__,
        description=APPDESCR,
        packages=[APPNAME],
        options={"build_exe": buildOptions, "sdist_msi": winOptions},
        executables=[Executable(MAIN, base="Win32GUI", targetName=APPNAME, icon=APP_ICON)],
        author=__author__,
    )
elif sys.platform == "linux":
    setup(
        name=APPNAME,
        version=__version__,
        description=APPDESCR,
        packages=[APPNAME],
        options={"build_exe": buildOptions},
        executables=[Executable(MAIN, base=None, targetName=APPNAME, icon=APP_ICON)],
        entry_points={'console_scripts': ['ihesync=ihesync.ui.app:main']},
        data_files=[('share/applications', [f'{APPNAME}.desktop'])],
        classifiers=["License :: OSI Approved :: BSD License"],
        author=__author__,
    )
    # includefiles += [...] : ajouter les recopies specifiques à Linux
elif sys.platform == "darwin":
    setup(name=APPNAME,
          version=__version__,
          description=APPDESCR,
          packages=[APPNAME],
          options={"build_exe": buildOptions, "bdist_mac": macOptions, "bdist_dmg": dmgOptions},
          executables=[Executable(MAIN, base=None, targetName=APPNAME, icon=APP_ICON)],
          )
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici

# On Mac OS
# python setup.py bdist_mac --iconfile=assets/banana.icns --custom-info-plist=Info.plist
