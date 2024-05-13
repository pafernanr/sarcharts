import datetime
import os
import pprint

import jinja2

from sarcharts.lib.progressbar import ProgressBar


class ChartJS:

    def write_files(self, charts, colors, outputpath):
        pb = ProgressBar()
        pb.all_entries = len(charts) * len(charts)
        pb.start_time = datetime.datetime.now()
        pbi = 0
        for nodename, nodecharts in charts.items():
            for activity, csvdata in nodecharts['activities'].items():
                outputfile = outputpath + f"/{nodename}_{activity}.html"
                pbi += 1
                pb.print_bar(pbi, f"Write {outputfile}.")
                context = {
                    "chart": activity,
                    "xlabels": sorted(nodecharts['xlabels']),
                    "details": csvdata,
                    "pages": sorted(nodecharts['activities'].keys()),
                    "colors": colors,
                    "hostname": nodename
                    }
                parent = (
                    os.path.dirname(
                        os.path.realpath(__file__)) + "/../templates/"
                        )
                environment = (
                    jinja2.Environment(loader=jinja2.FileSystemLoader(parent))
                    )
                template = environment.get_template("chart.html")
                with open(outputfile, mode="w", encoding="utf-8") as results:
                    results.write(template.render(context))
        pb.finish(f"  Write Output to {outputpath}.")
