import os

from common_types import *
from opaque_user_types import *
import opaque_user_types as OT

import path_functions as PFuncs

from temporary_dir_data import DIRS


def get_absolute_path(path: t_Str):
#(
    return PFuncs.get_absolute_path(path)
#)


def is_file(path: t_Str):
#(
    return os.path.isfile(path)
#)


def get_local_file_size(path: t_Str):
#(
    return os.path.getsize(path)
#)


def ignore_redundant_subdirs(obj_iter: t_ObjIter, \
                                get_path_from_obj: t_FnGetObjPath):
#(
    paths = map(get_path_from_obj, obj_iter)
    
    return PFuncs.ignore_redundant_subdirs(paths)
#)


def get_fpaths_recursively(ref: t_OpaqueObj, \
                            get_path_from_obj: t_FnGetObjPath):
#(
    path = get_path_from_obj(ref)
    
    return PFuncs.get_fpaths_recursively(path)
#)


def get_fpaths_from_path_iter(obj_iter: t_ObjIter, \
                                get_path_from_obj: t_FnGetObjPath) \
                            -> t_Iter[t_Tuple[t_Any, t_List]]:
#(
    selected_dirs = ignore_redundant_subdirs(obj_iter, get_path_from_obj)
    
    objs_to_paths = []
    
    for obj in selected_dirs:
    #(
        found_paths = get_fpaths_recursively(obj, get_path_from_obj)
        
        objs_to_paths.append( (obj, found_paths) )
        
        #TODO(armagan): ???Use yield instead of return???
    #)
    
    return objs_to_paths
#)


def combine_file_paths_from_tuples(obj_pathlist_tuples):
#(
    combination = []
    
    for tpl in obj_pathlist_tuples:
    #(
        combination.extend(tpl[1])
    #)
    
    return combination
#)


def filter_for_files(paths: t_Iter[t_Str]):
#(
    return filter(os.path.isfile, paths)
#)


def collect_all_file_paths(obj_iter: t_ObjIter, \
                            get_dirpath_from_obj: t_FnGetObjPath):
#(
    dir_filelist_tuples = get_fpaths_from_path_iter(obj_iter, get_dirpath_from_obj)
    
    # OpPthFn.
    potential_fpaths = combine_file_paths_from_tuples(dir_filelist_tuples)
    
    fpaths = filter(os.path.isfile, potential_fpaths)
    
    return fpaths
#)


def main_1(args):
#(
    data = ["asd", "acv", "xzd", "efr"]
    
    def fn_get_path(obj: t_OpaqueObj):
    #(
        return obj
    #)
    
    
    get_fpaths_from_path_iter(data, fn_get_path)
    
#)


def main_2(args):
#(
    data = ["./", \
            "/home/genel/Videos/", \
            "/home/genel/Music/" ]
    #
    
    def fn_get_path(obj: t_OpaqueObj):
    #(
        return obj
    #)
    
    
    #refs = [idx for idx in range(len(data))]
    
    rec_paths = get_fpaths_from_path_iter(data, fn_get_path)
    
    for elm in rec_paths:
    #(
        print("-------------")
        print(f"Ref:{elm[0]}")
        print("Paths:")
        for p in elm[1]:
        #(
            print(p)
        #)
    #)
#)



def print_files_and_sizes(args):
#(
    LOCAL_DIRS = args["dirs"]
    
    def get_dir_path(obj: t_OpaqueObj):
    #(
        return obj
    #)
    
    
    def usr_get_entity_size(obj: t_OpaqueObj) -> t_ObjSize:
    #(
        path = obj
        
        return os.path.getsize(path) #TODO(armagan): Error handling.
    #)
    
    
    recursive_paths = get_fpaths_from_path_iter(LOCAL_DIRS, get_dir_path)
    
    # TODO(armagan): Combine recursive path results. Then use it for get_recursive_path.
    
    found_paths = []
    
    for dirref, paths in recursive_paths:
    #(
        found_paths.extend(paths)
    #)
    
    
    def get_file_path(obj: t_OpaqueObj):
    #(
        return obj
    #)
    
    
    for pthidx, elm in enumerate(found_paths):
    #(
        print("-------------")
        print(f"Ref:{pthidx}")
        
        #(
        print(f"File ({pthidx}) path == {elm}")
        
        sz = usr_get_entity_size(elm) # -1 because ref is 
        # unimportant for this case.
        
        print(f"File ({pthidx}) size == {sz/(1024**2):.3} Mb , {sz/(1024):.3} Kb , {sz} bytes.")
        print()
        #)
    #)
#)


def main_3(args):
#(
    dirs = ["./", \
            "/home/genel/Videos/", \
            "/home/genel/Music/" \
            ,"/media/genel/Bare-Data/ALL BOOKS-PAPERS/" ]
    #
    print_files_and_sizes( {"dirs": dirs} )
#)


def main_4(args):
#(
    print_files_and_sizes( {"dirs": DIRS["dirs_20"]} ) # external storage dirs.
#)


if __name__ == "__main__":
#(
    #main_1(dict())
    
    #main_2(dict())
    
    main_3(dict())
    
    #main_4(dict())
    
#)
