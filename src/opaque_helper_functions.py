import os

import common_types as CT
import opaque_user_types as OT

import path_functions as PFuncs
#from private_data import DIRS
import util as UTIL


def ignore_redundant_subdirs(obj_iter: OT.t_ObjIter,
                             get_path_from_obj: OT.t_FnGetObjPath):
    # (
    # TODO(armagans): Don't lose objects. Return values should be opaque objects,
    # not path strings.
    paths = map(get_path_from_obj, obj_iter)

    return PFuncs.ignore_redundant_subdirs(paths)
# )


def get_fpaths_recursively(ref: OT.t_OpaqueObj,
                           get_path_from_obj: OT.t_FnGetObjPath):
    # (
    path = get_path_from_obj(ref)

    return PFuncs.get_fpaths_recursively(path)
# )


def get_fpaths_from_path_iter(obj_iter: OT.t_ObjIter,
                              get_path_from_obj: OT.t_FnGetObjPath) \
        -> CT.t_Iter[CT.t_Tuple[CT.t_Any, CT.t_List]]:
    # (
    selected_dirs = ignore_redundant_subdirs(obj_iter, get_path_from_obj)

    objs_to_paths = []

    for obj in selected_dirs:
        # (
        found_paths = get_fpaths_recursively(obj, get_path_from_obj)

        objs_to_paths.append((obj, found_paths))

        # TODO(armagan): ???Use yield instead of return???
    # )

    return objs_to_paths
# )


def combine_file_paths_from_tuples(obj_pathlist_tuples):
    # (
    combination = []

    for tpl in obj_pathlist_tuples:
        # (
        combination.extend(tpl[1])
    # )

    return combination
# )


def filter_for_files(paths: CT.t_Iter[CT.t_Str]):
    # (
    return filter(os.path.isfile, paths)
# )


def collect_all_file_paths(obj_iter: OT.t_ObjIter,
                           get_dirpath_from_obj: OT.t_FnGetObjPath) \
                           -> CT.t_Iter:
    # (
    dir_filelist_tuples = get_fpaths_from_path_iter(
        obj_iter, get_dirpath_from_obj)

    # OpHlp.
    potential_fpaths = combine_file_paths_from_tuples(dir_filelist_tuples)

    fpaths = filter(os.path.isfile, potential_fpaths)

    return fpaths
# )


def get_local_file_bytes(obj: OT.t_OpaqueObj, get_file_path: OT.t_FnGetObjPath,
                         start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
    # (
    path_str = get_file_path(obj)

    read_bytes = UTIL.read_local_file_bytes(path_str, start_idx, end_idx)
    # Includes end_idx byte.

    return read_bytes  # Returns b'' on error.
# )


def get_multi_obj_sizes(obj_iter: OT.t_ObjIter, get_obj_size: OT.t_FnGetObjSize,
                        opts: OT.t_Arg):
    # (
    return map(lambda x: (x, get_obj_size(x, opts)), obj_iter)
# )


def get_fsizes_from_given_dirs(obj_iter: OT.t_ObjIter,
                               get_path_from_obj: OT.t_FnGetObjPath,
                               opts: OT.t_Arg):
    # (
    #selected_dirs = OpHlp.ignore_redundant_subdirs(obj_iter, get_path_from_obj)

    fpaths = collect_all_file_paths(obj_iter, get_path_from_obj)

    return get_multi_obj_sizes(fpaths, UTIL.get_local_file_size, opts)
# )


def main_1(args):
    # (
    data = ["asd", "acv", "xzd", "efr"]

    def fn_get_path(obj: OT.t_OpaqueObj):
        # (
        return obj
    # )

    get_fpaths_from_path_iter(data, fn_get_path)

# )


def main_2(args):
    # (
    data = ["./",
            "/home/genel/Videos/",
            "/home/genel/Music/"]
    #

    def fn_get_path(obj: OT.t_OpaqueObj):
        # (
        return obj
    # )

    #refs = [idx for idx in range(len(data))]

    rec_paths = get_fpaths_from_path_iter(data, fn_get_path)

    for elm in rec_paths:
        # (
        print("-------------")
        print(f"Ref:{elm[0]}")
        print("Paths:")
        for p in elm[1]:
            # (
            print(p)
        # )
    # )
# )


def print_files_and_sizes(args):
    # (
    LOCAL_DIRS = args["dirs"]

    def get_dir_path(obj: OT.t_OpaqueObj):
        # (
        return obj
    # )

    def usr_get_entity_size(obj: OT.t_OpaqueObj) -> OT.t_ObjSize:
        # (
        path = obj

        return os.path.getsize(path)  # TODO(armagan): Error handling.
    # )

    recursive_paths = get_fpaths_from_path_iter(LOCAL_DIRS, get_dir_path)

    # TODO(armagan): Combine recursive path results. Then use it for get_recursive_path.

    found_paths = []

    for dirref, paths in recursive_paths:
        # (
        found_paths.extend(paths)
    # )

    def get_file_path(obj: OT.t_OpaqueObj):
        # (
        return obj
    # )

    for pthidx, elm in enumerate(found_paths):
        # (
        print("-------------")
        print(f"Ref:{pthidx}")

        # (
        print(f"File ({pthidx}) path == {elm}")

        sz = usr_get_entity_size(elm)  # -1 because ref is
        # unimportant for this case.

        print(
            f"File ({pthidx}) size == {sz/(1024**2):.3} Mb , {sz/(1024):.3} Kb , {sz} bytes.")
        print()
        # )
    # )
# )


def main_3(args):
    # (
    dirs = ["./",
            "/home/genel/Videos/",
            "/home/genel/Music/", "/media/genel/Bare-Data/ALL BOOKS-PAPERS/"]
    #
    print_files_and_sizes({"dirs": dirs})
# )


def main_4(args):
    # (
    print_files_and_sizes({"dirs": DIRS["dirs_20"]})  # external storage dirs.
# )


if __name__ == "__main__":
    # (
    # main_1(dict())

    # main_2(dict())

    main_3(dict())

    # main_4(dict())

# )
