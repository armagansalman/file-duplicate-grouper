import opaque_core as OC
import constants as CONST


BYTE = CONST.BYTE
KB = CONST.KB
MB = CONST.MB


def local_duplicate_scan(args):
#(
    return OC.main_11( args )
#)


if __name__ == "__main__":
#(
    # TODO(armagans): csv output path should be decided by user.
    
    dirs = ["/home/genel"] # 125650 items, totalling 52,5 GiB (56.358.510.573 bytes)
    #dirs = ["/media/genel/Bare-Data/"] # 34735 items, totalling 67,6 GiB (72.553.152.052 bytes)
    #dirs = ["/media/genel/9A4277A5427784B3/"] # 513816 items, totalling 88,4 GiB (94.866.674.987 bytes)
    
    #dirs = DIRS["dirs_20"]
    
    SMALLEST_FSIZE = 500 * KB
    
    byte_idx_pairs = [ 
                        (0, 256 * BYTE) \
                        ,(0, 2 * KB) \
                        ,(0, 64 * KB) \
                        ,(0, 384 * KB) \
                     ]
    #
    
    params = {"dirs": dirs , "SMALLEST_FSIZE": SMALLEST_FSIZE \
        , "byte_idx_pairs": byte_idx_pairs}
    
    scan_groups = local_duplicate_scan(params)
#)
