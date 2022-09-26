import os
import time
import hashlib as HASH
import json as JSON

import common_types as CT


def local_datetime_str_iso8601():
#(
    lt = time.localtime()
    
    msec = round(time.time() % 1, 3)
    
    iso_8601_str = f"{lt.tm_year}-{lt.tm_mon}-{lt.tm_mday}T{lt.tm_hour}:{lt.tm_min}:{lt.tm_sec}:{msec}"
    
    return iso_8601_str
#)


def pretty_dict_str(dct, dict_descriptor):
#(
    str_buffer = []
    
    str_buffer.append(f"~~~~~~~~~~~~~ START '{dict_descriptor}' Dictionary ~~~~~~~~~~~~~")
    
    ix = 0
    for k,val in dct.items():
    #(
        str_buffer.append(f"~~~~~~~~~~~~~")
        str_buffer.append(f"( Key, Val Index: {ix} )")
        str_buffer.append(f"-- Key: {k}")
        str_buffer.append(f"- Values:")
        
        
        l_val = list(val)
        prefixed_lval = map(lambda x: "+ " + str(x), l_val)
        
        str_buffer.extend(prefixed_lval)
        
        ix += 1
    #)
    
    str_buffer.append(f"~~~~~~~~~~~~~ END '{dict_descriptor}' Dictionary ~~~~~~~~~~~~~")
    
    dct_lines = '\n'.join(str_buffer)
    
    return dct_lines
#)


def list_of_two_tuples_str(lot, lot_descriptor):
#(
    str_buffer = []
    
    str_buffer.append(f"~~~~~~~~~~~~~ START '{lot_descriptor}' List of Tuples ~~~~~~~~~~~~~")
    
    ix = 0
    for k,val in lot:
    #(
        str_buffer.append(f"~~~~~~~~~~~~~")
        str_buffer.append(f"( 2-Tuple Index: {ix} )")
        str_buffer.append(f"-- Tuple[0]: {k}")
        str_buffer.append(f"- Tuple[1]:")
        l_val = val if type(val) == str else list(val)
        str_buffer.extend(l_val)
        
        ix += 1
    #)
    
    str_buffer.append(f"~~~~~~~~~~~~~ END '{lot_descriptor}' List of Tuples ~~~~~~~~~~~~~")
    
    dct_lines = '\n'.join(str_buffer)
    
    return dct_lines
#)


def get_local_file_size(path: CT.t_Str, options: CT.t_Any) -> CT.t_Int:
#(
    # TODO(armagans): Decide if options can be used inside the function.
    return os.path.getsize(path)
#)


def read_local_file_bytes(file_path: CT.t_Str, start_offset: CT.t_Int, \
                        end_offset: CT.t_Int):
#(
    # Includes bytes at start_offset and end_offset
    
    try:
    #(
        data: bytes = b'0'
        
        #TODO(armagan): Read by chunks.
        with open(file_path, "rb") as in_fobj:
        #(
            if start_offset == 0:
            #(
                data = in_fobj.read(end_offset - start_offset + 1)
            #)
            else:
            #(
                in_fobj.seek(start_offset)
                data = in_fobj.read(end_offset - start_offset + 1)
            #)
        #)
        
        return data
    #)
    except: # TODO(armagan): Report/except when None.
    #(
        return b''
    #)
#)


def read_opaque_local_file_bytes(file_path: CT.t_Str, opt_prm: CT.t_Any):
#(
    return read_local_file_bytes(file_path, opt_prm["start_offset"], \
                                opt_prm["end_offset"])
#)


def sha512_hexdigest(data: CT.t_Bytes):
#(
    sha512_obj = HASH.sha512()
    
    sha512_obj.update(data)
    
    return sha512_obj.hexdigest()
#)


def key_group_pairs_to_json_data(pairs):
#(
    grp_idx = 0
    file_idx = 0
    
    group_objects = []
    for key, group in pairs:
    #(
        dct = {"Group idx":grp_idx}
        element_objects = []
        
        for elm in group:
        #(
            element_objects.append( {"File idx": file_idx \
                                    ,"Item": str(elm)} )
            #
            file_idx += 1
        #)
        dct["Item list"] = element_objects
        
        group_objects.append(dct)
        
        grp_idx += 1
    #)
    return {"Group list": group_objects}
#)


def key_group_pairs_to_csv_data_v1(pairs, info: CT.t_Dict):
#(
    # TODO(armagan): Add info part.
    # [GROUP-FILE-ELEMENT] ;0 ;1 ;"/home/documents/f1"
    # [GROUP-FILE-ELEMENT] ;0 ;2 ;"/home/documents/f2"
    # [INFO] ;"Start time (iso-8601):" ;"2022-09-17T22:12"
    # [INFO] ;"Directories:" ;"/dir1" ;"/dir2" ;"/dir3"
    # [INFO] ;"End time (iso-8601):" ;"2022-09-17T22:13"
    # [INFO] ;"Grouper functions:" ;"500 KB (smallest fsize), sha512: 512 Byte, 4 KB, 1 MB"
    
    CSV_DATA_VERSION = 1
    
    csv_data = []
    
    csv_data.append([ "[ROW TYPE INFO]", "[GID-FID-PATH]", "Group Id, File Id, File Path" ])
    csv_data.append([ "[ROW TYPE INFO]", "[CSV DATA VERSION]", "A hashable value which refers to the specification of a csv output data format." ])
    
    csv_data.append([ "[CSV DATA VERSION]", CSV_DATA_VERSION ])
    
    for key, val in info.items():
    #(
        info_line = ["[INFO]", key, val]
        csv_data.append( info_line )
    #)
    
    
    grp_idx = 0
    file_idx = 0
    
    for key, group in pairs:
    #(
        for elm in group:
        #(
            line_data = ["[GID-FID-PATH]"]
            
            line_data.extend( [str(grp_idx), str(file_idx), str(elm)] )
            
            csv_data.append(line_data)
            
            file_idx += 1
        #)
        csv_data.append( ["[SEPARATOR]"] ) # Add separator after every group.
        
        grp_idx += 1
    #)
    return csv_data
#)


def key_group_pairs_to_csv_data(csv_version: CT.t_Hashable, pairs, info: CT.t_Dict):
#(
    version_to_function = {
                            1: key_group_pairs_to_csv_data_v1 \
                        }
    #
    
    DEFAULT_VERSION_KEY = 1
    csv_data_func = version_to_function[DEFAULT_VERSION_KEY]
    
    if csv_version in version_to_function:
    #(
        csv_data_func = version_to_function[csv_version]
    #)
    
    return csv_data_func(pairs, info)
#)


def write_json(data, fpath, mode="w"):
#(
    with open(fpath, mode, encoding="utf-8") as fout:
    #(
        JSON.dump(data, fout)
    #)
#)


def write_csv(rows, filepath, _encoding="utf8", mode="w"): # Rearrange param order.
#(
    # TODO(armagan): Complete. (Separator (;), quote ("))
    import csv
    
    DELIMITER = ';'
    QUOTECHAR = '"'
    
    with open(filepath, mode, encoding=_encoding, newline='') as csvfile:
    #(    
        csvwriter = csv.writer(csvfile, delimiter=DELIMITER,
                                quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        #
        csvwriter.writerow([ "[CSV INFO]", "Encoding", _encoding ])
        csvwriter.writerow([ "[CSV INFO]", "Delimiter", DELIMITER ])
        csvwriter.writerow([ "[CSV INFO]", "Quotechar", QUOTECHAR ])
        
        csvwriter.writerows(rows)
        #csvwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        #csvwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    #)
#)



