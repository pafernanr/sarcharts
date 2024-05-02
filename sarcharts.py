#!/usr/bin/python3
'''
Author: Pablo Fernández Rodríguez
Web: https://github.com/pafernanr/sarcharts
Licence: GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
'''
import os
import re
import webbrowser
from jinja2 import Environment, FileSystemLoader
from lib.configuration import Conf
from lib.util import Util


if __name__ == "__main__":
    Conf.get_opts()
    sarfiles = Util.get_sarfiles(Conf)
    showheader = ""
    notavailable = []
    Util.debug(Conf, 'W', "Getting data from sar files.")
    for inputfile in sarfiles[-Conf.last:]:
        for k, v in Conf.charts.items():
            csvfile = Conf.outputdir + "sar/" + k + ".csv"
            [stdout, stderr] = Util.exec_command(Conf, f"sadf -dt {inputfile} -- {v['arg']}"
                                                 + f" {showheader} >> {csvfile}")
            if stderr:
                if "Requested activities not available" in stderr and k not in notavailable:
                    notavailable.append(k)
        showheader = "| grep -vE '^#'"

    hostname = ""
    firstdate = ""
    lastdate = ""
    # convert csv to chartjs compatible Lists
    Util.debug(Conf, 'W', "Generating Charts.")
    for k, v in Conf.charts.items():
        csvfile = Conf.outputdir + "sar/" + k + ".csv"
        with open(csvfile) as f:
            line = f.readline().strip()
            headers = line[2:].split(";")
            # insert fake item for non multiple charts
            if not Conf.charts[k]['multiple']:
                headers.insert(3, "")
            for line in f:
                Util.debug(Conf, 'D', csvfile + ": " + line.strip())
                if "LINUX-RESTART" in line or re.match(r"^#", line):
                    continue
                fields = line.strip().split(";")
                if Util.in_date_range(Conf, fields[2]):
                    if firstdate == "":
                        firstdate = line.split(";")[2]
                    # insert fake item for non multiple charts
                    if not Conf.charts[k]['multiple']:
                        fields.insert(3, "")
                    if fields[2] not in Conf.charts[k]['labels']:
                        Conf.charts[k]['labels'].append(fields[2])  # date
                    item = fields[3].replace("-", "_")
                    if item == "_1":
                        item = "ALL"
                    if item not in Conf.charts[k]['datasets'].keys():
                        Conf.charts[k]['datasets'][item] = []
                        for h in headers[4:]:
                            Conf.charts[k]['datasets'][item].append({"label": h, "values": []})  # noqa E501

                    fields = fields[4:]
                    for i in range(len(fields)):
                        Conf.charts[k]['datasets'][item][i]['values'].append(fields[i])  # noqa E501
            if line != "":
                hostname = line.split(";")[0]
                lastdate = line.split(";")[2]
    # print(Conf.charts)
    # write html output files
    for chart, details in Conf.charts.items():
        context = {
                    "chart": chart,
                    "details": details,
                    "pages": Conf.charts.keys(),
                    "colors": Conf.colors,
                    "notavailable": notavailable,
                    "hostname": hostname,
                    "firstdate": firstdate,
                    "lastdate": lastdate
                }
        parent = os.path.dirname(os.path.realpath(__file__)) + "/templates/"
        environment = Environment(loader=FileSystemLoader(parent))
        template = environment.get_template("chart.html")
        with open(Conf.outputdir + f"/{chart}.html", mode="w", encoding="utf-8") as results:  # noqa E501
            results.write(template.render(context))

    webbrowser.open(Conf.outputdir + "/cpu.html", 0, True)
