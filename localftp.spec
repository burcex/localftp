# -*- mode: python -*-
a = Analysis(['localftp.py'],
             pathex=['E:\\cygwin\\cygwin\\home\\march\\python\\localftp'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='localftp.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
