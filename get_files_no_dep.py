import os
from typing import List

import temporary_dir_data as Tdata


DIRS = Tdata.DIRS
DIRS_19 = Tdata.DIRS_19[:]
DIRS_20: tuple = DIRS["dirs_20"]


def get_fpaths_recursively(PATH: str):
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


def get_fpaths_from_path_iter(paths_iter: List[str]):
#(
    if type(paths_iter) != list:
        raise Exception("A list of str paths must be given.")
    
    file_paths: list = []
    unq_paths = set(paths_iter)
    
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    
    for path in unq_paths:
    #(
        file_paths.extend( get_fpaths_recursively(path) )
    #)
    
    return file_paths
#)


def main_1(args):
#(
    dirs = [ "/home/genel/Desktop/TEMP/" \
            , "/home/genel/Videos/"]
    #
    
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
    #args_1: dict = dict()
    #main_1(args_1)
    
    #args_2: dict = dict()
    #main_2(args_2)
    
    #args_3: dict = dict()
    #main_3(args_3)
    
    args_4: dict = {"dirs": list(DIRS_20)}
    main_4(args_4)
    
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
