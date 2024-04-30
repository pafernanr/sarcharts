'''
Author: Pablo Fernández Rodríguez
Web: https://github.com/pafernanr/dynflowparser
Licence: GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
'''
import datetime
import getopt
import os
from pathlib import Path
import shutil
import sys
from lib.util import Util


class Conf:
    inputdir = "."
    outputdir = "./"
    debug = "W"  # [D, I, W, E]
    dfrom = False
    last = 7
    dto = False
    quiet = False
    charts = {"cpu": {"arg": "-u", "datasets": [], "labels": [],
                      "hidden": ['CPU', '%steal', '%idle']},
              "memory": {"arg": "-r", "datasets": [], "labels": [],
                         "hidden": ['kbmemfree', 'kbavail', 'kbmemused',
                                    'kbbuffers', 'kbcached', 'kbcommit',
                                    '%commit', 'kbactive', 'kbinact',
                                    'kbdirty']},
              "swap": {"arg": "-S", "datasets": [], "labels": [],
                       "hidden": ['kbswpfree', 'kbswpused',
                                  'kbswpcad', '%swpcad']},
              "memorypaging": {"arg": "-B", "datasets": [], "labels": [],
                               "hidden": ['fault/s', 'majflt/s', 'pgfree/s',
                                          'pgscank/s', 'pgscand/s', 'pgsteal/s', 
                                          '%vmeff']},
              "load": {"arg": "-q", "datasets": [], "labels": [],
                       "hidden": ['runq-sz', 'plist-sz', 'blocked']},
              "network": {"arg": "-n DEV", "datasets": [], "labels": [],
                          "hidden": []},
              "io": {"arg": "-b", "datasets": [], "labels": [],
                     "hidden": []}
              }
    colors = ['255, 99, 132',
              '255, 159, 64',
              '255, 205, 86',
              '75, 192, 192',
              '54, 162, 235',
              '153, 102, 255',
              '201, 203, 207',
              '201, 203, 207',
              '201, 203, 207',
              '201, 203, 207',
              '201, 203, 207',
              '201, 203, 207']

    def show_help(errmsg=""):
        print("Usage: sarcharts.py"
              + " [Options] [INPUTDIR] [OUTPUTDIR]"
              "\n  Options:"
              "\n    [-d|--debug]: Debug level [D,I,W,E]. Default Warning."  # noqa E501
              "\n    [-f|--from] DATE: From date (2023-12-01 23:01:00)."
              "\n    [-h|--help]: Show help."
              "\n    [-l|--last] N: Show last N days. Default is 7 days."
              "\n    [-t|--to] DATE: To date (2023-12-01 23:01:00)."
              "\n  Arguments:"
              "\n    [INPUTDIR]: Default is current path."
              "\n    [OUTPUTDIR]: Default is current path plus '/sarcharts/'.")  # noqa E501
        if errmsg != "":
            print("\nERROR: " + errmsg)
            sys.exit(1)
        else:
            sys.exit(0)

    def get_opts():
        try:
            options, remainder = getopt.getopt(sys.argv[1:], 'd:f:hl:t:',
                                               ['debug=', 'from=', 'help',
                                                'last=', 'to='])
            for opt, arg in options:
                if opt == '-d' or opt == '--debug':
                    Conf.debug = arg
                elif opt == '-f' or opt == '--from':
                    if Util.is_valid_date(Conf, arg):
                        Conf.dfrom = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')  # noqa E501
                elif opt == '-h' or opt == '--help':
                    Conf.show_help()
                elif opt == '-l' or opt == '--last':
                    Conf.last = int(arg)
                elif opt == '-t' or opt == '--to':
                    if Util.is_valid_date(Conf, arg):
                        Conf.dto = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')  # noqa E501

            if Conf.dto and not Conf.dfrom:
                Util.debug(Conf, 'E', "'--from' used but no '--to' provided.")
            if Conf.dfrom and not Conf.dto:
                Util.debug(Conf, 'E', "'--to' used but no '--from' provided.")

            if len(remainder) > 0:
                if remainder[0].endswith("/"):
                    remainder[0] = remainder[0][:-1]
                Conf.inputdir = remainder[0]
                if not Path(Conf.inputdir).is_dir():
                    Conf.show_help("provided sosreport '" + Conf.inputdir
                                   + "' is not a folder")
                if len(remainder) == 2:
                    Conf.outputdir = remainder[1]
                    if not Path(Conf.outputdir).is_dir():
                        Conf.show_help("provided outputdir "
                                       + Conf.outputdir
                                       + " is not a folder or doesn't exists")
                elif len(remainder) > 2:
                    Conf.show_help("Wrong parameters count")

            Conf.outputdir = str(Conf.outputdir + "sarcharts/")

            if os.path.exists(Conf.outputdir):
                for d in ["/sar", "/html"]:
                    shutil.rmtree(Conf.outputdir + d)

            os.makedirs(Conf.outputdir + "/sar")
            shutil.copytree(os.path.dirname(
                        os.path.realpath(__file__)) + "/../html",
                        Conf.outputdir + "/html")

        except Exception as e:
            print(e)
