from common_types import *
from opaque_user_types import *

import opaque_path_functions as OpPthFn

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
    
    selected_dirs = obj_iter
    dir_filelist_tuples = OpPthFn.get_fpaths_from_path_iter(selected_dirs, get_path_from_obj)
    
    potential_fpaths = OpPthFn.combine_file_paths_from_tuples(dir_filelist_tuples)
    
    fpaths = filter(OpPthFn.is_file, potential_fpaths)
    
    return get_multi_obj_sizes(fpaths, OpPthFn.get_file_size)
#)


def group_objs_by_fsize(obj_iter: t_ObjIter, get_obj_size: t_FnGetObjSize):
#(
    size_to_objs = dict()
    
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


def 



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

#

if __name__ == "__main__":
#(
    #main_1(dict())
    
    #main_2(dict())
    
    #main_3(dict())
    
    main_4(dict())
    
#)

