import logging

import common_types as CT
import opaque_user_types as OT

import opaque_helper_functions as OpHlp
import util as UTIL
import maybe as Maybe
import private_data as CDATA

import constants as CONST

BYTE = CONST.BYTE
KB = CONST.KB
MB = CONST.MB


def get_multi_hashable_data(obj_iter: OT.t_ObjIter, getter: OT.t_FnGetHashable, options: OT.t_OpaqueObj) \
        -> CT.t_HashableIter:
    """ Creates 2-tuples of object and its relevant hashable data.  """
# (
    return map(lambda x: (x, getter(x, options)), obj_iter)
# )


def group_objects(obj_iter: OT.t_ObjIter, get_obj_hashable: OT.t_FnGetHashable, options: CT.t_Any) \
        -> OT.t_HashToSetDict:
    # (
    hsh_to_objs: OT.t_HashToSetDict = dict()

    for obj in obj_iter:
        # (
        hsh = None

        try:
            # (
            hsh = get_obj_hashable(obj, options)
        # )
        except Exception as Err:
            # (
            msg = [f"Can't get hash from object ~{str(obj)}~", "It was skipped." \
                    , f"Exception: {str(Err)}" \
                    , f"Function: {__name__}.group_objects" \
                    , "~~~" ]
            #

            logging.error('\n'.join(msg))

            continue
        # )

        same_hash_group: CT.t_Set = hsh_to_objs.get(hsh, None)

        if same_hash_group == None:
            # (
            new_hashable_set = set()
            new_hashable_set.add(obj)

            hsh_to_objs[hsh] = new_hashable_set
        # )
        else:
            # (
            same_hash_group.add(obj)
        # )
    # )

    return hsh_to_objs
# )


def get_multi_obj_bytes(obj_iter: OT.t_ObjIter, get_obj_bytes: OT.t_FnGetObjBytes, start_idx: OT.t_StartIdx, end_idx: OT.t_EndIdx):
    # (
    # TODO(armagans): Use function, opt_arg pair. Retrieve params from opt_arg,
    # don't take them as parameters to this function.

    map(lambda x: (x, get_obj_bytes(x, start_idx, end_idx)), obj_iter)
# )

# TODO(armagan): Make a fn separate_unq_dups that returns unique key-group pairs
# and potentially duplicate key-group pairs in a named tuple (collections.namedtuple).


def apply_grouper_funcs_dfs(obj_iter, getter_and_param_list:
                            CT.t_List[OT.FnHashableArgPair], FN_IDX: CT.t_Int):
    # -> CT.t_List[OT.t_KeyGroupPair]:
    # (
    FN_LIST_LEN = len(getter_and_param_list)

    if FN_IDX >= FN_LIST_LEN:
        # (
        return obj_iter
    # )

    obj_iter = list(obj_iter)

    if len(obj_iter) < 2:  # 1-element group can not contain duplicates.
        return []

    fn_and_param = getter_and_param_list[FN_IDX]
    getter: OT.t_FnGetHashable = fn_and_param.function
    opt_param: CT.t_Any = fn_and_param.opt_arg

    mapping = group_objects(obj_iter, getter, opt_param)

    # Last grouper was applied. Return key,group iterable.
    if FN_IDX == FN_LIST_LEN - 1:
        # (
        # items = key, group iterable.
        # Len group > 1.
        return filter(lambda x: len(x[1]) > 1, mapping.items())
    # )

    # Combine key,group iterables and return.
    NEXT_FN_IDX = FN_IDX + 1
    #key_group_pairs: CT.t_List[OT.t_KeyGroupPair] = []
    key_group_pairs = []

    for key, group in mapping.items():
        # (
        sub_pairs = apply_grouper_funcs_dfs(group, getter_and_param_list,
                                            NEXT_FN_IDX)
        #
        key_group_pairs.extend(sub_pairs)
    # )

    return key_group_pairs
# )


def apply_grouper_funcs(obj_iter, getter_and_param_list:
                        CT.t_List[OT.FnHashableArgPair]):
    # (
    if len(getter_and_param_list) < 1:  # No grouper to process.
        # (
        return obj_iter
    # )

    for elm in getter_and_param_list:
        # (
        grouper = elm.function
        assert (grouper != None)
    # )

    FN_IDX = 0
    return apply_grouper_funcs_dfs(obj_iter, getter_and_param_list, FN_IDX)
# )


