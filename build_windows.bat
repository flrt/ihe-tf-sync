python -m PyQt5.uic.pyuic --import-from="ihesync.ui" -o ihesync\ui\about_dialog.py ihesync\ui\about_dialog.ui
python -m PyQt5.uic.pyuic --import-from="ihesync.ui" -o ihesync\ui\ihesync_app.py ihesync\ui\ihesync_app.ui
python -m PyQt5.uic.pyuic --import-from="ihesync.ui" -o ihesync\ui\prepare_dialog.py ihesync\ui\prepare_dialog.ui
python -m PyQt5.uic.pyuic --import-from="ihesync.ui" -o ihesync\ui\progress_dialog.py ihesync\ui\progress_dialog.ui
python -m PyQt5.uic.pyuic --import-from="ihesync.ui" -o ihesync\ui\sync_dialog.py ihesync\ui\sync_dialog.ui

python setup.py build_exe
python setup.py bdist_msi