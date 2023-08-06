
# Copyright (C) 2010-2017 - Andreas Maier
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)
from  jpype import  JArray,JDouble
from pyconrad import PyConrad, PyGrid, java_float_dtype
import numpy as np

pyconrad = PyConrad()
pyconrad.setup()

#Test extention methods to create from numpy and to convert to numpy: PointND
pyconrad.add_import('edu.stanford.rsl.conrad.geometry.shapes.simple')
java_point = pyconrad['PointND'](JArray(JDouble)([2.1,3.1]))
java_point2 = pyconrad['PointND'].from_numpy(np.array([2.1,3.1]))
java_point3 = pyconrad['PointND'].from_list([2.1,3.1])
numpy_point = java_point.as_numpy()
numpy_point2 = java_point2.as_numpy()
numpy_point3 = java_point3.as_numpy()

#Test extention methods to create from numpy and to convert to numpy: SimpleVector
pyconrad.add_import('edu.stanford.rsl.conrad.numerics')
java_vector = pyconrad['SimpleVector'](JArray(JDouble)([2.1,3.1]))
java_vector2 = pyconrad['SimpleVector'].from_numpy(np.array([2.1,3.1]))
java_vector3 = pyconrad['SimpleVector'].from_list([2.1,3.1])
numpy_vector = java_vector.as_numpy()
numpy_vector2 = java_vector2.as_numpy()
numpy_vector3 = java_vector3.as_numpy()

#Test extention methods to create from numpy and to convert to numpy: SimpleMatrix
pyconrad.add_import('edu.stanford.rsl.conrad.numerics')
java_matrix = pyconrad['SimpleMatrix'](JArray(JDouble,2)([[1.1,2.2,3.3],[4.4,5.5,6.6]]))
java_matrix2 = pyconrad['SimpleMatrix'].from_numpy(np.matrix([[1.1,2.2,3.3],[4.4,5.5,6.6]]))
java_matrix3 = pyconrad['SimpleMatrix'].from_list([[1.1,2.2,3.3],[4.4,5.5,6.6]])
numpy_matrix = java_matrix.as_numpy()
numpy_matrix2 = java_matrix2.as_numpy()
numpy_matrix3 = java_matrix3.as_numpy()

pyconrad.add_import('edu.stanford.rsl.tutorial.phantoms')
phantom = pyconrad['MickeyMouseGrid2D'](200,200)

#extension methods are added tu numeric grid, which is the parent class of Grid1D, Grid2D, Grid3D,...
pyconrad.add_import("edu.stanford.rsl.conrad.data.numeric")
java_grid3D = pyconrad["Grid3D"](100,100,100)
java_grid3D2 = pyconrad["Grid3D"].from_numpy(np.array([[[2.1,3.1],[2.2,3.2],[2.3,3.3]]]))
java_grid3D3 = pyconrad["Grid3D"].from_list([[[2.1,3.1],[2.2,3.2],[2.3,3.3]]])

np_grid3D = java_grid3D.as_numpy()
np_grid3D2 = java_grid3D2.as_numpy()
np_grid3D3 = java_grid3D3.as_numpy()

# Create PyGrid from Grid2D
pygrid1 = PyGrid.from_grid(phantom)
# use Java method
pygrid1.grid().show()
# use Python method
from scipy.misc import imshow
imshow(pygrid1)

# Create PyGrid from numpy array (must be of type pyconrad.java_float_dtype)
array = np.random.rand(4,2,3).astype(java_float_dtype)
pygrid2 = PyGrid.from_numpy(array)

# Manipulate data in using CONRAD at Position (x,y,z) = (1,2,4)
pygrid2.grid().setValue(5.0, [0,1,3])

# Print this pixel using Python indexes [z,y,x]
print("Before update: %f" % pygrid2[3,1,0])
# Python data must be synchronized with CONRAD
pygrid2.update_numpy()
print("After update: %f" % pygrid2[3,1,0])

# Manipulate pixel using python
pygrid2[1,1,1] = 3.0
# Update CONRAD data
pygrid2.update_grid()

# Print
print(pygrid2)

