import datetime
import getopt
import os
import re
import sys

import jinja2
from pathlib import Path
import shutil
import webbrowser

from sarcharts.lib import util


class SarCharts:
    sarfilespaths = ["."]
    outputpath = "."
    debuglevel = "W"  # [D, I, W, E]
    dfrom = False
    dto = False
    quiet = False
    charts = {
        "cpu": {
            "arg": "-P ALL",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": ["%steal", "%idle"],
        },
        "disk": {
            "arg": "-d",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": ["tps", "dtps", "bread/s", "bwrtn/s", "bdscd/s"],
        },  # noqa E501
        "hugepages": {
            "arg": "-H",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "inodes": {
            "arg": "-v",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "io": {
            "arg": "-b",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "interrrupts": {
            "arg": "-I",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "load": {
            "arg": "-q LOAD",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": ["runq-sz", "plist-sz", "blocked"],
        },  # noqa E501
        "memory": {
            "arg": "-r ALL",
            "multiple": False,
            "datasets": {},
            "labels": [],  # noqa E501
            "hidden": [
                "kbmemfree",
                "kbavail",
                "kbmemused",
                "kbbuffers",
                "kbcached",
                "kbcommit",
                "%commit",
                "kbactive",
                "kbinact",
                "kbdirty",
                "kbanonpg",
                "kbslab",
                "kbkstack",
                "kbpgtbl",
                "kbvmused",
            ],
        },
        "mount": {
            "arg": "-F",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netdevice": {
            "arg": "-n DEV",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [
                "rxpck/s",
                "txpck/s",
                "rxcmp/s",
                "txcmp/s",
                "rxmcst/s",
                "%ifutil",
            ],
        },  # noqa E501
        "netdevicee": {
            "arg": "-n EDEV",
            "multiple": True,
            "datasets": {},  # noqa E501
            "labels": [],
            "hidden": [],
        },
        "netfiberchannel": {
            "arg": "-n FC",
            "multiple": True,
            "datasets": {},  # noqa E501
            "labels": [],
            "hidden": [],
        },
        "neticmp": {
            "arg": "-n ICMP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "neticmpe": {
            "arg": "-n EICMP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netip": {
            "arg": "-n IP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netipe": {
            "arg": "-n EIP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netip6": {
            "arg": "-n IP6",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netip6e": {
            "arg": "-n EIP6",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netnfs": {
            "arg": "-n NFS",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netsock": {
            "arg": "-n SOCK",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netsock6": {
            "arg": "-n SOCK6",
            "multiple": False,
            "datasets": {},  # noqa E501
            "labels": [],
            "hidden": [],
        },
        "nettcp": {
            "arg": "-n TCP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "nettcpe": {
            "arg": "-n ETCP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netudp": {
            "arg": "-n UDP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "netudp6": {
            "arg": "-n UDP6",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "paging": {
            "arg": "-B",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [
                "fault/s",
                "majflt/s",
                "pgfree/s",
                "pgscank/s",
                "pgscand/s",
                "pgsteal/s",
                "%vmeff",
            ],
        },  # noqa E501
        "powermanagement": {
            "arg": "-m ALL",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },  # noqa E501
        "swap": {
            "arg": "-S",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": ["kbswpfree", "kbswpused", "kbswpcad", "%swpcad"],
        },  # noqa E501
        "tasks": {
            "arg": "-w",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
        "tty": {
            "arg": "-y",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [],
        },
    }
    colors = [
        "255, 99, 132",
        "255, 159, 64",
        "255, 205, 86",
        "75, 192, 192",
        "54, 162, 235",
        "153, 102, 255",
        "201, 203, 207",
        "153, 24, 44",
        "54, 157, 72",
        "75, 89, 123",
        "255, 22, 237",
        "99, 215, 99",
        "199, 215, 29",
        "68, 15, 229",
        "88, 115, 67",
        "149, 245, 44",
    ]

    def __init__(self):
        options, remainder = getopt.getopt(
            sys.argv[1:],
            "d:f:ho:t:",
            ["debug=", "from=", "help", "outputpath=", "to="],
        )
        for opt, arg in options:
            if opt == "-d" or opt == "--debug":
                self.debuglevel = arg
            elif opt == "-f" or opt == "--from":
                if util.is_valid_date(self, arg):
                    self.dfrom = datetime.datetime.strptime(
                        arg, "%Y-%m-%d %H:%M:%S"
                    )
            elif opt == "-h" or opt == "--help":
                self.show_help()
                exit()
            elif opt == "-o" or opt == "--outputpath":
                if not Path(arg).is_dir():
                    self.show_help(
                        "provided outputpath '"
                        + self.outputpath
                        + "' is not a folder or doesn't exists"
                    )
                    exit(1)
                self.outputpath = str(arg + "/sarcharts")
            elif opt == "-t" or opt == "--to":
                if util.is_valid_date(self, arg):
                    self.dto = datetime.datetime.strptime(
                        arg, "%Y-%m-%d %H:%M:%S"
                    )
        # check if '--to' and '--from' where properly provided
        if self.dto and not self.dfrom:
            util.debug(
                self.debuglevel, "E", "'--from' used but no '--to' provided."
            )
        if self.dfrom and not self.dto:
            util.debug(
                self.debuglevel, "E", "'--to' used but no '--from' provided."
            )
        # get sarfilespaths
        if len(remainder) > 0:
            self.sarfilespaths = []
            for path in remainder:
                self.sarfilespaths.append(path)
        # create required files on outputpath
        if os.path.exists(self.outputpath):
            shutil.rmtree(self.outputpath)
        os.makedirs(self.outputpath + "/sar")
        shutil.copytree(
            os.path.dirname(os.path.realpath(__file__)) + "/html",
            self.outputpath + "/html",
        )

    def show_help(self, errmsg=""):
        print(
            "Usage: sarcharts.py"
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
            "\n    - sarcharts.py /tmp/previousmonth/sa?? sa08 sa09 sa1?"
        )
        if errmsg != "":
            print("\nERROR: " + errmsg)

    def main(self):
        sarfiles = util.get_filelist(self.sarfilespaths)
        util.debug(self.debuglevel, "D", "sarfiles: " + str(sarfiles))
        # merge sar files to csv files
        showheader = ""
        notavailable = []
        util.debug(self.debuglevel, "", "Getting data from sar files.")
        for inputfile in sarfiles:
            for k, v in self.charts.items():
                csvfile = self.outputpath + "/sar/" + k + ".csv"
                command = f"sadf -dt {inputfile} -- {v['arg']} {showheader}"
                [stdout, stderr] = util.exec_command(self.debuglevel, command)
                if stderr:
                    if "Requested activities not available" in stderr:
                        util.debug(self.debuglevel, "I", stderr.strip())
                        if k not in notavailable:
                            notavailable.append(k)
                    else:
                        util.debug(self.debuglevel, "W", stderr.strip())
                else:
                    util.debug(
                        self.debuglevel,
                        "D",
                        "Merge " + inputfile + " to " + csvfile,
                    )
                    if os.path.exists(csvfile):
                        with open(csvfile, "a") as myfile:
                            myfile.write(stdout)
                    else:
                        with open(csvfile, "w") as myfile:
                            myfile.write(stdout)
            showheader = "| grep -vE '^#'"

        # convert csv to chartjs compatible Lists
        hostname = ""
        firstdate = ""
        lastdate = ""
        util.debug(self.debuglevel, "", "Generating Charts.")
        for k, v in self.charts.items():
            if k not in notavailable:
                csvfile = self.outputpath + "/sar/" + k + ".csv"
                with open(csvfile) as f:
                    # set the first data field
                    datastart = 4 if self.charts[k]["multiple"] else 3
                    # get headers from first line
                    line = f.readline().strip()
                    headers = line.split(";")[datastart:]
                    # get hostname and first stats date
                    pos = f.tell()
                    line = f.readline().split(";")
                    firstdate = line[2]
                    hostname = line[0]
                    # seek file to first stats line
                    f.seek(pos)
                    for line in f:
                        if "LINUX-RESTART" in line or re.match(r"^#", line):
                            continue
                        fields = line.strip().split(";")
                        if util.in_date_range(self, fields[2]):
                            # set fake item on non-multiple charts
                            item = (
                                fields[3] if self.charts[k]["multiple"] else ""
                            )
                            # add date field to Chart labels
                            if fields[2] not in self.charts[k]["labels"]:
                                self.charts[k]["labels"].append(fields[2])
                            if item not in self.charts[k]["datasets"].keys():
                                self.charts[k]["datasets"][item] = []
                                for h in headers:
                                    i = {"label": h, "values": []}
                                    self.charts[k]["datasets"][item].append(i)

                            for i in range(len(fields[datastart:])):
                                self.charts[k]["datasets"][item][i][
                                    "values"
                                ].append(
                                    fields[i + datastart]
                                )  # noqa E501
                    if line != "":
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
                "lastdate": lastdate,
            }
            parent = (
                os.path.dirname(os.path.realpath(__file__)) + "/templates/"
            )
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(parent)
            )
            template = environment.get_template("chart.html")
            outputfile = self.outputpath + f"/{chart}.html"
            with open(outputfile, mode="w", encoding="utf-8") as results:
                results.write(template.render(context))

        webbrowser.open(self.outputpath + "/cpu.html", 0, True)


SarCharts().main()
