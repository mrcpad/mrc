# -*- coding: utf-8 -*-


from netCDF4 import Dataset
import os
from functools import reduce





def showHDFInfo(path):
    if os.path.exists(path):
        hdf = Dataset(path, 'r',)
        attrdict = {}

        if hdf.groups:

            print('The HDF file contains {count} groups information:'.format(count=str(len(hdf.groups.keys()))))
            for gnum,g in enumerate(hdf.groups):
                VerifyData(hdf.groups[g], path)
                print('group({gnum}):groupName:({gname})'.format(gnum=str(gnum + 1),gname=str(g)))
                print('The HDF file all  variables :{vlist}'.format(vlist=str(list(hdf.groups[g].variables.keys()))))
                print('The HDF file contains {count} variables information:'.format(count=str(len(hdf.groups[g].variables.keys()))))
                for num, var in enumerate(hdf.groups[g].variables.keys()):
                    vhdf = hdf.groups[g].variables[var]
                    for d in vhdf.ncattrs():
                        attrdict[d] = vhdf.getncattr(d)
                    s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                    print(s.format(num=str(num + 1), vname=vhdf.name, vtype=str(vhdf.dtype), vdims=str(vhdf.dimensions),
                                   vshape=str(vhdf.shape), vattrs=str(attrdict)))
                attrdict = {}


        else:


            print('The HDF file all  variables :{vlist}'.format(vlist=str(list(hdf.variables.keys()))))
            print('The HDF file contains {count} variables information:'.format(count=str(len(hdf.variables.keys()))))
            VerifyData(hdf, path)
            for num,var in enumerate(hdf.variables.keys()):

                vhdf = hdf.variables[var]
                for d in vhdf.ncattrs():
                    attrdict[d] = vhdf.getncattr(d)
                s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                print(s.format(num=str(num + 1),vname=vhdf.name,vtype=str(vhdf.dtype),vdims=str(vhdf.dimensions),vshape=str(vhdf.shape),vattrs=str(attrdict)))
                attrdict = {}


def showOneVarHDFInfo(path,varName):
    if os.path.exists(path):
        hdf = Dataset(path, 'r', )
        attrdict = {}

        if hdf.groups:
            for gnum, g in enumerate(hdf.groups):
                VerifyData(hdf.groups[g], path)
                print('group({gnum}):groupName:({gname})'.format(gnum=str(gnum + 1), gname=str(g)))
                vnc = hdf.groups[g].variables.get(varName,'')
                if vnc:
                    for d in vnc.ncattrs():
                        attrdict[d] = vnc.getncattr(d)
                    s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                    print(s.format(num=str(0), vname=vnc.name, vtype=str(vnc.dtype), vdims=str(vnc.dimensions),
                                   vshape=str(vnc.shape), vattrs=str(attrdict)))
                else:
                    print('The Variable "{varName}" does not exist！chage again?'.format(varName=varName))


        else:

            print('The HDF file contains {count} variables information:'.format(count=str(len(hdf.variables.keys()))))
            VerifyData(hdf, path)


            vhdf = hdf.variables.get(varName,'')
            if vhdf:
                for d in vhdf.ncattrs():
                    attrdict[d] = vhdf.getncattr(d)
                s = 'VariableInfo({num}):\n\t\t|\n\t\t--VariableName:\n\n\t\t\t----{vname}\n\t\t|\n\t\t--VariableDtype:\n\n\t\t\t----{vtype}\n\t\t|\n\t\t--VariableDimensions:\n\n\t\t\t----{vdims}\n\t\t|\n\t\t--VariableShape:\n\n\t\t\t----{vshape}\n\t\t|\n\t\t--VariableAttrs:\n\n\t\t\t----{vattrs}'

                print(s.format(num=str(0), vname=vhdf.name, vtype=str(vhdf.dtype), vdims=str(vhdf.dimensions),
                               vshape=str(vhdf.shape), vattrs=str(attrdict)))

            else:
                print('The Variable "{varName}" does not exist！change again?'.format(varName=varName))


def VerifyData(hdf,path):
    LatGridNumber = 0
    LatGridNumber = 0

    lone = hdf.get_variables_by_attributes(axis='X')
    if lone:
        long = lone[0][:]
        StartLon = long[0]
        EndLon = long[-1]
        LonGridNumber = len(long)
        LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

    else:
        if hdf.variables.get('longitude'):
            long = hdf.variables.get('longitude')[:]
            StartLon = long[0]
            EndLon = long[-1]
            LonGridNumber = len(long)
            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)
            # print(np.round(LonGridLength, decimals=2))
        elif hdf.variables.get('lon'):
            long = hdf.variables.get('lon')[:]
            StartLon = long[0]
            EndLon = long[-1]
            LonGridNumber = len(long)
            LonGridLength = (EndLon - StartLon) / (LonGridNumber - 1)

    late = hdf.get_variables_by_attributes(axis='Y')
    if late:
        lat = late[0][:]
        StartLat = lat[0]
        EndLat = lat[-1]
        LatGridNumber = len(lat)
        LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
    else:
        if hdf.variables.get('latitude'):
            lat = hdf.variables.get('latitude')[:]
            StartLat = lat[0]
            EndLat = lat[-1]
            LatGridNumber = len(lat)
            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
        elif hdf.variables.get('lat'):
            lat = hdf.variables.get('lat')[:]
            StartLat = lat[0]
            EndLat = lat[-1]
            LatGridNumber = len(lat)
            LatGridLength = (EndLat - StartLat) / (LatGridNumber - 1)
        else:
            LatGridNumber = 0
            LonGridNumber = 0


    for var in hdf.variables.keys():
        if len(hdf.variables[var].dimensions) >= 2:
            NcCount = reduce(lambda x,y:x*y,hdf.variables[var].shape)
            print('Verify the integrity of HDF data:(file={f})'.format(f=path))
            print('Check and Verify the Variable:(name={v})'.format(v=str(var)))
            print('Verify the integrity of HDF data:')
            print(hdf.variables[var].dimensions)
            print(hdf.variables[var].shape)
            if LatGridNumber == 0 and LonGridNumber == 0:
                if len(hdf.variables[var].dimensions) == 4:
                    print('LatGridNumber = {lat}, LonGridNumber = {lon}'.format(lat=str(hdf.variables[var].shape[2]), lon=str(hdf.variables[var].shape[3])))
            print('Total data :{tot}'.format(tot=str(len(hdf.variables[var][:].reshape(-1,1)))))

            if NcCount == len(hdf.variables[var][:].reshape(-1,1)):
                print('Verify HDF data successfully')

            else:
                print('Failed to verify HDF data')


if __name__ == '__main__':

    #showOneVarHDFInfo('./1.hdf', '')
    showHDFInfo('/home/trywangdao/mrcpysrc/m4/log/ER123.nc')




