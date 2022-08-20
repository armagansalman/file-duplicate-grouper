import os

from common_types import *
from entity_user_types import *


def get_fpaths_recursively(ref: t_EntityRef, get_path_from_entity: t_FnGetPath):
#(
    path = get_path_from_entity(ref)
    print(path)
#)


def main_1(args):
#(
    data = ["asd", "acv", "xzd", "efr"]
    
    def fn_get_path(ref: t_EntityRef):
    #(
        return data[ref]
    #)
    
    
    for idx, elm in enumerate(data):
    #(
        get_fpaths_recursively(idx, fn_get_path)
    #)
    
#)


if __name__ == "__main__":
#(
    main_1(dict())
#)
