import logging

import opaque_core as OC
import constants as CONST

#import maybe as Maybe
import util as UTIL

#import private_data as PData


BYTE = CONST.BYTE
KB = CONST.KB
MB = CONST.MB


def local_duplicate_scan(args):
    """docstring"""
# (
    return OC.main_11(args)
# )


if __name__ == "__main__":
    """docstring"""
# (
    log_name = "LOG_duplicate-find_" + UTIL.local_datetime_str_iso8601() + ".txt"

    logging.basicConfig(filename=log_name, level=logging.INFO, filemode='a',
                        format='[ %(levelname)s ] | %(asctime)s | %(message)s')
    # '%(levelname)s ~ %(name)s ~ %(asctime)s ~ %(message)s' name is root by default.
    
    
    search_dirs = [ "/home/genel", "/home/genel/Documents/" ]

    #MINIMUM_FSIZE = 500 * KB
    MINIMUM_FSIZE = 1000 * KB
    MAXIMUM_FSIZE = None

    # Each pair == (file_byte_start, file_byte_end)
    byte_idx_pairs = [
        (0, 32 * BYTE) , (0, 256 * BYTE)# , (0, 2 * KB)# , (0, 16 * KB)# , (0, 256 * KB)
    ]
    #
    
    
    params = {"dirs": search_dirs, "FSIZE_MINMAX_PAIR": (MINIMUM_FSIZE, MAXIMUM_FSIZE),
              "byte_idx_pairs": byte_idx_pairs}

    logging.info(f"File duplicate scan Started: " +
                 UTIL.local_datetime_str_iso8601())
    
    logging.info(f"Search Directories: " + str(search_dirs))
    
    scan_groups = local_duplicate_scan(params)

    logging.info(f"File duplicate scan Finished: " +
                 UTIL.local_datetime_str_iso8601())
# )


# Directories for personal(armagansalman) experiments:
#DIRS = PData.DIRS
#dirs = DIRS["dirs_20"]
#_search_dirs = DIRS["dirs_20"]
#_search_dirs = ["D:\\"]
#_search_dirs = ["/home/genel/"]
#_dirs = [ "C:\\" ]
#_search_dirs = [ "/media/genel/9A4277A5427784B3/" ]
#_search_dirs = [ "/media/genel/Bare-Data/" ]
