import os

import jinja2


class ChartJS:

    def write_files(self, charts, colors, chartinfo, outputpath):
        for chart, details in charts.items():
            context = {
                "chart": chart,
                "details": details,
                "pages": charts.keys(),
                "colors": colors,
                "notavailable": chartinfo['notavailable'],
                "hostnames": chartinfo['hostnames'],
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
