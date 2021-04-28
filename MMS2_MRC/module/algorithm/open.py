#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 
"""

import sys
sys.path.append(r'E:\Work\Hitec\MSZC\MSS2\05source\MMS2_MRC')
import click
from module.algorithm.netcdf.netcdf import Nc
from module.algorithm.netcdf.hdf import HDF
from module.algorithm.micaps.pymicaps import M4
from module.algorithm.grib.grib_info import GRIBInfo




@click.command()
@click.option('--hr', help='Open HDF File.')
@click.option('--nr', help='Open NetCDF File.')
@click.option('--mr', help='Open MICAPS4 File.')
@click.option('--gr', help='Open GRIB File.')
def open(hr,nr,mr,gr):
    dataType=''
    info=''
    if not hr==None and len(hr)>0:
        meteo = HDF(hr)
        dataType='HDF'
        info = meteo.print_property_info()
    if not nr==None and len(nr)>0:
        meteo = Nc(nr)
        dataType='NetCDF'
        info = meteo.print_property_info()
    if not mr==None and len(mr)>0:
        meteo = M4(mr)
        dataType='Micaps4'
        info = meteo.print_property_info()
    if not gr==None and len(gr)>0:
        meteo = GRIBInfo(gr)
        dataType='GRIB'
        info = meteo.print_property_info()


    click.echo(dataType+' Data:\n%s\n' % info)


if __name__ == "__main__":
    open()