import common_types as CT
import opaque_user_types as OT

import opaque_helper_functions as OpHlp
import util as UTIL


def get_multi_hashable_data(obj_iter: OT.t_ObjIter, getter: OT.t_FnGetHashable \
                            , options: OT.t_OpaqueObj) \
                            -> CT.t_HashableIter:
    """ Creates 2-tuples of object and its relevant hashable data.  """
#(
    return map( lambda x: (x, getter(x, options)) , obj_iter )
#)


def group_objects(obj_iter: OT.t_ObjIter, get_obj_hashable: OT.t_FnGetHashable, \
                    options:CT.t_Any):
#(
    hsh_to_objs: CT.t_Dict[CT.t_Hashable, CT.t_Set[OT.t_OpaqueObj]] = dict()
    
    for obj in obj_iter:
    #(
        hsh = get_obj_hashable(obj, options)
        
        same_hash_group = hsh_to_objs.get(hsh, None)
        
        if same_hash_group == None:
        #(
            new_hashable_set = set()
            new_hashable_set.add(obj)
            
            hsh_to_objs[hsh] = new_hashable_set
        #)
        else:
        #(
            same_hash_group.add(obj)
        #)
    #)
    
    return hsh_to_objs
    
#)


def group_objs_by_fsize(obj_iter: OT.t_ObjIter, get_obj_size: OT.t_FnGetHashable):
#(
    return group_objects(obj_iter, get_obj_size, None)
#)


