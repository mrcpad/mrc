# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None



a = Analysis(['ffc_v5.py'],
             pathex=['/home/trywangdao/miniconda3/bin/python','/home/trywangdao/miniconda3/lib/python3.7/site-packages','/home/trywangdao/file/clickUtil','/home/trywangdao/file',],
             binaries=[],
             datas=[('/home/trywangdao/download/installecCodes/bin','.installeccodes/bin'),('/home/trywangdao/download/installecCodes/include','.installeccodes/include'),
             ('/home/trywangdao/download/installecCodes/lib','.installeccodes/lib'),('/home/trywangdao/download/installecCodes/share','.installeccodes/share')],
             hiddenimports=['numpy','numpy.ma.core.MaskedArray','netCDF4','cftime','wrapt','pyproj','ncepgrib2','pygrib','matplotlib','basemap'],
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
          name='mrc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )