import datetime
import os

import argparse
import configparser
import fnmatch
from pathlib import Path
import shutil
import webbrowser

from sarcharts.lib.chartjs import ChartJS
from sarcharts.lib.events import Events
from sarcharts.lib.metrics import Metrics
from sarcharts.lib.sadf import Sadf
from sarcharts.lib import util


class SarCharts:
    args = ()
    cwd = os.getcwd()
    default_cfg = f"{Path.home()}/.sarcharts.cfg"

    def valid_date(self, d):
        valid = util.valid_date_formats
        for v in valid:
            try:
                return datetime.datetime.strptime(d, v)
            except ValueError:
                pass
        raise argparse.ArgumentTypeError(
            f"not a valid date: {d!r}. Valid formats: {str(valid)}")

    def valid_config_path(self, path):
        if path == self.default_cfg and not os.path.exists(self.default_cfg):
            currpath = os.path.dirname(os.path.realpath(__file__))
            shutil.copyfile(
                f"{currpath}/conf/sarcharts.cfg-dist",
                self.default_cfg)
            return path
        if os.path.exists(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"not a valid path: {path!r}")

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
            '-c',
            '--configfile',
            help='Use alternative config file. Default `~/.sarcharts.cfg`.',
            default=self.default_cfg,
            type=self.valid_config_path
            )
        self.parser.add_argument(
            '-d',
            '--debug',
            help='Set debug level. Default `W`.',
            default='W',
            choices=['D', 'I', 'W', 'E']
            )
        self.parser.add_argument(
            '-e',
            '--eventfile',
            help='Add events csv file. Header: '
                 + '# date;hostname;eventname;eventdescription',
            type=self.valid_path
            )
        self.parser.add_argument(
            '-f',
            '--fromdate',
            help='Include metrics/events from this date.',
            default=datetime.datetime.strptime('1970-01-01', '%Y-%m-%d'),
            type=self.valid_date
            )
        self.parser.add_argument(
            '-m',
            '--metricfile',
            help='Add metrics csv file. Header: '
                 + '# date;hostname;metricname;metricvalue',
            type=self.valid_path
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
            help='Include metrics/events before this date.',
            default=datetime.datetime.strptime('2039-01-01', '%Y-%m-%d'),
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
            util.debug(self.args, 'E',
                       f"Output path '{self.args.outputpath}' already exists.")
            # shutil.rmtree(self.args.outputpath)
        os.makedirs(self.args.outputpath + "/csvfiles")
        shutil.copytree(os.path.dirname(
                        os.path.realpath(__file__)) + "/html",
                        self.args.outputpath + "/html")

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.args.configfile)

    def main(self):
        self.read_config()
        hidden_metrics = self.config.get('main', 'hidden_metrics').split("\n")
        hidden_custom = self.config.get('main', 'hidden_custom').split("\n")
        if len(self.args.sarfilespaths) > 0:
            sarfiles = util.get_filelist(self.args.sarfilespaths)
            if len(sarfiles) > 0:
                util.debug(self.args, 'D', "sarfiles: " + str(sarfiles))
                charts = Sadf().sar_to_chartjs(self.args, sarfiles)
                charts = Events.getCSVdata(self.args, charts)
                charts = Metrics.getCSVdata(self.args, charts)
                ChartJS(hidden_metrics,
                        hidden_custom).write_files(self.args, charts)
                util.debug(self.args, '', "Open SarCharts in default browser.")
                webbrowser.open(self.args.outputpath, 0, True)
            else:
                self.parser.print_help()
                util.debug(
                    self.args, 'E',
                    f"No valid `sa??` files in `{self.args.sarfilespaths}`.")
