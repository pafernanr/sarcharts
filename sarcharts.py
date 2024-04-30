#!/usr/bin/python3
'''
Author: Pablo Fernández Rodríguez
Web: https://github.com/pafernanr/sarcharts
Licence: GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
'''
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
from lib.configuration import Conf
from lib.util import Util


if __name__ == "__main__":
    Conf.get_opts()
    sarfiles = Util.get_sarfiles(Conf)
    showheader = ""
    for f in sarfiles[-Conf.limit:]:
        inputfile = Conf.inputdir + "/" + f
        for k, v in Conf.charts.items():
            csvfile = Conf.outputdir + "sar/" + k + ".csv"
            Util.exec_command(Conf, f"sadf -dt {inputfile} -- {v['arg']}"
                              + f" {showheader} >> {csvfile}")
        showheader = "| grep -vE '^#'"

    # convert csv to chartjs compatible Lists
    for k, v in Conf.charts.items():
        csvfile = Conf.outputdir + "sar/" + k + ".csv"
        with open(csvfile) as f:
            line = f.readline().strip()
            headers = line[2:].split(";")
            for h in headers[3:]:
                Conf.charts[k]['datasets'].append({"label": h,
                                                   "data": []})
            for line in f:
                fields = line.strip().split(";")
                if Util.in_date_range(Conf, fields[2]):
                    Conf.charts[k]['labels'].append(fields[2])
                    fields = fields[3:]
                    for i in range(len(fields)):
                        Conf.charts[k]['datasets'][i]['data'].append(fields[i])

    # write html output files
    for chart, details in Conf.charts.items():
        context = {
                    "chart": chart,
                    "details": details,
                    "pages": Conf.charts.keys(),
                    "colors": Conf.colors
                }
        parent = os.path.dirname(os.path.realpath(__file__)) + "/templates/"
        environment = Environment(loader=FileSystemLoader(parent))
        template = environment.get_template("chart.html")
        with open(Conf.outputdir + f"/{chart}.html", mode="w", encoding="utf-8") as results:  # noqa E501
            results.write(template.render(context))

    webbrowser.open(Conf.outputdir + "/cpu.html", 0, True)

    # print(Conf.charts)
