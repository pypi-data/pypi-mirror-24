
# Copyright (C) 2010-2017 - Andreas Maier 
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)

# all non-underscored names are exported unless __all__ is defined

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
from jpype import JDouble,JArray,JInt,JString,JShort,JProxy,JByte,JBoolean,JChar,JLong,JFloat,JClass,JIterator
from ._imageutils import ImageUtil
from ._pygrid import PyGrid
from ._pyconrad import PyConrad
from .constants import java_float_dtype
from .download_conrad import download_conrad, conrad_jar_dir, conrad_jar_file
