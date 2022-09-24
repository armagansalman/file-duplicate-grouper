from common_types import *

t_EntityRef = t_Int
t_EntitySize = t_Int
t_RefIter = t_Iter[t_EntityRef]

t_UserDataBank = t_Any

t_FnGetEntityPath = t_Callable[[t_UserDataBank, t_EntityRef], t_Str]
t_FnGetEntitySize = t_Callable[[t_UserDataBank, t_EntityRef], t_EntitySize]
