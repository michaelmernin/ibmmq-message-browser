# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['venv\\Lib\\site-packages', 'C:\\Program Files\\IBM\\MQ\\bin', 'C:\\Program Files\\IBM\\MQ', 'C:\\Program Files\\IBM\\MQ\\tools\\lib', 'C:\\Program Files\\IBM\\MQ\\tools\\cplus\\include', 'C:\\Program Files\\IBM\\MQ\\tools\\c\\include', 'C:\\Program Files\\IBM\\MQ\\java\\jre', 'C:\\Program Files\\IBM\\MQ\\java', 'C:\\Program Files\\IBM\\MQ\\tools\\lib', 'C:\\Program Files\\IBM\\MQ\\tools\\lib64'],
             binaries=[],
             datas=[('templates', 'templates'), ('static', 'static')],
             hiddenimports=['pywin32'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
