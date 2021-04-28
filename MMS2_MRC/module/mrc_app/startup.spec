# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['startup_new.py'],
             pathex=['D:\\Python3\\Lib\site-packages','D:\\workspace11\\mrc','D:\\workspace11\\mrc\\module','D:\\workspace11\\mrc\\module\\mrc_app','D:\\workspace11\\mrc\\module\\algorithm\\src'],
             binaries=[('D:\\workspace11\\mrc\\lib\\net\\grib2Parameters.xml','.'),('D:\\workspace11\\mrc\\config\\log.txt','logs'),('D:\\workspace11\\mrc\\config\\log.txt','logs\\errorlogs'),
             ('D:\\workspace11\\mrc\\lib\\net','lib\\net')],
             datas=[('D:\\workspace11\\mrc\\config\\config.xml','config'),('D:\\workspace11\\mrc\\config\\menu.xml','config'),('D:\\workspace11\\mrc\\config\\toolbar.xml','config'),
             ('D:\\workspace11\\mrc\\config\\image\\*','config\\image')],
             hiddenimports=['numpy','numpy.ma.core','netCDF4','cftime','wrapt','matplotlib', 'module.mrc_command.menu.openfilecmd','module.mrc_command.menu.exitcmd',
             'module.mrc_command.tool.toolopenfilecmd','module.mrc_command.tool.toolconvertcmd','module.mrc_command.menu.convertcmd',
             'module.mrc_command.menu.ExportDataCmd','module.mrc_command.menu.newConvertcmd','module.mrc_command.menu.newFilecmd','module.mrc_command.menu.OpenRemoteFileCmd','module.mrc_command.menu.quitcmd',
             'module.mrc_command.menu.convert.hdf2m4','module.mrc_command.menu.convert.hdf2nc','module.mrc_command.menu.convert.m42hdf','module.mrc_command.menu.convert.m42nc','module.mrc_command.menu.convert.nc2hdf','module.mrc_command.menu.convert.nc2m4',
             'module.mrc_command.tool.convertcmd','module.mrc_command.tool.removecmd','module.mrc_command.menu.Savefilecmd'],
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
          console=False ,icon='D:\\workspace11\\mrc\\config\\image\\hpc_logos.ico')



#chcp 65001