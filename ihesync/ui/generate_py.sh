#!/bin/bash
python3 -m PyQt5.uic.pyuic -x ihesync_app.ui -o ihesync_app.py
python3 -m PyQt5.uic.pyuic -x sync_dialog.ui -o sync_dialog.py
python3 -m PyQt5.uic.pyuic -x progress_dialog.ui -o progress_dialog.py
python3 -m PyQt5.uic.pyuic -x about_dialog.ui -o about_dialog.py
pyrcc5 resources.qrc -o resources_rc.py