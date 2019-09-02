# FW-backend
# JSON Merge
## Usage
```main.py [-h] [-i IPREFIX] [-o OPREFIX] [-m MAX] inputdir outputdir key```
Where:
- **IPREFIX** is the prefix of input JSON files [Default: input]
- **OPREFIX** is the prefix for ouput merged JSON files [Default: merged]
- **MAX** is the maximum size of each merged JSON file in bytes *[Default: 1MB]

## Program
The program maintains the order of the the input elements in the merged files. This may result in creating more number of output files than required. But it is a trade-off to reduce program time and preserve the order.

### Algorithm Complexity
**O(n)** where n is the total number of array items in all files combined.

### Platform
Linux, Windows, OS X (not tested)

### Language
Python3

### Error Handling
- Check if input path contains any JSON files with the given prefix
- Check if the input files are valid JSON. Skip files that are not valid.
- Check if the JSON file contains the required key. Skip file if key is not present.
- Check if any individual record on its own, exceeds the maximum allowed size. Skip record if so.

