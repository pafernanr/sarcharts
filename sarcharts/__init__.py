import datetime
import os

import argparse
import fnmatch
import shutil
import webbrowser

from sarcharts.lib.chartjs import ChartJS
from sarcharts.lib.sadf import Sadf
from sarcharts.lib import util


class SarCharts:
    args = ()
    cwd = os.getcwd()
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

    def valid_date(self, d):
        valid = ["%Y-%m-%d %H:%M:%S",
                 "%Y-%m-%d %H",
                 "%Y-%m-%d %H:%M",
                 "%Y-%m-%d"
                 ]
        format = "%Y-%m-%d %H:%M:%S"
        for v in valid:
            try:
                o = datetime.datetime.strptime(d, v)
                return datetime.datetime.strptime(str(o), format)
            except ValueError:
                pass
        raise argparse.ArgumentTypeError(
            f"not a valid date: {d!r}. Valid formats: {str(valid)}")

    def valid_path(self, path):
        if os.path.exists(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"not a valid path: {path!r}")

    def default_sarfiles(self):
        files = []
        for f in os.listdir(self.cwd):
            if fnmatch.fnmatch(f, 'sa??'):
                files.append(f"{self.cwd}/{str(f)}")
        return files

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="SarCharts gets \"sysstat\" files from provided"
            + " `sarfilespaths` and generates dynamic HTML Charts."
            )
        self.parser.add_argument(
            '-d',
            '--debug',
            help='Set debug level. Default `W`.',
            default='W',
            choices=['D', 'I', 'W', 'E']
            )
        self.parser.add_argument(
            '-f',
            '--fromdate',
            help='Read metric starting on this date.',
            default='1970-01-01 00:00:00',
            type=self.valid_date
            )
        self.parser.add_argument(
            '-o',
            '--outputpath',
            help='Path to put output files. Default `./sarcharts`.',
            default='.'
            )
        self.parser.add_argument(
            '-t',
            '--todate',
            help='Discard metrics after this date.',
            default='2099-01-01 00:00:00',
            type=self.valid_date
            )
        self.parser.add_argument(
            '-q',
            '--quiet',
            help="Don't show progress.",
            default=False,
            action='store_true'
            )
        self.parser.add_argument(
            'sarfilespaths',
            help='`sa` file/s to parse. Default: `./sa??`.',
            default=self.default_sarfiles(),
            type=self.valid_path,
            nargs='*'
            )
        self.args = self.parser.parse_args()

        # create required files on outputpath
        self.args.outputpath = self.args.outputpath + "/sarcharts"
        if os.path.exists(self.args.outputpath):
            util.debug(self.args.debug, 'E',
                       f"Output path '{self.args.outputpath}' already exists.")
            # shutil.rmtree(self.args.outputpath)
        os.makedirs(self.args.outputpath + "/sar")
        shutil.copytree(os.path.dirname(
                        os.path.realpath(__file__)) + "/html",
                        self.args.outputpath + "/html")

    def main(self):
        # import ipdb; ipdb.set_trace()
        if len(self.args.sarfilespaths) > 0:
            sarfiles = util.get_filelist(self.args.sarfilespaths)
            util.debug(self.args.debug, 'D', "sarfiles: " + str(sarfiles))
            charts = Sadf().sar_to_chartjs(
                self.args.debug, self.args.quiet, sarfiles, self.args.outputpath + "/sar",
                self.args.fromdate, self.args.todate
                )
            ChartJS().write_files(charts, self.colors, self.args.outputpath)
            util.debug(self.args.debug, '',
                       "Open SarCharts in default browser.")
            webbrowser.open(self.args.outputpath + "/cpu.html", 0, True)
        else:
            self.parser.print_help()
            util.debug(self.args.debug, 'E',
                       "No valid `sa` files on provided path.")
