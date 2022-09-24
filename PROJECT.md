# Project Conventions

- Every type name starts with "t_" characters. First letter after t_
is always capitalized. Example: t_List, t_Int, t_Set, t_Tuple ...

- Every code block (similar to C { }) starts with #( and ends with #).
Example:
    for i in range(10):
    #(
        if i < 7:
        #(
            print(i)
        #)
        else:
        #(
            print(2*i)
        #)
    #)

------

A Traverser module mdl_Traverser is defined as follows:

1) Given an iterable of directory paths, discard every directory if one of 
its parents are also in the iterable. For example: discard 
"/home/videos" and "/home/music" paths if "/home" path is in the iterable.

    *Implemented in path_functions.py/ignore_redundant_subdirs (2022-09-24)*
    
    Function Signature (in Python syntax):
        t_Iter = Iterable
        t_Path = A USER DEFINED TYPE
        t_PathIter = t_Iter[t_Path]
        
        discard_redundants(DIRS: t_PathIter) -> t_PathIter:


2) Given an iterable of directory paths or file paths, find all file paths
recursively. Return found and given file paths as an iterable.

    *Implemented in path_functions.py/get_fpaths_from_path_iter (2022-09-24)*
    
    Function Signature (in Python syntax):
        t_Iter = Iterable
        t_Path = A USER DEFINED TYPE
        t_PathIter = t_Iter[t_Path]
        
        find_files_recursive(PATHS: t_PathIter) -> t_PathIter:


3) Any input or output path of mdl_Traverser can be relative or absolute.

4) find_files_recursive function does not call discard_redundants function.
The user may or may not want to call discard_redundants function.

------

From "A Relational Model of Data for Large Shared Data Banks" by E. F. Codd

R(g).r.d
R = Relation name
g = generation identifier (optional)
r = role name (optional)
d = domain name

------

- TODO(armagans): Learn Markdown
- TODO(armagans): ???mypy can't check element types of lists???
