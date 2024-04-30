### sarcharts
Generates Charts from sar files using [Chart.js](https://www.chartjs.org/). It reads files from INPUT folder using next command `ls -1tr INPUTDIR | grep -E 'sa[0-9][0-9].*'`
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

