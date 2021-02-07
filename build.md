Build instructions
=================

# windows
Build the msi distribution file

    set base=c:\\dev\\py
    cd %base%\\ihe-tf-sync
    .\Scripts\activate
    pip install -r requirements.txt
    python setup.py bdist_msi

# linux
Build the tar.gz file by launching linux_build.sh. A Makefile should be better, and a flatpak config even more. Soon, perhaps.

# mac os
Build the app only with the following command line

    source bin/activate
    python setup.py bdist_mac --iconfile=ihesync/ui/img/ihesync.icns --custom-info-plist=Info.plist

Build the dmg archive with

    python setup.py bdist_dmg 