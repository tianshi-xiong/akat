# -*- mode: python -*-

block_cipher = None


a = Analysis(['akat.py'],
             pathex=['..\\AKAT','C:\\Python27\\Lib\\site-packages\\PyInstaller\\loader\\rthooks'],
             binaries=None,
             datas=None,
             hiddenimports=['sip'],
             hookspath=[],
             runtime_hooks=['pyi_rth_qt4plugins_xth.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='AKAT',
          debug=False,
          strip=False,
          upx=True,
          console=False )
#images_tree=Tree('.\\images', prefix='images')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='AKAT')