# file-duplicate-grouper
Finds local file duplicates. It is not guaranteed that all files in a reported group are the same.

## Use
In main.py, put directory paths in variable 'search_dirs'. 'SMALLEST_FSIZE' can be changed also according to your needs. 'byte_idx_pairs' values for file slice indices were experimentally chosen for speed. It's last slice can be widened for better accuracy. Results will be in a file that starts with 'op-core_main-11'.
