import datetime
import os

import jinja2

from sarcharts.lib.progressbar import ProgressBar


class ChartJS:

    def write_files(self, charts, colors, chartinfo, outputpath):
        pb = ProgressBar()
        pb.all_entries = len(charts) * len(charts)
        pb.start_time = datetime.datetime.now()
        pbi = 0
        for chart, details in charts.items():
            pbi += 1
            pb.print_bar(pbi, f"Write {chart}.")
            context = {
                "chart": chart,
                "details": details,
                "pages": charts.keys(),
                "colors": colors,
                "notavailable": chartinfo['notavailable'],
                "hostname": chartinfo['hostname'],
                "firstdate": chartinfo['firstdate'],
                "lastdate": chartinfo['lastdate']
                }
            parent = (
                os.path.dirname(os.path.realpath(__file__)) + "/../templates/"
                )
            environment = (
                jinja2.Environment(loader=jinja2.FileSystemLoader(parent))
                )
            template = environment.get_template("chart.html")
            outputfile = outputpath + f"/{chart}.html"
            with open(outputfile, mode="w", encoding="utf-8") as results:
                results.write(template.render(context))
        pb.finish(f"  Write Output to {outputpath}.")
