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
    charts = {"cpu": {"arg": "-P ALL", "multiple": True, "datasets": {},
                      "labels": [], "hidden": ['%steal', '%idle']},
              "disk": {"arg": "-d", "multiple": True, "datasets": {},
                       "labels": [], "hidden": ['tps', 'dtps', 'bread/s', 'bwrtn/s', 'bdscd/s']},  # noqa E501
              "hugepages": {"arg": "-H", "multiple": True, "datasets": {},
                            "labels": [], "hidden": []},
              "inodes": {"arg": "-v", "multiple": False, "datasets": {},
                        "labels": [], "hidden": []},
              "io": {"arg": "-b", "multiple": False, "datasets": {},
                     "labels": [], "hidden": []},
              "interrrupts": {"arg": "-I", "multiple": False, "datasets": {},
                              "labels": [], "hidden": []},
              "load": {"arg": "-q LOAD", "multiple": False, "datasets": {},
                       "labels": [], "hidden": ['runq-sz', 'plist-sz', 'blocked']},  # noqa E501
              "memory": {"arg": "-r ALL", "multiple": False, "datasets": {}, "labels": [],  # noqa E501
                         "hidden": ['kbmemfree', 'kbavail', 'kbmemused',
                                    'kbbuffers', 'kbcached', 'kbcommit',
                                    '%commit', 'kbactive', 'kbinact',
                                    'kbdirty', 'kbanonpg', 'kbslab',
                                    'kbkstack', 'kbpgtbl', 'kbvmused']},
              "mount": {"arg": "-F", "multiple": True, "datasets": {},
                        "labels": [], "hidden": []},
              "netdevice": {"arg": "-n DEV", "multiple": True, "datasets": {},
                          "labels": [], "hidden": ['rxpck/s', 'txpck/s', 'rxcmp/s', 'txcmp/s', 'rxmcst/s', '%ifutil']},  # noqa E501
              "netdevicee": {"arg": "-n EDEV", "multiple": True, "datasets": {},
                             "labels": [], "hidden": []},
              "netfiberchannel": {"arg": "-n FC", "multiple": True, "datasets": {},
                                  "labels": [], "hidden": []},
              "neticmp": {"arg": "-n ICMP", "multiple": True, "datasets": {},
                          "labels": [], "hidden": []},
              "neticmpe": {"arg": "-n EICMP", "multiple": True, "datasets": {},
                           "labels": [], "hidden": []},
              "netip": {"arg": "-n IP", "multiple": True, "datasets": {},
                        "labels": [], "hidden": []},
              "netipe": {"arg": "-n EIP", "multiple": True, "datasets": {},
                         "labels": [], "hidden": []},
              "netip6": {"arg": "-n IP6", "multiple": False, "datasets": {},
                         "labels": [], "hidden": []},
              "netip6e": {"arg": "-n EIP6", "multiple": False, "datasets": {},
                          "labels": [], "hidden": []},
              "netnfs": {"arg": "-n NFS", "multiple": False, "datasets": {},
                         "labels": [], "hidden": []},
              "netsock": {"arg": "-n SOCK", "multiple": False, "datasets": {},
                          "labels": [], "hidden": []},
              "netsock6": {"arg": "-n SOCK6", "multiple": False, "datasets": {},
                           "labels": [], "hidden": []},
              "nettcp": {"arg": "-n TCP", "multiple": True, "datasets": {},
                         "labels": [], "hidden": []},
              "nettcpe": {"arg": "-n ETCP", "multiple": True, "datasets": {},
                          "labels": [], "hidden": []},
              "netudp": {"arg": "-n UDP", "multiple": True, "datasets": {},
                         "labels": [], "hidden": []},
              "netudp6": {"arg": "-n UDP6", "multiple": True, "datasets": {},
                          "labels": [], "hidden": []},
              "paging": {"arg": "-B", "multiple": False, "datasets": {},
                         "labels": [], "hidden": ['fault/s', 'majflt/s', 'pgfree/s', 'pgscank/s', 'pgscand/s', 'pgsteal/s', '%vmeff']},  # noqa E501
              "powermanagement": {"arg": "-m ALL", "multiple": True,
                                  "datasets": {}, "labels": [], "hidden": []},  # noqa E501
              "swap": {"arg": "-S", "multiple": False, "datasets": {},
                       "labels": [], "hidden": ['kbswpfree', 'kbswpused', 'kbswpcad', '%swpcad']},  # noqa E501
              "tasks": {"arg": "-w", "multiple": False, "datasets": {},
                        "labels": [], "hidden": []},
              "tty": {"arg": "-y", "multiple": False, "datasets": {},
                      "labels": [], "hidden": []},
              }
    colors = ['255, 99, 132',
              '255, 159, 64',
              '255, 205, 86',
              '75, 192, 192',
              '54, 162, 235',
              '153, 102, 255',
              '201, 203, 207',
              '153, 24, 44',
              '54, 157, 72',
              '75, 89, 123',
              '255, 22, 237',
              '99, 215, 99',
              '199, 215, 29',
              '68, 15, 229',
              '88, 115, 67',
              '149, 245, 44']

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
