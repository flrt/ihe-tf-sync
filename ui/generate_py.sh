#!/bin/bash
python3 -m PyQt5.uic.pyuic -x ihesync_app.ui -o ihesync_app.py
python3 -m PyQt5.uic.pyuic -x sync_dialog.ui -o sync_dialog.py