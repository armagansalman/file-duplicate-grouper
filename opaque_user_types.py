from common_types import *


t_OpaqueObj = t_Any
t_ObjIter = t_Iter[t_OpaqueObj]
t_ObjSize = t_Int

t_StartIdx = t_Int
t_EndIdx = t_Int

t_FnGetObjPath = t_Callable[[t_OpaqueObj], t_Str]
t_FnGetObjSize = t_Callable[[t_OpaqueObj], t_ObjSize]
t_FnGetObjBytes = t_Callable[[t_OpaqueObj, t_StartIdx, t_EndIdx], t_Bytes]
t_FnGetKey = t_Callable[[t_OpaqueObj], t_Any]
t_FnGetValue = t_Callable[[t_OpaqueObj], t_Iter]

t_FnGetHashable = t_Callable[[t_OpaqueObj, t_Any], t_Hashable]
