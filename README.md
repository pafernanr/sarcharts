### SarCharts
SarCharts gets [sysstat](https://sysstat.github.io/) files from provided `sarfilespaths` and generates dynamic HTML Charts.

**[Live Demo](https://pafernanr.github.io/sarcharts/)**

### Requirements
`sadf` command is needed to read sar files. Hence [sysstat](https://sysstat.github.io/) package is required.

### Installation
`pip install sarcharts`

### Usage
~~~
usage: sarcharts [-h] [-d {D,I,W,E}] [-e EVENTFILE] [-f FROMDATE] [-m METRICFILE] [-o OUTPUTPATH] [-t TODATE] [-q] [sarfilespaths ...]

SarCharts gets "sysstat" files from provided `sarfilespaths` and generates dynamic HTML Charts.

positional arguments:
  sarfilespaths         `sa` file/s to parse. Default: `./sa??`.

optional arguments:
  -h, --help            show this help message and exit
  -d {D,I,W,E}, --debug {D,I,W,E}
                        Set debug level. Default `W`.
  -e EVENTFILE, --eventfile EVENTFILE
                        Add events csv file. Header: # date;hostname;eventname;eventdescription
  -f FROMDATE, --fromdate FROMDATE
                        Include metrics/events from this date.
  -m METRICFILE, --metricfile METRICFILE
                        Add metrics csv file. Header: # date;hostname;metricname;metricvalue
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Path to put output files. Default `./sarcharts`.
  -t TODATE, --todate TODATE
                        Include metrics/events before this date.
  -q, --quiet           Don't show progress.
~~~

| Example Chart |
| --- |
| ![](/doc/sarcharts.png) |

