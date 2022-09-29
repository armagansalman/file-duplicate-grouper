import os
from typing import List

from common_types import *

import path_functions as PFuncs
import const_data as Tdata
import mdl_traverser as Seeker

DIRS = Tdata.DIRS
DIRS_19 = Tdata.DIRS_19[:]
DIRS_20: tuple = DIRS["dirs_20"]


get_fpaths_from_path_iter = PFuncs.get_fpaths_from_path_iter

def main_1(args):
#(
    dirs: t_List[t_Path] = [ PathData("/home/genel/Desktop/TEMP/") \
            , PathData("/home/genel/Videos/") ]
    #
    x = PathData("abc")
    
    print(type(dirs[0]))
    
    #fdatas = list(get_fpaths_from_path_iter(dirs))
    fdatas = list(Seeker.find_files_recursive(dirs))
    
    print(f"Total non-symbolic file count == {len(fdatas)}")
    
    for idx, data in enumerate(fdatas):
    #(
        pth = data.path_str
        print(f"File ({idx}) path == {pth}")
        
        sz = os.path.getsize(pth)
        print(f"File ({idx}) size == {sz/(1024**2):.2} Mb , {sz/(1024):.2} Kb , {sz} bytes.")
        print()
    #)
    exit()
#)


def main_2(args):
#(
    dirs_1 = [ "/media/genel/SAMSUNG/NOT SAMS/Personal/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Movies-Series/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ALL BOOKS-PAPERS/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ESSENTIAL BACKUP/" \
        , "/media/genel/SAMSUNG/NOT SAMS/BACKUP-HP-2022-05-06/" ]
    #
    dirs_5 = dirs_1
    dirs_5.extend( ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/"] )
    
    
    fpaths = get_fpaths_from_path_iter(dirs_5)
    
    print(f"Total non-symbolic file count == {len(fpaths)}")
    
    for idx, f in enumerate(fpaths):
    #(
        print(f"File ({idx}) path == {f}")
        
        sz = os.path.getsize(f)
        print(f"File ({idx}) size == {sz/(1024**2):.2} Mb , {sz/(1024):.2} Kb , {sz} bytes.")
        print()
    #)
    exit()
#)


def main_3(args):
#(
    dirs = list(DIRS_19[:])
    
    fpaths = get_fpaths_from_path_iter(dirs)
    
    print(f"Total non-symbolic file count == {len(fpaths)}")
    
    for idx, f in enumerate(fpaths):
    #(
        print(f"File ({idx}) path == {f}")
        
        sz = os.path.getsize(f)
        print(f"File ({idx}) size == {sz/(1024**2):.2} Mb , {sz/(1024):.2} Kb , {sz} bytes.")
        print()
    #)
    exit()
#)


def main_4(args):
#(
    dirs = args["dirs"]
    
    fpaths = get_fpaths_from_path_iter(dirs)
    
    print(f"Total non-symbolic file count == {len(fpaths)}")
    
    for idx, f in enumerate(fpaths):
    #(
        print(f"File ({idx}) path == {f}")
        
        sz = os.path.getsize(f)
        print(f"File ({idx}) size == {sz/(1024**2):.2} Mb , {sz/(1024):.2} Kb , {sz} bytes.")
        print()
    #)
    exit()
#)


if __name__ == "__main__":
#(
    args_1: dict = dict()
    main_1(args_1)
    
    #args_2: dict = dict()
    #main_2(args_2)
    
    #args_3: dict = dict()
    #main_3(args_3)
    
    #args_4: dict = {"dirs": list(DIRS_20)}
    #main_4(args_4)
    
#)

"""
dirs = [ "/media/genel/SAMSUNG/NOT SAMS/Personal/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Movies-Series/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ALL BOOKS-PAPERS/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ESSENTIAL BACKUP/" \
        , "/media/genel/SAMSUNG/NOT SAMS/BACKUP-HP-2022-05-06/" ]
    #
    dirs_5 = dirs
    dirs_5.extend( ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/"] )
    
    args_5 = {"dirs": dirs_5}
    main_5(args_5)
"""
