from common_types import *


t_OpaqueObj = t_Any
t_ObjIter = t_Iter[t_OpaqueObj]
t_ObjSize = t_Int


t_FnGetObjPath = t_Callable[[t_OpaqueObj], t_Str]
t_FnGetObjSize = t_Callable[[t_OpaqueObj], t_ObjSize]
