# All types have to start with t_

from typing import Iterable as t_Iter
from typing import List as t_List
from typing import Set as t_Set
from typing import Tuple as t_Tuple
from typing import Dict as t_Dict
from typing import Callable as t_Callable
from typing import Any as t_Any
from typing import Hashable as t_Hashable
from typing import Optional as t_Optional

t_Str = str
t_Int = int
t_Bytes = bytes

t_HashableIter = t_Iter[t_Hashable]
