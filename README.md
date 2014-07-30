uciget
======

Download datasets from [UCI repository](http://archive.ics.uci.edu/ml/) using regular expressions

###usage

`python uciget.py ^[Aa].* -d C:\Users\Will\Documents\Data`

Downloads all datasets that start with A or a to the specified folder

```
usage: uciget.py [-h] [-d SAVEDIR] D [D ...]

Get datasets from UCI repository

positional arguments:
  D           the name of the dataset [REGEX]
  
optional arguments:
  -h, --help  show this help message and exit
  -d SAVEDIR  directory to save downloaded files
```


