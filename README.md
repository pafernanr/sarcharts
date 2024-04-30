### sarcharts
Generates Charts from sar files using [Chart.js](https://www.chartjs.org/)

Usage: sarcharts.py [Options] [INPUTDIR] [OUTPUTDIR]
  Options:
    [-d|--debug]: Debug level [D,I,W,E]. Default Warning.
    [-h|--help]: Show help.
    [-l|--limit] N: Limit to last N days. Default is 7 days.
    [-q|--quiet]: Quiet. Don't show progress bar.
  Arguments:
    [INPUTDIR]: Default is current path.
    [OUTPUTDIR]: Default is current path plus '/sarcharts/'.

