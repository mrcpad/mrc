# -*- coding: utf-8 -*-

import numpy as np
from array import array
d1 = np.empty([3,4])
d1[0,0] = float(12.1)
d1[0,1] = float(12.2)
d1[0,2] = float(12.3)
d1[0,3] = float(12.4)
#print(d1[0,0])
#print(d1[0,1])
#print(type(d1))
#print([1,2,3,4,5][1:4])

#print(["%8d" % float('122.4546')])

# flag_output_file_path=open('./d1.dat',"wb")
# float_array = array('i', [1,2,3])
# float_array.tofile(flag_output_file_path)
# float_array = array('f', [1,2,3])
# float_array.tofile(flag_output_file_path)

#float_array.tofile('./d1.dat')



###########################
# x = array('b')
# x.frombytes('test'.encode())
#
# #array('b', [116, 101, 115, 116])
# x.tobytes()
# print(x.tobytes())
# x.tobytes().decode()
# print(x.tobytes().decode())

##################################
# maxlat=90
# maxlon=180
# minlat=-90
# minlon=-180
# #calculate grid number
# nx=(maxlon-minlon)/float(0.05)
# ny=(maxlat-minlat)/float(0.05)
# print(nx)
# print(ny)
#
# #save data
# data=list(np.random.random([int(nx),int(ny)]))
# print(data)
###############################
np.float32([1.0,2,3,'3']).tofile('output.grd')
print(np.float32([1.0,2,3,'3']))