def get_multi_obj_bytes(obj_iter: OT.t_ObjIter, get_obj_bytes: OT.t_FnGetObjBytes, \
                        start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
#(
    # TODO(armagan): Make this a generator for memory efficiency.
    for obj in obj_iter:
    #(
        received_bytes = get_obj_bytes(obj, start_idx, end_idx)
        yield ( obj, received_bytes )
    #)
#)


def ignore_unique_groups(obj_iter: OT.t_ObjIter, get_key: OT.t_FnGetKey, \
                    get_group: OT.t_FnGetValue):
#(
    DUPLICATE_THRESHOLD = 2
    potential_dups: CT.t_List[CT.t_List] = [] # [[key1,group1], [key2,group2], ...]
    
    for obj in obj_iter:
    #(
        key, group = get_key(obj), get_group(obj)
        
        sz = 0
        try:
        #(
            sz = len(group)
        #)
        except: # Group object might not have a len method.
        #(
            sz = len(list(group))
        #)
        
        if sz < DUPLICATE_THRESHOLD: 
        # A duplicate group always have at least DUPLICATE_THRESHOLD elements.
        #(
            continue # Ignore this key, group pair.
        #)
        else: # This group holds potential duplicates.
        #(
            potential_dups.append([key, group])
        #)
    #)
    
    return potential_dups
#)


def ignore_zero_len(obj_iter: OT.t_ObjIter, get_size: OT.t_FnGetObjSize):
#(
    for obj in obj_iter:
    #(
        sz = get_size(obj)
        if sz < 1:
            continue
        else:
            yield obj
    #)
#)


# TODO(armagan): Make a fn separate_unq_dups that returns unique key-group pairs
# and potentially duplicate key-group pairs in a named tuple (collections.namedtuple).


def print_path_size_iter(paths_n_sizes):
#(
    for ix, elm in enumerate(paths_n_sizes):
    #(
        print(f"Path ({ix}): {elm[0]}")
        print(f"Size: {elm[1]} bytes, {elm[1]//1024} Kb, {elm[1]// (1024**2)} Mb")
        print()
    #)
#)


def main_1(args):
#(
    dirs = ["/home/genel", "/home/genel", "/home/genel", "/home/genel/Desktop/" \
            ,"/home/genel/Desktop/" ]
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_2(args):
#(
    dirs = ["/media/genel/Bare-Data/"]
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_3(args):
#(
    dirs = ["/media/genel/9A4277A5427784B3/"]
    # 513815 items, totalling 88,4 GiB (94.866.674.987 bytes)
    # 408255 of which are files.
    
    """
    real    9m27,050s
    user    0m23,461s
    sys     1m25,914s
    """
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    print_path_size_iter(path_n_sizes)
#)


def main_4(args):
#(
    dirs = ["/media/genel/Bare-Data/"]
    # 34734 items. 32742 files.
    
    path_n_sizes = get_fsizes_from_given_dirs(dirs, lambda x: x)
    
    size_groups = group_objs_by_fsize(path_n_sizes, lambda x: x[1])
    
    count = 0
    for sz, multi_obj in size_groups.items():
    #(
        if len(multi_obj) < 2: # Unique item. No duplicate.
            continue
        
        print("-----------")
        print(f"Group size: {sz}")
        print("Objects: ...")
        
        for obj in multi_obj:
        #(
            count += 1
            
            print(f"Object {count}: {obj}")
        #)
        print()
    #)
    
    
    #print_path_size_iter(path_n_sizes)
#)


def main_5(args):
#(
    dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    GAP = 1024 * 1
    
    start_idx = 0
    end_idx = GAP + start_idx - 1
    
    print(f"Gap:{GAP}, start_idx:{start_idx}, end_idx:{end_idx}")
    
    def read_byte_from_path(path, start, end):
    #(
        return UTIL.read_local_file_bytes(path, start, end)
    #)
    
    obj_bytes_coll = get_multi_obj_bytes(fpaths, read_byte_from_path, start_idx, end_idx)
    
    for idx, elm in enumerate(obj_bytes_coll):
    #(
        obj, data = elm
        
        print(f"----------- {idx}")
        print(obj)
        
        sz = len(data)
        
        print_len = 10
        
        if sz < print_len:
            print(sz)
        else:
            print(data[-print_len:])
        #
        print()
    #)
#)


def main_6(args):
#(
    dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    size_groups = group_objs_by_fsize(fpaths, UTIL.get_local_file_size)
    
    print(f"Total key count: {len(size_groups)}")
    
    dict_str = UTIL.pretty_dict_str(size_groups, "File len bytes to paths")
    
    print(dict_str)
    
    uniques = ignore_uniques(size_groups.items(), lambda x: x[0], lambda x: x[1])
    
    lol_str = UTIL.list_of_two_tuples_str(uniques, "File size bytes, File paths")
    
    print(lol_str)
    
    exit()
    #######
    
    GAP = 1024 * 1
    
    start_idx = 0
    end_idx = GAP + start_idx - 1
    
    print(f"Gap:{GAP}, start_idx:{start_idx}, end_idx:{end_idx}")
    
    def read_byte_from_path(path, start, end):
    #(
        return UTIL.read_local_file_bytes(path, start, end)
    #)
#)


def print_uniques_by_size(args):
#(
    #dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    dirs = args["dirs"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    size_groups = group_objs_by_fsize(fpaths, UTIL.get_local_file_size)
    
    print(f"Total key count: {len(size_groups)}")
    
    dict_str = UTIL.pretty_dict_str(size_groups, "File len bytes to paths")
    
    print(dict_str)
    
    uniques = ignore_unique_groups(size_groups.items(), lambda x: x[0], lambda x: x[1])
    
    lot_str = UTIL.list_of_two_tuples_str(uniques, "File size bytes, File paths")
    
    print(lot_str)
#)


def main_7(args):
#(
    dirs = ["/home/genel/", "/home/genel/Downloads/"]
    
    dct = {"dirs": dirs}
    
    print_uniques_by_size(dct)
#)


def main_8(args):
#(
    dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    PATHS = list(fpaths)
    
    def size_getter(obj, options):
    #(
        return UTIL.get_local_file_size(obj)
    #)
    
    objs_n_sizes = get_multi_hashable_data(fpaths, size_getter, None)
    
    tmp = map(lambda x: [x[0], [x[1]]], objs_n_sizes)
    
    string = UTIL.list_of_two_tuples_str(tmp, "Objects and Sizes")
    
    print(string)
    
    
    def read_file_bytes(obj, options: CT.t_Any) -> CT.t_Bytes:
    #(
        start = options["start_idx"]
        end = options["end_idx"]
        path = obj
        
        return UTIL.read_local_file_bytes(path, start, end)
    #)
    
    dct = {"start_idx":0, "end_idx":64}
    obj_bytes = get_multi_hashable_data(PATHS, read_file_bytes, dct)
    
    tmp2 = map(lambda x: [ x[0] , UTIL.sha512_hexdigest(x[1]) ] , obj_bytes)
    
    for left, right in tmp2:
    #(
        print(f"Left: {left}")
        print(f"Right: {right}")
    #)
    
#)


def main_9(args):
#(
    dirs = ["/home/genel/Downloads/", "/home/genel/Documents/"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    PATHS = list(fpaths)
    
    size_groups = group_objects(PATHS, UTIL.get_local_file_size, None)
    
    dup_groups = ignore_unique_groups(size_groups.items(), \
                                    lambda x: x[0], lambda x: x[1])
    #
    
    
    
    pretty_str = UTIL.list_of_two_tuples_str(dup_groups, "Removed Uniques, Non-zero len")
    
    print(pretty_str)
    
    def read_bytes(obj, options):
    #(
        return UTIL.read_local_file_bytes(obj, options["start_idx"], options["end_idx"])
    #)
    
    dct = {"start_idx":0 , "end_idx": 64}
    obj_to_bytes = get_multi_hashable_data(PATHS, read_bytes, dct)
    
    obj_to_sha512digest = map(lambda x: [ x[0], UTIL.sha512_hexdigest(x[1]) ], \
                                obj_to_bytes)
    #

    #
    
    
#)


def main_10(args):
#(
    dirs = ["/home/genel/"]
    
    fpaths = OpHlp.collect_all_file_paths(dirs, lambda x: x)
    
    PATHS = list(fpaths)
    
    def read_bytes(obj, options):
    #(
        return UTIL.read_local_file_bytes(obj, options["start_idx"], options["end_idx"])
    #)
    
    dct = {"start_idx":0 , "end_idx": 64}
    obj_to_bytes = get_multi_hashable_data(PATHS, read_bytes, dct)
    
    obj_to_sha512digest = map(lambda x: [ x[0], UTIL.sha512_hexdigest(x[1]) ], \
                                obj_to_bytes)
    #
    
    ix = 0
    for obj, digest in obj_to_sha512digest:
    #(
        print(f"~~~~~~~ Index: {ix}")
        print(f"Obj: {obj}")
        print(f"- sha512: {digest}")
        
        ix += 1
    #)
#)


if __name__ == "__main__":
#(
    #main_1(dict())
    
    #main_2(dict())
    
    #main_3(dict())
    
    #main_4(dict())
    
    #main_5(dict())
    
    #main_6(dict())
    
    #main_7(dict())
    
    #main_8(dict())
    
    #main_9(dict())
    
    main_10(dict())
    
#)

