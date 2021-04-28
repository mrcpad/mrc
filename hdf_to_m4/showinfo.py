# -*- coding: gbk -*-


from netCDF4 import Dataset


hdf = Dataset('./elementM4_t6.hdf', 'r',)

#print(hdf.groups['m4'].groups['data'].groups['temperature'])
#print(hdf.groups['m4'].path)
import copy

def getAgroupinfo(fgrs):

    global sh
    grs = fgrs.groups
    if grs:
        for g in grs:
            print(g)
            gs = grs[g]
            if not gs.variables:
                getAgroupinfo(gs)
            else:
                #print(gs)
                sh = gs

        return sh#(sh.variables)
    return sh

print(getAgroupinfo(hdf.groups['m4']))

#print(hdf.groups['m4'].groups['data'].groups['temperature'])











def getAllgroups(hdf):
    listgrps = list()
    grpname = list()
    global sh
    grs = hdf.groups
    for g in grs:
        grpname.append(g)
        gs = hdf.groups[g]
        if not gs.variables:
            getAllgroups(gs)
        else:
            #print(gs)
            sh = gs
        listgrps.append(sh)

    print(grpname)
    return listgrps#(sh.variables)

#ds = getAllgroups(hdf)
#print(ds)

def globalAttrVal(dataset):#获取全局属性
    av = dict()

    if dataset:
        for attr in dataset.ncattrs():
            av[attr] = dataset.getncattr(attr)
            # print(hdf.getncattr(attr))
    else:
        print('ERROR dataset')
    return av

#print(globalAttrVal(hdf))


def getDimensions(dataset):#获取维度信息
    dim = dict()
    if dataset:
       dimkeys = dataset.dimensions.keys()
       if dimkeys:
           for dk in dimkeys:
               dim[dk] = dataset.dimensions[dk].size
    else:
        print('error')
    return dim

#print(getDimensions(ds))

def getVariablesInfo(dataset):
    vin = dict()
    varattrsdict = dict()
    if dataset:
        varkeys = dataset.variables.keys()
        if varkeys:
            for vk in varkeys:
                dim = dataset.variables[vk].dimensions
                vshape = dataset.variables[vk].shape
                dsdict = dict(zip(dim, vshape))
                vin[vk] = [dataset.variables[vk].dtype, dsdict]
                varattrs = dataset.variables[vk].ncattrs()
                if varattrs:
                    for vt in varattrs:
                        varattrsdict[vt] = dataset.variables[vk].getncattr(vt)
                        vin[vk].append(varattrsdict)
                        #print(varattrsdict)
                #print(dataset.variables[vk].dtype)
                #vin[vk].append(dataset.variables[vk].dtype)
        #print(vin)
#getVariablesInfo(ds)
#.ncattrs()  dtype  dimensions   getncattr

