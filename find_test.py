"""
import subprocess
#args = ("bin/bar", "-c", "somefile.xml", "-d", "text.txt", "-r", "aString", "-f", "anotherString")
search_dir = "/media/genel/Bare-Data/ALL BOOKS-PAPERS/"
args = ("./gnu_find.elf", search_dir, "-name", "*")
#Or just:
#args = "bin/bar -c somefile.xml -d text.txt -r aString -f anotherString".split()
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
print(output)
"""

import os
import subprocess
from dataclasses import dataclass

from typing import List as t_List


@dataclass
class DirData:
#(
    file_count: int
    size_sum: int
#)


def get_files_from_dir_recursive(dirpath: str, find_exec_path: str):
#(
  # https://docs.python.org/3/library/subprocess.html
  import subprocess
  #args = ("bin/bar", "-c", "somefile.xml", "-d", "text.txt", "-r", "aString", "-f", "anotherString")
  #search_dir = "/media/genel/Bare-Data/ALL BOOKS-PAPERS/"
  search_dir = dirpath
  # For maximum reliability, use a fully-qualified path for the executable.
  # ! -type d == exclude dirs from output.
  # -type f == include only regular files.
  # find_exec_path = "../bin/findutils/gnu_find.elf"
  args = (find_exec_path, search_dir, "-name", "*", "-type", "f")
  #Or just:
  #args = "bin/bar -c somefile.xml -d text.txt -r aString -f anotherString".split()
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)

  out, err_out = popen.communicate() # Warning: Holds all data in memory. Can overflow.

  return out.decode("utf-8").split("\n")
#)


def get_files_recursive_multi_dir(dirs: t_List[str] , find_exec_path: str) \
                                    -> bytes:
#(
    args = [find_exec_path]
    args.extend(dirs)
    
    options = ["-name", "*", "-type", "f"]
    args.extend(options)
    
    completed = subprocess.run(args, capture_output=True)
    # .returncode should be zero typically.
    
    out_bytes = completed.stdout
    
    return out_bytes
#)


def main_1():
#(
    to_search = "/media/genel/Bare-Data/ALL BOOKS-PAPERS/"
    res = get_files_from_dir_recursive(to_search)
    print(res)
#)


def main_2(args):
#(
    dirs = args["dirs"]
    
    files = []
    
    for elm in dirs:
    #(
        lst = get_files_from_dir_recursive(elm)
        files.extend(lst)
    #)
    
    
    sizes = map( os.path.getsize , filter(os.path.isfile , files) )
    
    sz_list = list(sizes)
    
    total_sum = sum(sz_list)

    data = DirData(file_count = len(sz_list) , size_sum = total_sum)
    
    print(f"Total file count == {data.file_count} \
            , size_sum == {data.size_sum} bytes")
#)


def main_3(args):
#(
    dirs = ["/home/genel/Videos/", "/home/genel/Pictures/" \
            , "/home/genel/Downloads/"]
    
    gnu_find_path = "./bin/findutils/gnu_find.elf"
    
    files: bytes = get_files_recursive_multi_dir(dirs, gnu_find_path)
    
    print(files[:333])
    
    files_str: str = files.decode("utf-8")
    
    files_list = files_str.split('\n') # Last element is EOF. Discard it.
    
    print("-------------------")
    print(files_str)

    print("-------------------")
    print(files_list[:-1])
#)


def main_4(args):
#(
    dirs = ["/home/genel/Videos/", "/home/genel/Pictures/" \
            , "/home/genel/Downloads/", "/home"]

    
    # dirs = args["dirs"]
    
    gnu_find_path = "./bin/findutils/gnu_find.elf"
    
    files: bytes = get_files_recursive_multi_dir(dirs, gnu_find_path)
    
    files_str: str = files.decode("utf-8")
    
    all_files = files_str.split('\n')[:-1] # Last element is EOF. Discard it.
    
    all_files.sort()
    
    print('\n'.join(all_files))
    print(f"Total non-symbolic file count == {len(all_files)}")
    
    sizes = map( os.path.getsize , filter(os.path.isfile , all_files) )
    
    sz_list = list(sizes)
    
    total_sum = sum(sz_list)

    data = DirData(file_count = len(sz_list) , size_sum = total_sum)
    
    print(f"Total file count == {data.file_count} \
            , size_sum == {data.size_sum} bytes")
#)


def main_5(args):
#(
    dirs = args["dirs"]
    
    gnu_find_path = "./bin/findutils/gnu_find.elf"
    
    files: bytes = get_files_recursive_multi_dir(dirs, gnu_find_path)
    
    files_str: str = files.decode("utf-8")
    
    all_files = files_str.split('\n')[:-1] # Last element is EOF. Discard it.
    
    print(f"Total non-symbolic file count == {len(all_files)}")
    
    
    for idx, f in enumerate(all_files):
    #(
        print(f"File ({idx}) path == {f}")
        
        sz = os.path.getsize(f)
        print(f"File ({idx}) size == {sz/(1024**2):.2} Mb , {sz/(1024):.2} Kb , {sz} bytes.")
        print()
    #)
    exit()
    
    size_iter = map( os.path.getsize , filter(os.path.isfile , all_files) )
    
    sz_list = list(size_iter)
    
    total_sum = sum(sz_list)

    data = DirData(file_count = len(sz_list) , size_sum = total_sum)
    
    print(f"Total file count == {data.file_count} \
            , size_sum == {data.size_sum} bytes")
#)


if __name__ == "__main__":
#(
    # TODO(armagan): If multiple directories has a common prefix,
    # use the path with the maximum common prefix for GNU find, 
    # discard others. (Use *parent folders when present.)
    
    dirs = [ "/media/genel/SAMSUNG/NOT SAMS/Personal/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Movies-Series/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ALL BOOKS-PAPERS/" \
        , "/media/genel/SAMSUNG/NOT SAMS/ESSENTIAL BACKUP/" \
        , "/media/genel/SAMSUNG/NOT SAMS/BACKUP-HP-2022-05-06/" ]
    #
    args = {"dirs": dirs}
    
    # main_2(args)
    # main_3(dict())
    
    # main_4(dict())
    
    dirs_5 = dirs
    dirs_5.extend( ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/"] )
    
    args_5 = {"dirs": dirs_5}
    main_5(args_5)
#)
