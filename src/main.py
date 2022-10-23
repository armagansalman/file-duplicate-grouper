import logging

import opaque_core as OC
import constants as CONST

import maybe as Maybe
import util as UTIL


BYTE = CONST.BYTE
KB = CONST.KB
MB = CONST.MB


def local_duplicate_scan(args):
#(
	return OC.main_11( args )
#)


if __name__ == "__main__":
#(
	log_name = "LOG_duplicate-find_" + UTIL.local_datetime_str_iso8601() + ".txt"
	
	logging.basicConfig(filename= log_name \
		, level= logging.INFO \
		, filemode= 'a' \
		, format= '[ %(levelname)s ]~~~%(asctime)s~~~%(message)s')
	# '%(levelname)s ~ %(name)s ~ %(asctime)s ~ %(message)s' name is root by default.
	
	#dirs = DIRS["dirs_20"]

	search_dirs = [ "D:\\" ]

	#_dirs = [ "C:\\" ]

	SMALLEST_FSIZE = 500 * KB

	byte_idx_pairs = [ 
						(0, 256 * BYTE) \
						,(0, 2 * KB) \
						,(0, 64 * KB) \
						,(64 * KB, 320 * KB) \
					 ]
	#

	params = {"dirs": search_dirs , "SMALLEST_FSIZE": SMALLEST_FSIZE \
		, "byte_idx_pairs": byte_idx_pairs}

	logging.info(f"File duplicate scan Started: " + UTIL.local_datetime_str_iso8601())

	scan_groups = local_duplicate_scan(params)
	
	logging.info(f"File duplicate scan Finished: " + UTIL.local_datetime_str_iso8601())
#)

