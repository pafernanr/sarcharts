### sarcharts
Generates Charts from sar files using [Chart.js](https://www.chartjs.org/). It reads `sa` files from INPUT folder and generates Charts for the last 7 days (by default).

### Requirements
`sadf` command is needed to read sar files. Hence sysstat package is required.

### Usage
~~~
Usage: sarcharts.py [Options] [INPUTDIR] [OUTPUTDIR]
  Options:
    [-d|--debug]: Debug level [D,I,W,E]. Default Warning.
    [-h|--help]: Show help.
    [-l|--limit] N: Limit to last N days. Default is 7 days.
  Arguments:
    [INPUTDIR]: Default is current path.
    [OUTPUTDIR]: Default is current path plus '/sarcharts/'.
~~~

