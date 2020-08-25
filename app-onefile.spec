# -*- mode: python -*-

block_cipher = None
import sys

a = Analysis(['app.py'],
             pathex=['/dev/ihe-tf-sync','/dev/ihe-tf-sync/ui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += []
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='iheapp',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True,
            icon='ihesync/ui/img/3_books.icns')
elif sys.platform == 'win32' or sys.platform == 'win64':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='iheapp',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='ihesync/ui/img/3_books.ico')
elif sys.platform == 'linux':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='iheapp',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='ihesync/ui/img/3_books.ico')

# Build a .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='iheapp.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                },
                icon='ihesync/ui/img/3_books.icns')