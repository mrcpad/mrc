# -*- coding: utf-8 -*-

import sys

import os
ppath = os.path.abspath('..')
sys.path.append(ppath)
import time
import threading


from m4_to_nc.m4_to_nc import m4_to_nc_batGenNCfile
from m4_to_hdf.m4_to_hdf import m4_to_hdf_batGenNCfile
from hdf_to_m4.hdf_m4_v2 import HDF_to_M4
from nc_to_m4.nc_m4_v2 import NC_to_M4
from grib.grib_to_nc import grib_to_nc_batGenNCfile
from grib.grib_to_m4 import Grib_to_M4
from grib.grib_to_hdf import grib_to_hdf_batGenNCfile

from netcdf.convert2netCDF import nc2hdf,hdf2nc

from netcdf.hdf import HDF
from netcdf.netcdf import Nc



import click

class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def copy(src, dst):
    """Move file SRC to DST."""
    for fn in src:
        click.echo('move %s to folder %s' % (fn, dst))



def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()





@click.group()

def climain():

    click.echo(click.style('Initializing shell.......... !', bg='black', fg='green'))
    time.sleep(1)



@climain.command(options_metavar='<-sh>')
@click.option('--sh','-sh', help='eg.: <mrc info -sh /ncfile.nc>', default=os.path.abspath('.'))

def info(sh):

    """This script show file information.  Commands:--help"""
    if sh:

        if os.path.isfile(sh):
            click.echo(click.style('showinfo--%s'% sh, bg='black', fg='green'))
            time.sleep(1)
            click.echo(click.style('Running showinfo shell.......... !', bg='black', fg='green'))
            time.sleep(1)
            expath = sh.split('.')[1].upper()
            if expath == 'HDF':
                h = HDF(sh)
                print(h.print_property_info())
            elif expath == 'NC':
                c = Nc(sh)
                print(c.print_property_info())
            elif expath == 'GRIB':
                pass
            else:
                click.echo(click.style('Invalid File:%s!' % sh, bg='black', fg='bright_red'))



        else:
            click.echo(click.style('sh:%s not file ,Your File please!' % sh, bg='black', fg='bright_red'))
    else:

        click.echo(click.style('Your File please!', bg='black', fg='bright_red'))






'''@climain.command()
def dropdb():
    click.echo('Dropped the database')'''







@climain.command(options_metavar='<-ft> <-vn>')
@click.option('--ft','-ft', help='eg.: <mrc convert -ft nm -vn "" /src/m4  /des/ncfile.nc>',type=click.Choice(['nh', 'hn','nm',\
            'mn','hm','mh','gn','gm','gh']))
@click.option('--vn','-vn', default='variable000', prompt='Your Variables please',help='Variables needed to generate nc files or hdf files',metavar='<-vn>')
@click.argument('src', nargs=-1,type=click.Path(), metavar='<src>')
@click.argument('dst', nargs=1,type=click.Path(), metavar='<dst>')
@click.confirmation_option(prompt='Are you sure you want to ft file?')

