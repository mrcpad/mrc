# -*- coding: gbk -*-


from netCDF4 import Dataset

dd = {"aa":[1,2,3],"bb":[1,2,3],"cc":[1,2,3]}
for k in dd.keys():
    dd[k].append(4)

print(dd)
a = list([1,2,3])
print(a[1])



#print(hdf.groups['m4'].groups['data'].groups['temperature'].groups)
#print(hdf.groups['m4'].variables)
def getAllgroups(hdf):
    grs = hdf.groups
    for g in grs:
        gs = hdf.groups[g]
        if not gs.variables:
            getAllgroups(gs)
        else:
            return gs.variables

#print(getAllgroups(hdf))

'''def getAllgroups(hdf):

     grs = hdf.groups

     for g in grs:

         gs = hdf.groups[g]

       fileAbsPath = os.path.join(path,fileName)
       if os.path.isdir(fileAbsPath):
            print("$$目录$$：",fileName)
            getAllDir(fileAbsPath)
       else:
          print("**普通文件！**",fileName)
 # print(fileList)
 pass'''
#getAllgroups("G:\\")
















def factorial(n):
    if n == 0 or n == 1: return 1
    else: return (n * factorial(n - 1))


#print(hdf.groups.keys())
#print(list(hdf.groups['m4'].variables.keys())[:])
#print(hdf.groups['m4'].vltypes)

#print(hdf.ncattrs())
#print(hdf.getncattr('year'))

    #print(hdf.getncattr(ncattr))



'''print(hdf.groups['m4'].variables['time'].ncattrs())
print(hdf.groups['m4'].ncattrs())

#print(hdf.groups['m4'].variables['time'].dtype.find('str'))


#print(hdf.groups['m4'].variables['lvtemperature'].get_dims())
print(hdf.groups['m4'].variables['lvtemperature'].dimensions)
print(hdf.groups['m4'].variables['lvtemperature'].shape)
a = hdf.groups['m4'].variables['lvtemperature'].dimensions
b = hdf.groups['m4'].variables['lvtemperature'].shape
d = dict(zip(a,b))
print(d)
print(type(a))
for s in zip(a,b):
    print(s)



import os
import datetime

#print(list(hdf.groups['m4'].dimensions.keys())[:])
#print(hdf.groups['m4'].variables['lvtemperature'].dimensions)
#print(hdf.ncattrs())




for g in hdf.groups:
    pass
    #print(g)
#print(nc.dimensions.keys())
#print(nc.variables.keys())
#print(nc.variables['lvtemperature'])
#print(nc.variables['lvtemperature'].dimensions)
#print(nc.variables['lvtemperature'].shape)

tdate1 = datetime.datetime.strptime('2015-12-15 08', '%Y-%m-%d %H')
tdate2 = datetime.datetime.strptime('2015-12-20 20', '%Y-%m-%d %H')
#print((tdate2 - tdate1).days*24)'''





































#__author:"吉**"
#date: 2018/10/21 0021
#function:
# 深度优先遍历目录层级结构
import os
def getAllDirDP(path):
 stack = []
 # 压栈操作,相当于图中的A压入
 stack.append(path)
 # 处理栈，当栈为空的时候结束循环
 while len(stack) != 0:
  #从栈里取数据，相当于取出A，取出A的同时把BC压入
  dirPath = stack.pop()
  firstList = os.listdir(dirPath)
  #判断：是目录压栈，把该目录地址压栈，不是目录即是普通文件，打印
  for filename in firstList:
   fileAbsPath=os.path.join(dirPath,filename)
   if os.path.isdir(fileAbsPath):
    #是目录就压栈
    print("目录：",filename)
    stack.append(fileAbsPath)
   else:
    #是普通文件就打印即可，不压栈
    print("普通文件：",filename)
#getAllDirDP(r'E:\[AAA]（千)全栈学习python\18-10-21\day7\temp\dir')














#__author:"吉**"
#date: 2018/10/21 0021
#function:
# 广度优先搜索模拟
# 利用队列来模拟广度优先搜索
import os
import collections
def getAllDirIT(path):
 queue=collections.deque()
 #进队
 queue.append(path)
 #循环，当队列为空，停止循环
 while len(queue) != 0:
  #出队数据 这里相当于找到A元素的绝对路径
  dirPath = queue.popleft()
  # 找出跟目录下的所有的子目录信息，或者是跟目录下的文件信息
  dirList = os.listdir(dirPath)
  #遍历该文件夹下的其他信息
  for filename in dirList:
   #绝对路径
   dirAbsPath = os.path.join(dirPath,filename)
   # 判断：如果是目录dir入队操作，如果不是dir打印出即可
   if os.path.isdir(dirAbsPath):
    print("目录："+filename)
    queue.append(dirAbsPath)
   else:
    print("普通文件："+filename)
# 函数的调用
#getAllDirIT(r'E:\[AAA]（千)全栈学习python\18-10-21\day7\temp\dir')







#__author:"吉*佳"
#date: 2018/10/21 0021
#function:
import os
def getAllDir(path):
 fileList = os.listdir(path)
 print(fileList)
 for fileName in fileList:
  fileAbsPath = os.path.join(path,fileName)
  if os.path.isdir(fileAbsPath):
   print("$$目录$$：",fileName)
   getAllDir(fileAbsPath)
  else:
   print("**普通文件！**",fileName)
 # print(fileList)
 pass
#getAllDir("G:\\")
