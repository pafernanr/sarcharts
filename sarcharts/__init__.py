from sarcharts.lib.util import debug, is_valid_date, get_sarfiles, exec_command, in_date_range  # noqa E501
import datetime
import getopt
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
import re
import shutil
import sys
import webbrowser


class SarCharts:
    inputdir = "."
    outputdir = "./"
    debuglevel = "W"  # [D, I, W, E]
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
              "netdevicee": {"arg": "-n EDEV", "multiple": True, "datasets": {},  # noqa E501
                             "labels": [], "hidden": []},
              "netfiberchannel": {"arg": "-n FC", "multiple": True, "datasets": {},  # noqa E501
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
              "netsock6": {"arg": "-n SOCK6", "multiple": False, "datasets": {},  # noqa E501
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

    def __init__(self):
        options, remainder = getopt.getopt(sys.argv[1:], 'd:f:hl:t:',
                                           ['debug=', 'from=', 'help',
                                            'last=', 'to='])
        for opt, arg in options:
            if opt == '-d' or opt == '--debug':
                self.debug = arg
            elif opt == '-f' or opt == '--from':
                if is_valid_date(self, arg):
                    self.dfrom = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')  # noqa E501
            elif opt == '-h' or opt == '--help':
                self.show_help()
                exit()
            elif opt == '-l' or opt == '--last':
                self.last = int(arg)
            elif opt == '-t' or opt == '--to':
                if is_valid_date(self, arg):
                    self.dto = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')  # noqa E501

        if self.dto and not self.dfrom:
            debug(self.debuglevel, 'E',
                  "'--from' used but no '--to' provided.")
        if self.dfrom and not self.dto:
            debug(self.debuglevel, 'E',
                  "'--to' used but no '--from' provided.")

        if len(remainder) > 0:
            if remainder[0].endswith("/"):
                remainder[0] = remainder[0][:-1]
            self.inputdir = remainder[0]
            if not Path(self.inputdir).is_dir():
                self.show_help("provided sosreport '" + self.inputdir
                               + "' is not a folder")
                exit(1)
            if len(remainder) == 2:
                self.outputdir = remainder[1]
                if not Path(self.outputdir).is_dir():
                    self.show_help("provided outputdir "
                                   + self.outputdir
                                   + " is not a folder or doesn't exists")
                    exit(1)
            elif len(remainder) > 2:
                self.show_help("Wrong parameters count")
                exit(1)

        self.outputdir = str(self.outputdir + "sarcharts/")

        for d in ["/sar", "/html"]:
            if os.path.exists(self.outputdir + d):
                shutil.rmtree(self.outputdir + d)

        os.makedirs(self.outputdir + "/sar")
        shutil.copytree(os.path.dirname(
                        os.path.realpath(__file__)) + "/html",
                        self.outputdir + "/html")

    def show_help(self, errmsg=""):
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

    def output(self):
        sarfiles = get_sarfiles(self)
        showheader = ""
        notavailable = []
        debug(self.debuglevel, 'W', "Getting data from sar files.")
        for inputfile in sarfiles[-self.last:]:
            for k, v in self.charts.items():
                csvfile = self.outputdir + "sar/" + k + ".csv"
                [stdout, stderr] = exec_command(self.debuglevel, f"sadf -dt {inputfile} -- {v['arg']}"  # noqa E501
                                                     + f" {showheader} >> {csvfile}")  # noqa E501
                if stderr:
                    if "Requested activities not available" in stderr and k not in notavailable:  # noqa E501
                        notavailable.append(k)
            showheader = "| grep -vE '^#'"

        hostname = ""
        firstdate = ""
        lastdate = ""
        # convert csv to chartjs compatible Lists
        debug(self.debuglevel, 'W', "Generating Charts.")
        for k, v in self.charts.items():
            csvfile = self.outputdir + "sar/" + k + ".csv"
            with open(csvfile) as f:
                line = f.readline().strip()
                headers = line[2:].split(";")
                # insert fake item for non multiple charts
                if not self.charts[k]['multiple']:
                    headers.insert(3, "")
                for line in f:
                    debug(self.debuglevel, 'D', csvfile + ": " + line.strip())
                    if "LINUX-RESTART" in line or re.match(r"^#", line):
                        continue
                    fields = line.strip().split(";")
                    if in_date_range(self, fields[2]):
                        if firstdate == "":
                            firstdate = line.split(";")[2]
                        # insert fake item for non multiple charts
                        if not self.charts[k]['multiple']:
                            fields.insert(3, "")
                        if fields[2] not in self.charts[k]['labels']:
                            self.charts[k]['labels'].append(fields[2])  # date
                        item = fields[3].replace("-", "_")
                        if item == "_1":
                            item = "ALL"
                        if item not in self.charts[k]['datasets'].keys():
                            self.charts[k]['datasets'][item] = []
                            for h in headers[4:]:
                                self.charts[k]['datasets'][item].append({"label": h, "values": []})  # noqa E501

                        for i in range(len(fields[4:])):
                            self.charts[k]['datasets'][item][i]['values'].append(fields[i+4])  # noqa E501
                if line != "":
                    hostname = fields[0]
                    lastdate = fields[2]

        # write output Charts
        for chart, details in self.charts.items():
            context = {
                        "chart": chart,
                        "details": details,
                        "pages": self.charts.keys(),
                        "colors": self.colors,
                        "notavailable": notavailable,
                        "hostname": hostname,
                        "firstdate": firstdate,
                        "lastdate": lastdate
                    }
            parent = os.path.dirname(os.path.realpath(__file__)) + "/templates/"  # noqa E501
            environment = Environment(loader=FileSystemLoader(parent))
            template = environment.get_template("chart.html")
            with open(self.outputdir + f"/{chart}.html", mode="w", encoding="utf-8") as results:  # noqa E501
                results.write(template.render(context))

        webbrowser.open(self.outputdir + "/cpu.html", 0, True)


SarCharts().output()
