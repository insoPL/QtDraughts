# -*- mode: python -*-

block_cipher = None

icon_path = 'graphics\\icon.ico'
full_name = 'QtDraughts'

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['_cffi_backend'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=full_name,
          debug=False,
          onefile=True,
          windowed=True,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon=icon_path)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='draug')
app = BUNDLE(coll,
             name=full_name+'.app',
             icon=icon_path,
             bundle_identifier = 'com.insoPL.'+full_name )