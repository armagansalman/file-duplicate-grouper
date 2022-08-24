from common_types import *
import common_types as CT
from opaque_user_types import *
import opaque_user_types as OT

import opaque_path_functions as OpPthFn

import util as UTIL


def get_multi_obj_sizes(obj_iter: t_ObjIter, get_obj_size: t_FnGetObjSize):
#(
    obj_sizes = []
    
    for obj in obj_iter:
    #(
        sz = get_obj_size(obj)
        
        obj_sizes.append( (obj, sz) )
    #)
    
    return obj_sizes
#)


def get_fsizes_from_given_dirs(obj_iter: t_ObjIter, get_path_from_obj: t_FnGetObjPath):
#(
    #selected_dirs = OpPthFn.ignore_redundant_subdirs(obj_iter, get_path_from_obj)
    
    fpaths = OpPthFn.collect_all_file_paths(obj_iter, get_path_from_obj)
    
    return get_multi_obj_sizes(fpaths, OpPthFn.get_local_file_size)
#)


def group_objs_by_fsize(obj_iter: t_ObjIter, get_obj_size: t_FnGetObjSize):
#(
    size_to_objs: CT.t_Dict[OT.t_ObjSize, CT.t_Set[OT.t_OpaqueObj]] = dict()
    
    for obj in obj_iter:
    #(
        sz = get_obj_size(obj)
        
        same_sized = size_to_objs.get(sz, None)
        
        if same_sized == None:
        #(
            new_size_set = set()
            new_size_set.add(obj)
            
            size_to_objs[sz] = new_size_set
        #)
        else:
        #(
            same_sized.add(obj)
        #)
    #)
    
    return size_to_objs
    
#)


def get_local_file_bytes(obj: OT.t_OpaqueObj, get_file_path: OT.t_FnGetObjPath, \
            start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
#(
    path_str = get_file_path(obj)
    
    read_bytes = UTIL.read_local_file_bytes(path_str, start_idx, end_idx) 
    # Includes end_idx byte.
    
    return read_bytes # Returns b'' on error.
#)


def get_bytes(obj: OT.t_OpaqueObj, get_obj_bytes: OT.t_FnGetObjBytes, \
            start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
#(
    read_bytes = get_obj_bytes(obj, start_idx, end_idx) # Includes end_idx byte.
    
    return read_bytes
#)


def get_multi_obj_bytes(obj_iter, get_obj_bytes: OT.t_FnGetObjBytes, \
                        start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
#(
    # TODO(armagan): Make this a generator for memory.
    for obj in obj_iter:
    #(
        yield ( obj, get_bytes(obj, get_obj_bytes, start_idx, end_idx) )
    #)
#)


def print_path_size_iter(paths_n_sizes):
#(
    for ix, elm in enumerate(paths_n_sizes):
    #(
        print(f"Path ({ix}): {elm[0]}")
        print(f"Size: {elm[1]} bytes, {elm[1]//1024} Kb, {elm[1]// (1024**2)} Mb")
        print()
    #)
#)


def main_1(args):
#(
    dirs = ["/home/genel", "/home/genel", "/home/genel", "/home/genel/Desktop/" \
            ,"/home/genel/Desktop/" ]
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_2(args):
#(
    dirs = ["/media/genel/Bare-Data/"]
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_3(args):
#(
    dirs = ["/media/genel/9A4277A5427784B3/"]
    # 513815 items, totalling 88,4 GiB (94.866.674.987 bytes)
    # 408255 of which are files.
    
    """
    real    9m27,050s
    user    0m23,461s
    sys     1m25,914s
    """
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_4(args):
#(
    dirs = ["/media/genel/Bare-Data/"]
    # 34734 items. 32742 files.
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    size_groups = group_objs_by_fsize(path_n_sizes, lambda x: x[1])
    
    count = 0
    for sz, multi_obj in size_groups.items():
    #(
        if len(multi_obj) < 2: # Unique item. No duplicate.
            continue
        
        print("-----------")
        print(f"Group size: {sz}")
        print("Objects: ...")
        
        for obj in multi_obj:
        #(
            count += 1
            
            print(f"Object {count}: {obj}")
        #)
        print()
    #)
    
    
    #print_path_size_iter(path_n_sizes)
#)


def main_5(args):
#(
    dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    fpaths = OpPthFn.collect_all_file_paths(dirs, lambda x: x)
    
    GAP = 1024*64
    
    start_idx = 0
    end_idx = GAP + start_idx - 1
    
    print(f"Gap:{GAP}, start_idx:{start_idx}, end_idx:{end_idx}")
    
    def read_byte_from_path(path, start, end):
    #(
        return UTIL.read_local_file_bytes(path, start, end)
    #)
    
    obj_bytes_coll = get_multi_obj_bytes(fpaths, read_byte_from_path, start_idx, end_idx)
    
    for idx, elm in enumerate(obj_bytes_coll):
    #(
        obj, data = elm
        
        print(f"----------- {idx}")
        print(obj)
        
        sz = len(data)
        
        print_len = 10
        
        if sz < print_len:
            print(sz)
        else:
            print(data[-print_len:])
        #
        print()
    #)
#)


if __name__ == "__main__":
#(
    #main_1(dict())
    
    #main_2(dict())
    
    #main_3(dict())
    
    #main_4(dict())
    
    main_5(dict())
    
#)