def convert(ft,vn, src, dst):


    """This script Implementing different files File Format Conversion.  Commands:--help"""

    click.echo(click.style('Init shell.......... %s!'%ft, bg='black', fg='green'))
    time.sleep(1)
    click.echo(click.style('Checking %s' % ','.join(src), bg='black', fg='green'))
    time.sleep(1)
    click.echo(click.style('Checking %s' % dst, bg='black', fg='green'))
    time.sleep(1)
    click.echo(click.style('Running %s shell!' % ft, bg='black', fg='green'))
    time.sleep(1)

    if not src:
        #click.echo('empty src!')
        click.echo(click.style('empty src!', bg='black', fg='bright_red'))
        sys.exit(0)

    if src:

        v = ft
        for case in switch(v):
            if case('nh'):
                flag = 0
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        ncList = getNCBatFiles(srcFile)
                        batNCToHDFFileDeal(ncList, dst)
                    else:
                        if os.path.exists(srcFile):
                            (filepath, tempfilename) = os.path.split(srcFile)
                            (filename, extension) = os.path.splitext(tempfilename)
                            nc2hdf(srcFile, os.path.join(dst, filename + '.hdf'))
                        else:
                            flag = 1
                            print('src:%s not exist!' % srcFile)
                            continue
                if flag == 0:
                    click.echo(click.style('Successful file generation', bg='black', fg='green'))
                break
            if case('hn'):

                for srcFile in src:
                    if os.path.isdir(srcFile):
                        hdfList = getHDFBatFiles(srcFile)
                        batHDFToNCFileDeal(hdfList, dst)
                    else:
                        if os.path.exists(srcFile):
                            (filepath, tempfilename) = os.path.split(srcFile)
                            (filename, extension) = os.path.splitext(tempfilename)
                            hdf2nc(srcFile, os.path.join(dst, filename + '.nc'))
                        else:
                            print('src:%s not exist!' % srcFile)
                            continue


                click.echo(click.style('Successful file generation', bg='black', fg='green'))
                break
            if case('nm'):
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        ncList = getNCBatFiles(srcFile)
                        for nc in ncList:
                            c = NC_to_M4(nc, dst,'')
                    else:
                        c = NC_to_M4(srcFile, dst, '')
                    if c.flag == 0:
                        click.echo(click.style('Successful file generation', bg='black', fg='green'))
                    else:
                        click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))
                        continue
                break
            if case('mn'):
                for srcFile in src:
                    if vn == '':
                        flag = m4_to_nc_batGenNCfile(srcFile, dst, 'variable000')
                        if flag == 0:
                            click.echo(click.style('Successful file generation', bg='black', fg='green'))
                        else:
                            click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))
                            continue
                    else:

                        flag = m4_to_nc_batGenNCfile(srcFile, dst, vn)
                        if flag == 0:
                            click.echo(click.style('Successful file generation', bg='black', fg='green'))
                        else:
                            click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))

                break
            if case('hm'):
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        hdfList = getHDFBatFiles(srcFile)
                        for hdf in hdfList:
                            c = HDF_to_M4(hdf, dst, '')
                    else:
                        c = HDF_to_M4(srcFile, dst, '')


                    if c.flag == 0:
                        click.echo(click.style('Successful file generation', bg='black', fg='green'))
                    else:
                        click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))

                break
            if case('mh'):
                for srcFile in src:
                    if vn == '':
                        flag = m4_to_hdf_batGenNCfile(srcFile, dst, 'variable000')
                        if flag == 0:
                            click.echo(click.style('Successful file generation', bg='black', fg='green'))
                        else:
                            click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))
                    else:

                        flag = m4_to_hdf_batGenNCfile(srcFile, dst, vn)
                        if flag == 0:
                            click.echo(click.style('Successful file generation', bg='black', fg='green'))
                        else:
                            click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))

                break
            if case('gm'):
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        grbList = getGRBBatFiles(srcFile)
                        for grb in grbList:
                            (filepath, tempfilename) = os.path.split(grb)
                            (filename, extension) = os.path.splitext(tempfilename)
                            if os.path.exists(os.path.join(dst,filename)):
                                c = Grib_to_M4(grb, os.path.join(dst,filename), '')
                            else:
                                os.makedirs(os.path.join(dst,filename))
                                c = Grib_to_M4(grb, os.path.join(dst,filename), '')
                    else:
                        if os.path.exists(srcFile):

                            c = Grib_to_M4(srcFile, dst, '')
                        else:
                            print('src:%s not exist!' % srcFile)
                            continue

                if c.flag == 0:
                    click.echo(click.style('Successful file generation', bg='black', fg='green'))
                else:
                    click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))
                break

            if case('gn'):
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        grbList = getGRBBatFiles(srcFile)
                        batGrbToNCFileDeal(grbList, dst)
                    else:
                        if os.path.exists(srcFile):
                            (filepath, tempfilename) = os.path.split(srcFile)
                            (filename, extension) = os.path.splitext(tempfilename)
                            flag = grib_to_nc_batGenNCfile(srcFile, os.path.join(dst, filename + '.nc'), vn)
                        else:
                            print('src:%s not exist!' % srcFile)
                            continue

                #flag = grib_to_nc_batGenNCfile(src, dst, vn)
                if flag == 0:
                    click.echo(click.style('Successful file generation', bg='black', fg='green'))
                else:
                    click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))

                break
            if case('gh'):
                for srcFile in src:
                    if os.path.isdir(srcFile):
                        grbList = getGRBBatFiles(srcFile)
                        batGrbToHDFFileDeal(grbList, dst)
                    else:
                        if os.path.exists(srcFile):
                            (filepath, tempfilename) = os.path.split(srcFile)
                            (filename, extension) = os.path.splitext(tempfilename)
                            flag = grib_to_hdf_batGenNCfile(srcFile, os.path.join(dst, filename + '.hdf'), vn)
                        else:
                            print('src:%s not exist!' % srcFile)
                            continue


                #flag = grib_to_hdf_batGenNCfile(src, dst, vn)
                if flag == 0:
                    click.echo(click.style('Successful file generation', bg='black', fg='green'))
                else:
                    click.echo(click.style('Failure file generation', bg='black', fg='bright_red'))
                break
            if case('ng'):
                click.echo(click.style('Successful file generation', bg='black', fg='green'))
                break
            if case('hg'):
                click.echo(click.style('Successful file generation', bg='black', fg='green'))
                break
            if case('mg'):
                click.echo(click.style('Successful file generation', bg='black', fg='green'))
                break
            if case():  # default, could also just omit condition or 'if True'
                click.echo(click.style('ERROR KEY:"%s"!'%v, bg='black', fg='bright_red'))
                break


    else:
        #click.echo('no dir src,%s'%src)
        click.echo(click.style('src:%s not exist!'%src, bg='black', fg='bright_red'))

def modify_the_user(user):
    print(user)



def batNCToHDFFileDeal(flist,dst):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            print(file)
            print(filename + '.hdf')
            t = threading.Thread(target=nc2hdf, args=(file, os.path.join(dst, filename + '.hdf')))

            t.start()
        for t in thread_list:
            t.join()


def batHDFToNCFileDeal(flist,dst):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            print(file)
            print(filename + '.nc')
            t = threading.Thread(target=hdf2nc, args=(file, os.path.join(dst, filename + '.nc')))

            t.start()
        for t in thread_list:
            t.join()


def batGrbToNCFileDeal(flist,dst,vn):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            t = threading.Thread(target=grib_to_nc_batGenNCfile, args=(file, os.path.join(dst, filename + '.nc'), vn))

            t.start()
        for t in thread_list:
            t.join()


def batGrbToHDFFileDeal(flist,dst,vn):
    if flist:
        thread_list = []

        for file in flist:
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            t = threading.Thread(target=grib_to_hdf_batGenNCfile, args=(file, os.path.join(dst, filename + '.nc'), vn))

            t.start()
        for t in thread_list:
            t.join()





def getGRBBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.grb' or os.path.splitext(file)[1] == '.GRB' or os.path.splitext(file)[1] == '.grb2':
                flist.append(os.path.join(root, file))
    return flist








def getNCBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.nc' or os.path.splitext(file)[1] == '.NC':
                flist.append(os.path.join(root, file))
    return flist

def getHDFBatFiles(path):

    flist = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.hdf' or os.path.splitext(file)[1] == '.HDF':
                flist.append(os.path.join(root, file))
    return flist




if __name__ == '__main__':

    climain()
