import common_types as CT
import opaque_user_types as OT

import opaque_helper_functions as OpHlp
import util as UTIL
import const_data as CDATA


def get_multi_hashable_data(obj_iter: OT.t_ObjIter, getter: OT.t_FnGetHashable \
                            , options: OT.t_OpaqueObj) \
                            -> CT.t_HashableIter:
    """ Creates 2-tuples of object and its relevant hashable data.  """
#(
    return map( lambda x: (x, getter(x, options)) , obj_iter )
#)


def group_objects(obj_iter: OT.t_ObjIter, get_obj_hashable: OT.t_FnGetHashable, \
                    options:CT.t_Any) -> OT.t_HashToSetDict:
#(
    hsh_to_objs: OT.t_HashToSetDict = dict()
    
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


def apply_grouper_funcs_dfs(obj_iter, getter_and_param_list: \
                            CT.t_List[OT.FnHashableParamPair], FN_IDX: CT.t_Int) \
                            :
                            #-> CT.t_List[OT.t_KeyGroupPair]:
#(
    FN_LIST_LEN = len(getter_and_param_list)
    
    if FN_IDX >= FN_LIST_LEN:
    #(
        return obj_iter
    #)
    
    obj_iter = list(obj_iter)
    
    if len(obj_iter) < 2: # 1-element group can not contain duplicates.
        return []
    
    fn_and_param = getter_and_param_list[FN_IDX]
    getter: OT.t_FnGetHashable = fn_and_param.function
    opt_param: CT.t_Any = fn_and_param.opt_param
    
    mapping = group_objects(obj_iter, getter, opt_param)
    
    
    if FN_IDX == FN_LIST_LEN - 1: # Last grouper was applied. Return key,group iterable.
    #(
        # items = key, group iterable.
        return filter(lambda x: len(x[1]) > 1 , mapping.items()) # Len group > 1.
    #)
    
    
    # Combine key,group iterables and return.
    NEXT_FN_IDX = FN_IDX + 1
    #key_group_pairs: CT.t_List[OT.t_KeyGroupPair] = []
    key_group_pairs = []

    for key, group in mapping.items():
    #(
        sub_pairs = apply_grouper_funcs_dfs(group, getter_and_param_list, \
                                            NEXT_FN_IDX)
        #
        key_group_pairs.extend(sub_pairs)
    #)
    
    return key_group_pairs
#)


def apply_grouper_funcs(obj_iter, getter_and_param_list: \
                        CT.t_List[OT.FnHashableParamPair]):
#(
    if len(getter_and_param_list) < 1: # No grouper to process.
    #(
        return obj_iter
    #)
    
    for elm in getter_and_param_list:
    #(
        grouper = elm.function
        assert (grouper != None)
    #)
    
    FN_IDX = 0
    return apply_grouper_funcs_dfs(obj_iter, getter_and_param_list, FN_IDX)
#)


def print_path_size_iter(paths_n_sizes):
#(
    for ix, elm in enumerate(paths_n_sizes):
    #(
        print(f"Path ({ix}): {elm[0]}")
        print(f"Size: {elm[1]} bytes, {round(elm[1]/1024, 2)} Kb, {round(elm[1]/1024/1024, 2)} Mb")
        print()
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


def filter_and_apply_groupers(obj_iter, SMALLEST_FSIZE, GROUPERS):
#(
    fpaths = OpHlp.collect_all_file_paths(obj_iter, lambda x: x)
    
    PATHS = tuple(fpaths)
    
    nonsmall_files = filter(lambda elm: UTIL.get_local_file_size(elm, None) >= \
                            SMALLEST_FSIZE , PATHS)
    #
    
    key_group_pairs = apply_grouper_funcs(nonsmall_files, GROUPERS)
    
    return key_group_pairs
#)


def filter_and_multiple_hash(obj_iter, SMALLEST_FSIZE, BYTE_IDX_PAIRS):
#(
    size_grpr = OT.FnHashableParamPair(UTIL.get_local_file_size, None)
    
    
    def hash_getter(fpath, prm):
    #(
        start = prm["start_offset"]
        end = prm["end_offset"]
        
        data = UTIL.read_local_file_bytes(fpath, start, end)
        
        return UTIL.sha512_hexdigest(data)
    #)
    
    #BYTE = 1
    #KB = 1024
    #MB = 1024 * KB
    
    hash_grprs = []
    for start, end in BYTE_IDX_PAIRS:
    #(
        pair = OT.FnHashableParamPair(hash_getter, \
                                    {"start_offset": start , "end_offset": end})
        #
        hash_grprs.append(pair)
    #)
    
    return filter_and_apply_groupers(obj_iter, SMALLEST_FSIZE, [size_grpr, *hash_grprs])
#)



