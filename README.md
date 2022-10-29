# file-duplicate-grouper

Finds local file duplicates. It is not guaranteed that all files in a reported group are the same.

## Usage

* In main.py, put directory paths (as a list) in variable 'search_dirs'.

* To run on Linux (in command line): python3 main.py

* To run on Windows (in command line): py main.py

* (main.py) 'MINIMUM_FSIZE' and 'MAXIMUM_FSIZE' can also be changed according to your needs. Use None for any of the FSIZE limits if you don't want to filter for that size.

* (main.py) 'byte_idx_pairs' values (both inclusive) for file slice indices were experimentally chosen for speed. Other slice indices can be appended to 'byte_idx_pairs' for better accuracy (it will slow the scan down).

* Results will be in a .csv file which start with 'Result_duplicates'.

* There will be a log file starting with 'LOG_duplicate-find' which has some information about the scan and errors if there were any.

* Start and End date-time values (similar to iso-8601 format) will be printed to stdout.
