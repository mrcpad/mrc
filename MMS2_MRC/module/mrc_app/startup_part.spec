# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(100000)

block_cipher = None


a = Analysis(['startup.py'],
             pathex=['D:\\Python3\\Lib\site-packages','D:\\workspace09\\MMS2_MRC','D:\\workspace09\\MMS2_MRC\\module','D:\\workspace09\\MMS2_MRC\\module\\mrc_app','D:\\workspace09\\MMS2_MRC\\module\\algorithm\\src'],
             binaries=[('D:\\workspace09\\MMS2_MRC\\lib\\net\\grib2Parameters.xml','.'),('D:\\workspace09\\MMS2_MRC\\config\\log.txt','logs'),('D:\\workspace09\\MMS2_MRC\\config\\log.txt','logs\\errorlogs'),
             ('D:\\workspace09\\MMS2_MRC\\lib\\net','lib\\net')],
             datas=[('D:\\workspace09\\MMS2_MRC\\config\\config.xml','config'),('D:\\workspace09\\MMS2_MRC\\config\\menu.xml','config'),('D:\\workspace09\\MMS2_MRC\\config\\toolbar.xml','config'),
             ('D:\\workspace09\\MMS2_MRC\\config\\image\\*','config\\image')],
             hiddenimports=['numpy','numpy.ma.core','netCDF4','cftime','wrapt','matplotlib', 'module.mrc_command.menu.openfilecmd','module.mrc_command.menu.exitcmd',
             'module.mrc_command.tool.toolopenfilecmd','module.mrc_command.tool.toolconvertcmd','module.mrc_command.menu.convertcmd',
             'module.mrc_command.menu.ExportDataCmd','module.mrc_command.menu.newConvertcmd','module.mrc_command.menu.newFilecmd','module.mrc_command.menu.OpenRemoteFileCmd','module.mrc_command.menu.quitcmd',
             'module.mrc_command.menu.convert.hdf2m4','module.mrc_command.menu.convert.hdf2nc','module.mrc_command.menu.convert.m42hdf','module.mrc_command.menu.convert.m42nc','module.mrc_command.menu.convert.nc2hdf','module.mrc_command.menu.convert.nc2m4',
             'module.mrc_command.tool.convertcmd','module.mrc_command.tool.removecmd'],
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
          [],
          exclude_binaries=True,
          name='startup',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mrc')




#chcp 65001