- TODO(armagan): Learn Markdown

- NOTE: Every type name starts with "t_" characters. First letter after t_
is always capitalized. Example: t_List, t_Int, t_Set, t_Tuple ...

A Traverser module mdl_Traverser is defined as follows:

1) Given an iterable of directory paths, discard every directory if one of 
its parents are also in the iterable. For example: discard 
"/home/videos" and "/home/music" paths if "/home" path is in the iterable.

    Function Signature (in Python syntax):
        t_Str = str
        t_Path = t_Str
        t_PathList = t_List[t_Path]
        
        discard_redundants(DIRS: t_PathList) -> t_PathList


2) Given an iterable of directory paths or file paths, find all file paths
recursively. Return found and given file paths as an iterable.

    Function Signature (in Python syntax):
        t_Str = str
        t_Path = t_Str
        t_PathList = t_List[t_Path]
        
        find_files_recursive(PATHS: t_PathList) -> t_PathList


3) Any input or output path of mdl_Traverser can be relative or absolute.

4) find_files_recursive function does not call discard_redundants function.
The user may or may not want to call discard_redundants function.
