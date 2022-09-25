import os

import common_types as CT
#from user_types import *


def get_absolute_path(path: CT.t_Str):
#(
    return os.path.abspath(path)
#)


def is_file(path: CT.t_Str):
#(
    return os.path.isfile(path)
#)


def ignore_redundant_subdirs(dirs: CT.t_Iter[CT.t_Str]):
    """ If a dir D_1 is a descendant of a dir D_2, don't include D_1 as
        it will be included with recursive search of D_2. 
        WARNING: If a given path is a file, it will also be ignored.
    """
#(
    abs_paths = list(map(get_absolute_path, filter(os.path.isdir, dirs)))
    
    abs_paths.sort()
    
    prev = abs_paths[0]
    
    essential_dirs = []
    
    for ix in range(1, len(abs_paths)):
    #(
        current = abs_paths[ix]
        
        if current.startswith(prev): # Current is a descendant, ignore.
        #(
            continue
        #)
        else:
        #(
            essential_dirs.append(prev)
            prev = current
        #)
    #)
    essential_dirs.append(prev)
    
    return essential_dirs
#)


def get_fpaths_recursively(PATH: CT.t_Str):
#(
    rec_files: list = []
    # TODO(armaganslmn): ??? Error handling.
    #ap = os.path.abspath(PATH)
    
    ap = PATH
    if os.path.isfile(ap):
    #(
        rec_files.append(ap)
        return rec_files
    #)
    
    elif os.path.isdir(ap):
    #(
        for root, dirs, files in os.walk(ap):
        #(
            for name in files:
            #(
                p = os.path.join(root, name)
                rec_files.append(p) #os.path.abspath(p)
            #)
        #)
    #)
    
    else: # Link or something else. Ignore them.
    #(
        pass
    #)
    
    return rec_files
#)


def get_fpaths_from_path_iter(paths_iter: CT.t_List[CT.t_Str]):
#(
    if type(paths_iter[0]) != CT.t_Str or type(paths_iter[-1]) != CT.t_Str:
    #(
        raise Exception("A list of CT.t_Str must be given.")
    #)
    
    file_paths: list = []
    
    # Below line removed. Selection belongs to mdl_Traverser module.
    # unq_paths = set(map(lambda x: x.path_str , paths_iter))
    
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    
    #path_strings = map(lambda x: x.path_str , paths_iter)
    path_strings = paths_iter
    
    for string in path_strings:
    #(
        file_paths.extend( get_fpaths_recursively(string) )
    #)
    
    return file_paths
#)


def test_ignore_redundant_subdirs_1():
#(
    dirs = ["/home/genel/Desktop/TEMP/", "!abc" \
            ,"/home/genel/Desktop/" \
            ,"/home/genel/Desktop/TEMP/git-local/" \
            ,"/home/genel/Documents/" \
            ,"/home/genel/Documents/Programs/" \
            ,"/home/genel/Documents/Programs/eclipse/" ]
    #
    # WARNING: os.path.abspath removes leading / from path. Important for 
    # path string comparisons.
    essential_dirs = ["/home/genel/Desktop", "/home/genel/Documents"]
    
    calc_essential_dirs = ignore_redundant_subdirs(dirs)
    
    s1 = set(essential_dirs)
    s2 = set(calc_essential_dirs)
    
    assert(s1.difference(s2) == set())
    
    print(f"Passed | test_ignore_redundant_subdirs_1 | {__name__}")
#)


def main_1(args):
#(
    pass
#)


if __name__ == "__main__":
#(
    #main_1(dict())
    
    test_ignore_redundant_subdirs_1()
#)
