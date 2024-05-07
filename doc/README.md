### SarCharts
SarCharts gets [sysstat](https://sysstat.github.io/) files from provided `sarfilespaths` and generates dynamic HTML Charts.

### Requirements
`sadf` command is needed to read sar files. Hence [sysstat](https://sysstat.github.io/) package is required.

### Usage
~~~
usage: sarcharts.py [-h] [-d {D,I,W,E}] [-f FROMDATE] [-o OUTPUTPATH] [-t TODATE] [sarfilespaths ...]

SarCharts gets "sysstat" files from provided `sarfilespaths` and generates dynamic HTML Charts.

positional arguments:
  sarfilespaths         `sa` file/s to parse. Default: `./sa??`.

options:
  -h, --help            show this help message and exit
  -d {D,I,W,E}, --debug {D,I,W,E}
                        Set debug level. Default `W`.
  -f FROMDATE, --fromdate FROMDATE
                        Read metric starting on this date.
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Path to put output files. Default `./sarcharts`.
  -t TODATE, --todate TODATE
                        Discard metrics after this date.
~~~

| Example Chart |
| --- |
| ![](/doc/sarcharts.png) |

