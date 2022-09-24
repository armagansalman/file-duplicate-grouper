import os

from common_types import *
from entity_user_types import *

import path_functions as PFuncs

from temporary_dir_data import DIRS


def get_fpaths_recursively(ref: t_EntityRef, \
                            get_path_from_entity: t_FnGetEntityPath):
#(
    path = get_path_from_entity(ref)
    
    return PFuncs.get_fpaths_recursively(path)
#)


def get_fpaths_from_path_iter(ref_iter: t_RefIter, \
                                get_path_from_entity: t_FnGetEntityPath):
#(
    refs_to_paths = []
    
    for ref in ref_iter:
    #(
        found_paths = get_fpaths_recursively(ref, get_path_from_entity)
        
        refs_to_paths.append( (ref, found_paths) )
        
        #TODO(armagan): ???Use yield instead of return???
    #)
    
    return refs_to_paths
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


def main_2(args):
#(
    data = ["./", \
            "/home/genel/Videos/", \
            "/home/genel/Music/" ]
    #
    
    def fn_get_path(ref: t_EntityRef):
    #(
        return data[ref]
    #)
    
    
    refs = [idx for idx in range(len(data))]
    
    rec_paths = get_fpaths_from_path_iter(refs, fn_get_path)
    
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
    data = args["dirs"]
    
    def get_dir_path(ref: t_EntityRef):
    #(
        return data[ref]
    #)
    
    
    def usr_get_entity_size(ref: t_EntityRef, get_path: t_Callable) -> t_EntitySize:
    #(
        #path = data_bank # data_bank is the path string for main_3.
        path = get_path(ref)
        print(path)
        print()
        return os.path.getsize(path) #TODO(armagan): Error handling.
    #)
    
    data_bank = data
    refs = [idx for idx in range(len(data))]
    
    recursive_paths = get_fpaths_from_path_iter(refs, get_dir_path)
    
    # TODO(armagan): Combine recursive path results. Then use it for get_recursive_path.
    
    found_paths = []
    
    for dirref, paths in recursive_paths:
    #(
        found_paths.extend(paths)
    #)
    
    
    def get_recursive_path(ref: t_EntityRef):
    #(
        return found_paths[ref]
    #)
    
    
    idx = 0
    
    for pref, elm in enumerate(found_paths):
    #(
        print("-------------")
        print(f"Ref:{pref}")
        
        #(
        print(f"File ({idx}) path == {elm}")
        
        sz = usr_get_entity_size(pref, get_recursive_path) # -1 because ref is 
        # unimportant for this case.
        
        print(f"File ({idx}) size == {sz/(1024**2):.3} Mb , {sz/(1024):.3} Kb , {sz} bytes.")
        print()
        
        idx += 1
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
