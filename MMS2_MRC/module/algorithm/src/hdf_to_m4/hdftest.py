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
            print("$$Ŀ¼$$��",fileName)
            getAllDir(fileAbsPath)
       else:
          print("**��ͨ�ļ���**",fileName)
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





































#__author:"��**"
#date: 2018/10/21 0021
#function:
# ������ȱ���Ŀ¼�㼶�ṹ
import os
def getAllDirDP(path):
 stack = []
 # ѹջ����,�൱��ͼ�е�Aѹ��
 stack.append(path)
 # ����ջ����ջΪ�յ�ʱ�����ѭ��
 while len(stack) != 0:
  #��ջ��ȡ���ݣ��൱��ȡ��A��ȡ��A��ͬʱ��BCѹ��
  dirPath = stack.pop()
  firstList = os.listdir(dirPath)
  #�жϣ���Ŀ¼ѹջ���Ѹ�Ŀ¼��ַѹջ������Ŀ¼������ͨ�ļ�����ӡ
  for filename in firstList:
   fileAbsPath=os.path.join(dirPath,filename)
   if os.path.isdir(fileAbsPath):
    #��Ŀ¼��ѹջ
    print("Ŀ¼��",filename)
    stack.append(fileAbsPath)
   else:
    #����ͨ�ļ��ʹ�ӡ���ɣ���ѹջ
    print("��ͨ�ļ���",filename)
#getAllDirDP(r'E:\[AAA]��ǧ)ȫջѧϰpython\18-10-21\day7\temp\dir')














#__author:"��**"
#date: 2018/10/21 0021
#function:
# �����������ģ��
# ���ö�����ģ������������
import os
import collections
def getAllDirIT(path):
 queue=collections.deque()
 #����
 queue.append(path)
 #ѭ����������Ϊ�գ�ֹͣѭ��
 while len(queue) != 0:
  #�������� �����൱���ҵ�AԪ�صľ���·��
  dirPath = queue.popleft()
  # �ҳ���Ŀ¼�µ����е���Ŀ¼��Ϣ�������Ǹ�Ŀ¼�µ��ļ���Ϣ
  dirList = os.listdir(dirPath)
  #�������ļ����µ�������Ϣ
  for filename in dirList:
   #����·��
   dirAbsPath = os.path.join(dirPath,filename)
   # �жϣ������Ŀ¼dir��Ӳ������������dir��ӡ������
   if os.path.isdir(dirAbsPath):
    print("Ŀ¼��"+filename)
    queue.append(dirAbsPath)
   else:
    print("��ͨ�ļ���"+filename)
# �����ĵ���
#getAllDirIT(r'E:\[AAA]��ǧ)ȫջѧϰpython\18-10-21\day7\temp\dir')







#__author:"��*��"
#date: 2018/10/21 0021
#function:
import os
def getAllDir(path):
 fileList = os.listdir(path)
 print(fileList)
 for fileName in fileList:
  fileAbsPath = os.path.join(path,fileName)
  if os.path.isdir(fileAbsPath):
   print("$$Ŀ¼$$��",fileName)
   getAllDir(fileAbsPath)
  else:
   print("**��ͨ�ļ���**",fileName)
 # print(fileList)
 pass
#getAllDir("G:\\")
