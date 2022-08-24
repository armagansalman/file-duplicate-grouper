import common_types as CT


def read_local_file_bytes(file_path: CT.t_Str, start_offset: CT.t_Int, \
                        end_offset: CT.t_Int):
#(
    # Includes bytes at start_offset and end_offset
    try:
    #(
        data: bytes = b'0'
        
        #TODO(armagan): Read by chunks.
        with open(file_path, "rb") as in_fobj:
            in_fobj.seek(start_offset)
            data = in_fobj.read(end_offset - start_offset + 1)
        #
        
        return data
    #)
    except: # TODO(armagan): Report/except when None.
    #(
        return b''
    #)
#)
