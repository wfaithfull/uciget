uciget
======

Download datasets from [UCI repository](http://archive.ics.uci.edu/ml/) using regular expressions

###usage

`python uciget.py ^[Aa].* -d C:\Users\Will\Documents\Data`

Downloads all datasets that start with A or a to the specified folder

`python uciget.py -c Classification -d C:\Users\Will\Documents\Data`

Downloads all datasets whose default task is classification to the specified folder

```
usage: uciget.py [-h] [-n NAME [NAME ...]] [-d SAVEDIR] [-c CATEGORY]

Get datasets from UCI repository.

optional arguments:
  -h, --help          show this help message and exit
  -n NAME [NAME ...]  the name of the dataset [REGEX]
  -d SAVEDIR          directory to save downloaded files
  -c CATEGORY         category (default task) [REGEX]
```


