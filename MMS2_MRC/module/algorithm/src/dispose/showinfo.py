# -*- coding: gbk -*-


from netCDF4 import Dataset
import os

class DisposeNetCDF():

    def __init__(self,filename):
        if os.path.exists(filename):
            self.nc = Dataset(filename, 'r',)
            self.grpname = list()




    def getVariableInfo(self):
        vardict = dict()
        if self.nc.variables:
            for var in self.nc.variables.keys():
                vardict[var] = self.nc.variables.get(var,'')
            return vardict


    def getgrpAndVariableInfo(self):

        if self.nc.groups:
            grs = self.nc.groups
            grpdict = dict()
            for g in grs:
                grpdict[g] = grs[g].variables

            return grpdict
        elif self.nc.variables:
            vardict = dict()
            for var in self.nc.variables.keys():
                vardict[var] = self.nc.variables.get(var,'')
            return vardict

    def close(self):
        if self.nc:
            self.nc.close()
            self.nc = None



    def getgroupInfo(self):
        grs = self.nc.groups
        #print(grs)
        grpdict = dict()
        for g in grs:
            #print(grs[g].variables['temperature'][:])
            grpdict[g] = grs[g].variables

        return grpdict

    def getAgroupname(self, fgrs):
        global sh
        grs = fgrs.groups
        if grs:
            for g in grs:
                #print(g)
                self.grpname.append(g)
                gs = grs[g]
                if not gs.variables:
                    print(gs.name)
                    self.getAgroupname(gs)
                else:
                    print(gs.name)
                    sh = gs

            return self.grpname  # (sh.variables)



if __name__ == '__main__':
    nc = DisposeNetCDF(r'D:\PanoplyWin\15.hdf')
    print(nc.getgrpAndVariableInfo())




























