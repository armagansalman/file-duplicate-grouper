import os

from common_types import *
from user_types import *

def get_absolute_path(path):
#(
    return os.path.abspath(path)
#)

def get_fpaths_recursively(PATH: t_Str):
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


def get_fpaths_from_path_iter(paths_iter: t_List[t_Path]):
#(
    if type(paths_iter[0]) != t_Path or type(paths_iter[-1]) != t_Path:
    #(
        raise Exception("A list of t_Path must be given.")
    #)
    
    file_paths: list = []
    
    # Below line removed. Selection belongs to mdl_Traverser module.
    # unq_paths = set(map(lambda x: x.path_str , paths_iter))
    
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    
    path_strings = map(lambda x: x.path_str , paths_iter)
    
    for string in path_strings:
    #(
        file_paths.extend( get_fpaths_recursively(string) )
    #)
    
    return map(lambda x: PathData(x) , file_paths)
#)

