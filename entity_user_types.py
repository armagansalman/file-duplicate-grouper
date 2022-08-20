from common_types import *

t_EntityRef = t_Int
t_RefIter = t_Iter[t_EntityRef]

t_FnGetPath = t_Callable[[t_EntityRef], t_Str]
