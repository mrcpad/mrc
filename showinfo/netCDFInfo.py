# -*- coding: utf-8 -*-


from netCDF4 import Dataset
import os
from functools import reduce






def showNetCDFInfo(path):
    if os.path.exists(path):
        nc = Dataset(path, 'r',)
        VerifyData(nc, path)
        attrdict = {}

        if nc.groups:

            print('The NetCDF file contains {count} groups information:'.format(count=str(len(nc.groups.keys()))))
            for gnum,g in enumerate(nc.groups):
                print('group({gnum}):groupName:({gname})'.format(gnum=str(gnum + 1),gname=str(g)))
                print('The NetCDF file all  variables :{vlist}'.format(vlist=str(list(nc.groups[g].variables.keys()))))
                print('The NetCDF file contains {count} variables information:'.format(count=str(len(nc.groups[g].variables.keys()))))
                for num, var in enumerate(nc.groups[g].variables.keys()):
                    vnc = nc.groups[g].variables[var]
                    for d in vnc.ncattrs():
                        attrdict[d] = vnc.getncattr(d)
                    s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t-VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                    print(s.format(num=str(num + 1), vname=vnc.name, vtype=str(vnc.dtype), vdims=str(vnc.dimensions),
                                   vshape=str(vnc.shape), vattrs=str(attrdict)))
                attrdict = {}



        else:


            print('The NetCDF file all  variables :{vlist}'.format(vlist=str(list(nc.variables.keys()))))
            print('The NetCDF file contains {count} variables information:'.format(count=str(len(nc.variables.keys()))))

            for num,var in enumerate(nc.variables.keys()):

                vnc = nc.variables[var]
                for d in vnc.ncattrs():
                    attrdict[d] = vnc.getncattr(d)
                s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                print(s.format(num=str(num + 1),vname=vnc.name,vtype=str(vnc.dtype),vdims=str(vnc.dimensions),vshape=str(vnc.shape),vattrs=str(attrdict)))
                attrdict = {}


def showOneVarNetCDFInfo(path,varName):
    if os.path.exists(path):
        nc = Dataset(path, 'r',)
        VerifyData(nc, path)


        attrdict = {}

        if nc.groups:
            for gnum, g in enumerate(nc.groups):
                print('group({gnum}):groupName:({gname})'.format(gnum=str(gnum + 1), gname=str(g)))
                vnc = nc.groups[g].variables.get(varName,'')
                if vnc:
                    for d in vnc.ncattrs():
                        attrdict[d] = vnc.getncattr(d)
                    s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                    print(s.format(num=str(0), vname=vnc.name, vtype=str(vnc.dtype), vdims=str(vnc.dimensions),
                                   vshape=str(vnc.shape), vattrs=str(attrdict)))
                else:
                    print('The Variable "{varName}" does not exist！change again?'.format(varName=varName))


        else:

            print('The NetCDF file contains {count} variables information:'.format(count=str(len(nc.variables.keys()))))



            vnc = nc.variables.get(varName,'')
            if vnc:
                for d in vnc.ncattrs():
                    attrdict[d] = vnc.getncattr(d)
                s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                print(s.format(num=str(0), vname=vnc.name, vtype=str(vnc.dtype), vdims=str(vnc.dimensions),
                               vshape=str(vnc.shape), vattrs=str(attrdict)))

            else:
                print('The Variable "{varName}" does not exist！chage again?'.format(varName=varName))



def VerifyData(nc,path):
    LatGridNumber = 0
    LatGridNumber = 0

    lone = nc.get_variables_by_attributes(axis='X')
    if lone:
        long = lone[0][:]
        StartLon = long[0]
        EndLon = long[-1]
        LonGridNumber = len(long)
        LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

    else:
        if nc.variables.get('longitude'):
            long = nc.variables.get('longitude')[:]
            StartLon = long[0]
            EndLon = long[-1]
            LonGridNumber = len(long)
            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
            # print(np.round(LonGridLength, decimals=2))
        elif nc.variables.get('lon'):
            long = nc.variables.get('lon')[:]
            StartLon = long[0]
            EndLon = long[-1]
            LonGridNumber = len(long)
            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

    late = nc.get_variables_by_attributes(axis='Y')
    if late:
        lat = late[0][:]
        StartLat = lat[0]
        EndLat = lat[-1]
        LatGridNumber = len(lat)
        LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
    else:
        if nc.variables.get('latitude'):
            lat = nc.variables.get('latitude')[:]
            StartLat = lat[0]
            EndLat = lat[-1]
            LatGridNumber = len(lat)
            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
        elif nc.variables.get('lat'):
            lat = nc.variables.get('lat')[:]
            StartLat = lat[0]
            EndLat = lat[-1]
            LatGridNumber = len(lat)
            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
        else:
            LatGridNumber = 0
            LonGridNumber = 0


    for var in nc.variables.keys():
        if len(nc.variables[var].dimensions) >= 2:
            NcCount = reduce(lambda x,y:x*y,nc.variables[var].shape)
            print('Verify the integrity of NetCDF data:(file={f})'.format(f=path))
            print('Check and Verify the Variable:(name={v})'.format(v=str(var)))
            print('Verify the integrity of NetCDF data:')
            print(nc.variables[var].dimensions)
            print(nc.variables[var].shape)
            if LatGridNumber == 0 and LonGridNumber == 0:
                if len(nc.variables[var].dimensions) == 4:
                    print('LatGridNumber = {lat}, LonGridNumber = {lon}'.format(lat=str(LatGridNumber), lon=str(LonGridNumber)))
            print('Total data :{tot}'.format(tot=str(len(nc.variables[var][:].reshape(-1,1)))))

            if NcCount == len(nc.variables[var][:].reshape(-1,1)):
                print('Verify NetCDF data successfully')

            else:
                print('Failed to verify NetCDF data')


if __name__ == '__main__':

    showOneVarNetCDFInfo('/home/trywangdao/mrcpysrc/m4/log/ER123.nc', 'variable000')
    #showNetCDFInfo('/home/trywangdao/mrcpysrc/m4/log/ER123.nc')




