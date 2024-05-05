### sarcharts
Reads [sysstat](https://sysstat.github.io/) `sa*` files from INPUTDIR and generates Charts for the last 7 days (by default). Charts can be zoomed in and out.

### Requirements
`sadf` command is needed to read sar files. Hence [sysstat](https://sysstat.github.io/) package is required.

### Usage
~~~
Usage: sarcharts.py [Options] [sarfilespath] [sarfilespath] [sarfilespath]...
  Options:
    [-d|--debug]: Debug level [D,I,W,E]. Default Warning.
    [-f|--from] DATE: From date (2023-12-01 23:01:00).
    [-h|--help]: Show help.
    [-o|--outputpath] Path to put output files. Default is `./sarcharts`.
    [-t|--to] DATE: To date (2023-12-01 23:01:00).
  Arguments:
    [sarfilespath/s]: Multiple paths and patterns allowed. Default is `./sa??`.

  Examples:
    - sarcharts.py /var/log/sa/sa*
    - sarcharts.py /tmp/previousmonth/sa?? sa08 sa09 sa1?
~~~

| Example Chart |
| --- |
| ![](/doc/sarcharts.png) |

