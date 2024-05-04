### sarcharts
Reads [sysstat](https://sysstat.github.io/) `sa*` files from INPUTDIR and generates Charts for the last 7 days (by default). Charts can be zoomed in and out.

### Requirements
`sadf` command is needed to read sar files. Hence [sysstat](https://sysstat.github.io/) package is required.

### Usage
~~~
Usage: sarcharts.py [Options] [INPUTDIR] [OUTPUTDIR]
  Options:
    [-d|--debug]: Debug level [D,I,W,E]. Default Warning.
    [-f|--from] DATE: From date (2023-12-01 23:01:00).
    [-h|--help]: Show help.
    [-l|--last] N: Show last N days. Default is 7 days.
    [-t|--to] DATE: To date (2023-12-01 23:01:00).
  Arguments:
    [INPUTDIR]: Default is current path.
    [OUTPUTDIR]: Default is current path plus '/sarcharts/'.
~~~

| Example Chart |
| --- |
| ![](/doc/sarcharts.png) |

