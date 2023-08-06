
# Copyright (C) 2010-2017 - Andreas Maier
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)

import jpype
import numpy as np

from ._pyconrad import PyConrad
from .constants import java_float_dtype


class PyGrid(np.ndarray):
    def __new__(cls, shape):
        return super().__new__(cls, shape=shape, dtype=java_float_dtype)

    def __init__(self, shape):
        self.__numericpackage = PyConrad.get_instance().classes.stanford.rsl.conrad.data.numeric
        if not 0 < len(shape) < 5:
            raise Exception("shape dimension of %d not supported" % len(shape))
        self.__grid = getattr(self.__numericpackage, "Grid{}D".format(len(shape)))(*reversed(shape))

        if shape[0] != 0:
            self.__dbuffer = jpype.nio.convertToDirectBuffer(self)

    @classmethod
    def from_numpy(cls, array):
        instance = array.view(cls)
        instance.__dbuffer = jpype.nio.convertToDirectBuffer(array)
        instance.__numericpackage = PyConrad.get_instance().classes.stanford.rsl.conrad.data.numeric

        if not 0 < array.ndim < 5:
            raise Exception("shape dimension of %d not supported" % array.ndim)
        instance.__grid = getattr(instance.__numericpackage, "Grid{}D".format(array.ndim))(*reversed(array.shape))

        instance.update_grid()
        assert array.dtype == java_float_dtype, "Numpy array must be Big Endian 32bit float! Use pyconrad.java_float_dtype!"
        return instance

    @classmethod
    def from_grid(cls, grid):
        size = list(reversed(grid.getSize()[:]))
        numpy = np.zeros(size, java_float_dtype)
        instance = numpy.view(cls)
        instance.__grid = grid
        instance.__dbuffer = jpype.nio.convertToDirectBuffer(instance)
        instance.update_numpy()
        return instance

    def grid(self):
        return self.__grid

    def update_numpy(self):
        shape = self.shape
        if 0 == shape[0]:
            return

        f_buffer = self.__dbuffer.asFloatBuffer()
        if 0 < len(shape) < 3:
            f_buffer.put(self.__grid.getBuffer())
        elif len(shape) is 3:
            f_buffer = self.__dbuffer.asFloatBuffer()
            for z in range(0, shape[0]):
                f_buffer.put(self.__grid.getSubGrid(z).getBuffer())  # TODO: stride == 0?
        elif len(shape) is 4:
            f_buffer = self.__dbuffer.asFloatBuffer()
            for f in range(shape[0]):
                for z in range(shape[1]):
                    f_buffer.put(self.__grid.getSubGrid(f).getSubGrid(z).getBuffer())  # TODO: stride == 0?
        else:
            raise Exception("shape dimension not supported")

    def update_grid(self):
        shape = self.shape
        if 0 == shape[0]:
            return
        f_buffer = self.__dbuffer.asFloatBuffer()
        if 0 < len(shape) < 3:
            f_buffer.get(self.__grid.getBuffer())
        elif len(shape) is 3:
            for z in range(shape[0]):
                f_buffer.get(self.__grid.getSubGrid(z).getBuffer())  # TODO: stride == 0?
        elif len(shape) is 4:
            for f in range(shape[0]):
                for z in range(shape[1]):
                    f_buffer.get(self.__grid.getSubGrid(f).getSubGrid(z).getBuffer())  # TODO: stride == 0?
        else:
            raise Exception("shape dimension not supported")



    def show_grid(self):
        if not PyConrad.get_instance().is_gui_started():
            PyConrad.get_instance().start_conrad()
        self.__grid.show()

    def save_grid_as_tiff(self, path):
        ImageUtil.save_grid_as_tiff(self.__grid, path)

    def from_tiff(self, path):
        grid = ImageUtil.grid_from_tiff(path)
        return self.__class__.from_grid(grid)

    def set_origin(self, vec):
        self.__grid.setOrigin(jpype.JArray(jpype.JDouble)(vec))

    def set_spacing(self, vec):
        self.__grid.setSpacing(jpype.JArray(jpype.JDouble)(vec))

    @staticmethod
    def java_float_dtype():
        return java_float_dtype

    def __str__(self):
        return super(PyGrid,self).__str__()