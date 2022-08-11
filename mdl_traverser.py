from common_types import *
from user_types import *

import path_functions as PFuncs

# Type definitions:
#t_Iter = Iterable
#t_Path = A USER DEFINED TYPE


def discard_redundants(DIRS: t_PathIter) -> t_PathIter:
#(
    raise Exception("Unimplemented.")
    
    dir_strs = map(lambda x: x.path_str , DIRS)
    abs_dirs = map(PFuncs.get_absolute_path , dir_strs)
    
    # TODO(armagan): Sort path strings. If prev is parent of current,
    # discard current. Continue. Else, add prev to list and make current prev.
    
#)


def find_files_recursive(PATHS: t_PathIter) -> t_PathIter:
#(
    return PFuncs.get_fpaths_from_path_iter(list(PATHS))
#)


def test_1(paths: t_PathIter):
#(
    for pth in paths:
    #(
        print(str(pth))
    #)
#)


def main_1():
#(
    elms = ["abc", "asd", "aer"]

    test_1(elms)
#)


if __name__ == "__main__":
#(
    main_1()
#)
