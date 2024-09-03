import datetime
import os
import re

import jinja2
from random import randrange

from sarcharts.lib.progressbar import ProgressBar


class ChartJS:

    def __init__(self, hidden_metrics, hidden_custom):
        self.hidden_metrics = hidden_metrics
        self.hidden_custom = hidden_custom

    def get_color_palette(self, datasets):
        number = 0
        for k, data in datasets.items():
            size = len(data)
            if size > number:
                number = size
        colors = []
        for i in range(0, number):
            r = randrange(225)
            g = randrange(225)
            b = randrange(225)
            colors.append(f"{r}, {g}, {b}")
        return colors

    def is_hidden_metric(self, string):
        for r in self.hidden_metrics:
            if r != "" and re.search(f'^{r}$', string):
                return True

    def is_hidden_custom(self, string):
        for r in self.hidden_custom:
            if r != "" and re.search(r, string):
                return True

    def write_files(self, args, charts):
        pb = ProgressBar()
        all_entries = 0
        for nodename in charts.keys():
            all_entries += len(charts[nodename]['activities'].keys())
        pb.quiet = args.quiet
        pb.all_entries = all_entries
        pb.start_time = datetime.datetime.now()
        pbi = 0
        # show full metric list
        # for activity, csvdata in charts[list(charts.keys())[0]]['activities'].items():
        #     for i in list(csvdata['datasets'].values())[0]:
        #         print(f"{activity}:.*:{i['label']}")
        #     break

        # write output
        for nodename, nodecharts in charts.items():
            for activity, csvdata in nodecharts['activities'].items():
                palette = self.get_color_palette(csvdata['datasets'])
                outputfile = args.outputpath + f"/{nodename}_{activity}.html"
                pbi += 1
                pb.print_bar(pbi, f"{activity}.")
                context = {
                    "chart": activity,
                    "xlabels": sorted(nodecharts['xlabels']),
                    "sysname": nodecharts['sysname'],
                    "release": nodecharts['release'],
                    "machine": nodecharts['machine'],
                    "numberofcpus": nodecharts['number-of-cpus'],
                    "timezone": nodecharts['timezone'],
                    "details": csvdata,
                    "events": nodecharts['events'],
                    "pages": sorted(nodecharts['activities'].keys()),
                    "colors": palette,
                    "hostname": nodename,
                    "hostnames": charts.keys()                    }
                parent = (
                    os.path.dirname(
                        os.path.realpath(__file__)) + "/../templates/"
                        )
                environment = (
                    jinja2.Environment(
                        loader=jinja2.FileSystemLoader(parent),
                        extensions=['jinja2.ext.loopcontrols'])
                )
                environment.filters["is_hidden_metric"] = self.is_hidden_metric
                environment.filters["is_hidden_custom"] = self.is_hidden_custom
                template = environment.get_template("chart.html")
                with open(outputfile, mode="w", encoding="utf-8") as results:
                    results.write(template.render(context))
        pb.finish(f"  Write Charts and CSV file to {args.outputpath}.")