def filter_and_triple_hash(obj_iter, SMALLEST_FSIZE):
#(
    BYTE = 1
    KB = 1024
    MB = 1024 * KB
    
    byte_idx_pairs = [ 
                        (0, 512 * BYTE) \
                        ,(0, 64 * KB) \
                        , (0, 1 * MB) \
                    ]
    
    return filter_and_multiple_hash(obj_iter, SMALLEST_FSIZE, byte_idx_pairs)
#)


def main_11(args):
#(
    import time
    
    START_DATETIME = UTIL.local_datetime_str_iso8601()
    print(f"main_11 Start: {START_DATETIME}")
    #512000 byte smallest file size.
    #Groupers=size,512-hash,65536-hash 
    time_start = time.perf_counter()
    
    #json_out_path = args["json_out_path"]
    #milliseconds = round(time.time_ns() / 1000)
    json_out_path = f"op-core.main-11.{UTIL.local_datetime_str_iso8601()}.json"
    csv_out_path = f"op-core.main-11.{UTIL.local_datetime_str_iso8601()}.csv"
    
    DIRS = CDATA.DIRS
    
    dirs = ["/home/genel"] # 125650 items, totalling 52,5 GiB (56.358.510.573 bytes)
    #dirs = ["/media/genel/Bare-Data/"] # 34735 items, totalling 67,6 GiB (72.553.152.052 bytes)
    #dirs = ["/media/genel/9A4277A5427784B3/"] # 513816 items, totalling 88,4 GiB (94.866.674.987 bytes)
    
    #dirs = DIRS["dirs_20"]
    
    #print(f"Dirs: {dirs}")
    
    BYTE = 1
    KB = 1024 * BYTE
    MB = 1024 * KB
    
    #SMALLEST_FSIZE = 128 * KB
    SMALLEST_FSIZE = 500 * KB
    
    # TODO(armagan): Change Smallest_fsize. 64KB?
    
    # Try: (256Byte, 2KB, 128KB)
    
    # (256 Byte, 2 KB, 64 KB, 1 MB) seems a good balance for (512 KB smallest) hash byte index intervals.
    
    
    # Try only 128 bytes for Win10. Check hot and cold speed with that config.
    byte_idx_pairs = [ 
                        (0, 256 * BYTE) \
                        ,(0, 2 * KB) \
                        ,(0, 64 * KB) \
                        #,(0, 1 * MB) \
                    ]
    #
    #Win10; time (second)": 1014.4773, "Hash byte idx pairs": [[0, 256], [0, 2048], [0, 1048576]]
    
    
    key_group_pairs = filter_and_multiple_hash(dirs, SMALLEST_FSIZE, byte_idx_pairs)
    
    #print(f"main_11 csv End: {UTIL.local_datetime_str_iso8601()}")
    #exit()
    
    time_end = time.perf_counter()
    
    group_time_diff = time_end - time_start
    
    jsndata = UTIL.key_group_pairs_to_json_data(key_group_pairs)
    
    #objects = jsndata["groups"]
    total_time = time.perf_counter() - time_start
    
    
    #grp_time = UTIL.second_to_minute_second_str(round(group_time_diff, 3))
    #total_time = UTIL.second_to_minute_second_str(round(total_time, 3))
    
    info = dict()
    
    info["START_DATETIME"] = START_DATETIME
    info["Directories"] = dirs
    info["Smallest file size (bytes)"] = SMALLEST_FSIZE
    info["Elapsed seconds for groupers"] = round(group_time_diff, 3)
    #info["Group + convert to json time"] = round(total_time, 3)
    info["Hash byte idx pairs"] = byte_idx_pairs
    
    DATETIME_BEFORE_JSON_WRITE = UTIL.local_datetime_str_iso8601()
    info["DATETIME_BEFORE_JSON_WRITE"] = DATETIME_BEFORE_JSON_WRITE
    
    jsndata["Info"] = info
    
    UTIL.write_json(jsndata, json_out_path)
    
    csv_data = UTIL.key_group_pairs_to_csv_data(key_group_pairs, info)
    UTIL.write_csv(csv_data, csv_out_path)
    
    print(f"main_11 End: {UTIL.local_datetime_str_iso8601()}")
#)


def main_12(args):
#(
    DIRS = CDATA.DIRS
    
    dirs = DIRS["dirs_20"]
    
    BYTE = 1
    KB = 1024 * BYTE
    SMALLEST_FSIZE = 512 * KB
    
    key_group_pairs = filter_and_triple_hash(dirs, SMALLEST_FSIZE)
    
    grp_idx = 0
    fidx = 0
    for key,grp in key_group_pairs:
    #(
        for elm in grp:
        #(
            print(f"(Group=({grp_idx}), File=({fidx})), ({elm})")
            fidx += 1
        #)
        print()
        
        grp_idx += 1
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
    
    #main_10(dict())
    
    #{"json_out_path": ""}
    main_11( dict() )
    
    #main_12(dict())
    
#)

