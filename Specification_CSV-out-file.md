# CSV Output File Specification

- First element of every row holds type information for that row.
- Characters of type information must be uppercase.
- Metadata of a CSV file is always at the start of the file.
- CSV metadata type signature = [CSV INFO]
- CSV encoding is utf-8 by default.
- CSV delimiter is ; by default.
- CSV quotechar is " by default.

## Version 1

### 2022-09-25

[INFO] type signature is any extra information about the scan belonging that CSV output.
[GID-FID-PATH] type row has 2 ints. First one (left) is group id, second is file id. Last
value is file path.
