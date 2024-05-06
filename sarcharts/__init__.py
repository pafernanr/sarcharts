import datetime
import getopt
import os
import sys

from pathlib import Path
import shutil
import webbrowser

from sarcharts.lib.chartconf import ChartConf
from sarcharts.lib.chartjs import ChartJS
from sarcharts.lib.sadf import Sadf
from sarcharts.lib import util


class SarCharts:
    C = ChartConf()

    def __init__(self):
        options, remainder = getopt.getopt(sys.argv[1:], 'd:f:ho:t:',
                                           ['debug=', 'from=', 'help',
                                            'outputpath=', 'to='])
        for opt, arg in options:
            if opt in ['-d', '--debug']:
                self.C.debuglevel = arg
            elif opt in ['-f', '--from']:
                if util.is_valid_date(self, arg):
                    self.C.dfrom = (
                        datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
                    )
            elif opt in ['-h', '--help']:
                self.show_help()
                sys.exit()
            elif opt in ['-o', '--outputpath']:
                if not Path(arg).is_dir():
                    self.show_help("provided outputpath '"
                                   + self.C.outputpath
                                   + "' is not a folder or doesn't exists")
                    sys.exit(1)
                self.C.outputpath = arg
            elif opt in ['-t', '--to']:
                if util.is_valid_date(self, arg):
                    self.C.dto = (
                        datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
                    )
        # check if '--to' and '--from' where properly provided
        if self.C.dto and not self.C.dfrom:
            util.debug(self.C.debuglevel, 'E',
                       "'--from' used but no '--to' provided.")
        if self.C.dfrom and not self.C.dto:
            util.debug(self.C.debuglevel, 'E',
                       "'--to' used but no '--from' provided.")
        # get sarfilespaths
        if len(remainder) > 0:
            self.sarfilespaths = []
            for path in remainder:
                self.sarfilespaths.append(path)
        # create required files on outputpath
        self.C.outputpath = self.C.outputpath + "/sarcharts"
        if os.path.exists(self.C.outputpath):
            shutil.rmtree(self.C.outputpath)
        os.makedirs(self.C.outputpath + "/sar")
        shutil.copytree(os.path.dirname(
                        os.path.realpath(__file__)) + "/html",
                        self.C.outputpath + "/html")

    # pylint: disable=line-too-long
    def show_help(self, errmsg=""):
        print("Usage: sarcharts.py"
              + " [Options] [sarfilespath] [sarfilespath] [sarfilespath]..."
              "\n  Options:"
              "\n    [-d|--debug]: Debug level [D,I,W,E]. Default Warning."  # noqa E501
              "\n    [-f|--from] DATE: From date (2023-12-01 23:01:00)."
              "\n    [-h|--help]: Show help."
              "\n    [-o|--outputpath] Path to put output files. Default is `./sarcharts`."  # noqa E501
              "\n    [-t|--to] DATE: To date (2023-12-01 23:01:00)."
              "\n  Arguments:"
              "\n    [sarfilespath/s]: Multiple paths and patterns allowed. Default is `./sa??`."  # noqa E501
              "\n"
              "\n  Examples:"
              "\n    - sarcharts.py /var/log/sa/sa*"
              "\n    - sarcharts.py /tmp/previousmonth/sa?? sa08 sa09 sa1?")
        if errmsg != "":
            print("\nERROR: " + errmsg)

    def main(self):
        sarfiles = util.get_filelist(self.sarfilespaths)
        util.debug(self.C.debuglevel, 'D', "sarfiles: " + str(sarfiles))
        chartinfo = Sadf().sar_to_chartjs(
            self.C.debuglevel, sarfiles, self.C.outputpath + "/sar",
            self.C.charts, self.C.dfrom, self.C.dto
            )
        ChartJS().write_files(
            self.C.charts, self.C.colors, chartinfo, self.C.outputpath
            )
        webbrowser.open(self.C.outputpath + "/cpu.html", 0, True)


SarCharts().main()
