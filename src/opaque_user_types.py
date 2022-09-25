from dataclasses import dataclass

from common_types import *
import common_types as CT


t_OpaqueObj = t_Any
t_ObjIter = t_Iter[t_OpaqueObj]
t_ObjSize = t_Int

t_StartIdx = t_Int
t_EndIdx = t_Int

t_Option = t_Any

t_FnGetObjPath = t_Callable[[t_OpaqueObj], t_Str]
t_FnGetObjSize = t_Callable[[t_OpaqueObj, t_Option], t_ObjSize]
t_FnGetObjBytes = t_Callable[[t_OpaqueObj, t_StartIdx, t_EndIdx], t_Bytes]
t_FnGetKey = t_Callable[[t_OpaqueObj], t_Any]
t_FnGetValue = t_Callable[[t_OpaqueObj], t_Iter]

t_KeyGroupPair = CT.t_ItemsView[ CT.t_Hashable , CT.t_Set[t_OpaqueObj] ]

t_FnOpaqueFunction = t_Callable[[t_OpaqueObj, t_Option], t_Any]
t_FnGetHashable = t_Callable[[t_OpaqueObj, t_Option], t_Hashable]
t_HashToSetDict = CT.t_Dict[CT.t_Hashable, CT.t_Set[t_OpaqueObj]]
# t_FnGrouper = t_Callable[[t_ObjIter, t_FnGetHashable, CT.t_Any], ):


@dataclass
class FuncParamPair:
#(
    function: t_FnOpaqueFunction
    opt_param: CT.t_Any
#)


@dataclass
class FnHashableParamPair:
#(
    function: t_FnGetHashable
    opt_param: CT.t_Any
#)
