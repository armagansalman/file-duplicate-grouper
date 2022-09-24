from dataclasses import dataclass

from common_types import *

@dataclass
class PathData:
#(
    path_str: t_Str
#)

# TODO(armagan): Find out how to use PathData as a type. Using t_Str for now.
t_Path = PathData
t_PathIter = t_Iter[t_Path]
