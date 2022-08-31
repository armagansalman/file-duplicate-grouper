import os
import hashlib as HASH

import common_types as CT


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


def get_local_file_size(path: CT.t_Str, opt: CT.t_Any):
#(
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