def filter_and_apply_groupers(obj_iter, FSIZE_MINMAX_PAIR, GROUPERS):
    # (
    fpaths: CT.t_Iter = OpHlp.collect_all_file_paths(obj_iter, lambda x: x)
    
    PATHS = tuple(fpaths)
    
    if len(PATHS) < 2:
        logging.error(f"Couldn't collect file paths. Does the user have read permissions for search paths?")
    
    logging.info(f"Collected, unfiltered file path count: {len(PATHS)}")
    
    def size_filter(elm):
        """ Returns True if file object is between MINMAX limits. """
    #(
        SZ = None
        try:
        #(
            SZ = UTIL.get_local_file_size(elm, None)
        #)
        except Exception as Err:
        #(
            logging.error(f"Couldn't get size for: {str(elm)}. Error: {str(Err)}")
            
            return False
        #)
        
        MIN_LIMIT, MAX_LIMIT = FSIZE_MINMAX_PAIR
        
        is_valid = True
        
        is_valid = MIN_LIMIT <= SZ if (MIN_LIMIT is not None) else True
        
        is_valid = is_valid and (MAX_LIMIT >= SZ) if (MAX_LIMIT is not None) else is_valid
        
        return is_valid
    #)
    
    nonsmall_files = filter(size_filter, PATHS)
    #
    NS_FILES = tuple(nonsmall_files)
    
    logging.info(f"Filtered file path count: {len(NS_FILES)}")
    
    key_group_pairs = apply_grouper_funcs(NS_FILES, GROUPERS)

    return key_group_pairs
# )


def filter_and_multiple_hash(obj_iter, FSIZE_MINMAX_PAIR, BYTE_IDX_PAIRS):
    # (
    size_grpr = OT.FnHashableArgPair(UTIL.get_local_file_size, None)

    def hash_getter(fpath, prm):
        # (
        start = prm["start_offset"]
        end = prm["end_offset"]

        data = UTIL.read_local_file_bytes(fpath, start, end)

        return UTIL.sha512_hexdigest(data)
    # )

    #BYTE = 1
    #KB = 1024
    #MB = 1024 * KB

    hash_grprs = []
    for start, end in BYTE_IDX_PAIRS:
        # (
        pair = OT.FnHashableArgPair(hash_getter,
                                    {"start_offset": start, "end_offset": end})
        #
        hash_grprs.append(pair)
    # )

    return filter_and_apply_groupers(obj_iter, FSIZE_MINMAX_PAIR, [size_grpr, *hash_grprs])
# )


def main_11(args):
    # (
    import time

    START_DATETIME = UTIL.local_datetime_str_iso8601()
    print(f"main_11 Start: {START_DATETIME}")

    time_start = time.perf_counter()

    json_out_path = f"Result_duplicates_{UTIL.local_datetime_str_iso8601()}.json"
    csv_out_path = f"Result_duplicates_{UTIL.local_datetime_str_iso8601()}.csv"

    dirs = args["dirs"]
    #MINIMUM_FSIZE, MAXIMUM_FSIZE = args["FSIZE_LIMITS"]
    byte_idx_pairs = args["byte_idx_pairs"]

    key_group_pairs = filter_and_multiple_hash(
        dirs, args["FSIZE_MINMAX_PAIR"], byte_idx_pairs)

    time_end = time.perf_counter()

    group_time_diff = time_end - time_start

    jsndata = UTIL.key_group_pairs_to_json_data(key_group_pairs)

    #objects = jsndata["groups"]
    total_time = time.perf_counter() - time_start

    info = dict()

    info["START_DATETIME"] = START_DATETIME
    info["Scan Function"] = f"{__name__}.main_11"
    info["Directories"] = dirs
    info["Min, Max file size limits (bytes)"] = args["FSIZE_MINMAX_PAIR"]
    info["Elapsed seconds for groupers"] = round(group_time_diff, 3)
    #info["Group + convert to json time"] = round(total_time, 3)
    info["Hash byte idx pairs"] = byte_idx_pairs

    DATETIME_BEFORE_JSON_WRITE = UTIL.local_datetime_str_iso8601()
    info["DATETIME_BEFORE_OUTPUT_WRITE"] = DATETIME_BEFORE_JSON_WRITE

    jsndata["Info"] = info

    #UTIL.write_json(jsndata, json_out_path)

    CSV_DATA_VERSION = 1
    csv_data = UTIL.key_group_pairs_to_csv_data(
        CSV_DATA_VERSION, key_group_pairs, info)
    #
    UTIL.write_csv(csv_data, csv_out_path)

    print(f"main_11 End  : {UTIL.local_datetime_str_iso8601()}")

    return key_group_pairs
# )


if __name__ == "__main__":
    # (
    raise Exception("This module is not runnable.")
# )
