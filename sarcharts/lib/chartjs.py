import datetime
import os

import jinja2

from sarcharts.lib.progressbar import ProgressBar


class ChartJS:

    colors = [
        '255, 99, 132',
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

    def write_files(self, args, charts):
        pb = ProgressBar()
        all_entries = 0
        for nodename in charts.keys():
            all_entries += len(charts[nodename]['activities'].keys())
        pb.quiet = args.quiet
        pb.all_entries = all_entries
        pb.start_time = datetime.datetime.now()
        pbi = 0
        for nodename, nodecharts in charts.items():
            for activity, csvdata in nodecharts['activities'].items():
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
                    "colors": self.colors,
                    "hostname": nodename,
                    "hostnames": charts.keys()
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
        pb.finish(f"  Write Charts and CSV file to {args.outputpath}.")
