#!/bin/bash
APP=ihesync
APPDIR=/usr/share/$APP
echo "Install ihesync in $APPDIR..."

sudo mkdir $APPDIR
sudo cp $APP $APPDIR/
sudo cp -r lib $APPDIR/
sudo cp $APP.desktop /usr/share/applications/$APP.desktop
sudo cp $APP.ico /usr/share/pixmaps/$APP.ico

