### SarCharts
SarCharts gets [sysstat](https://sysstat.github.io/) files from provided `sarfilespaths` and generates dynamic HTML Charts.

### Requirements
`sadf` command is needed to read sar files. Hence [sysstat](https://sysstat.github.io/) package is required.

### Installation
`pip install sarcharts`

### Usage
~~~
usage: sarcharts [-h] [-d {D,I,W,E}] [-e EVENTFILE] [-f FROMDATE] [-o OUTPUTPATH] [-t TODATE] [-q] [sarfilespaths ...]

SarCharts gets "sysstat" files from provided `sarfilespaths` and generates dynamic HTML Charts.

positional arguments:
  sarfilespaths         `sa` file/s to parse. Default: `./sa??`.

optional arguments:
  -h, --help            show this help message and exit
  -d {D,I,W,E}, --debug {D,I,W,E}
                        Set debug level. Default `W`.
  -e EVENTFILE, --eventfile EVENTFILE
                        Add events csv file. Header: # date;hostname;event_name;event_description
  -f FROMDATE, --fromdate FROMDATE
                        Include metrics from this date.
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Path to put output files. Default `./sarcharts`.
  -t TODATE, --todate TODATE
                        Discard metrics after this date.
  -q, --quiet           Don't show progress.
~~~

| Example Chart |
| --- |
| ![](/doc/sarcharts.png) |

