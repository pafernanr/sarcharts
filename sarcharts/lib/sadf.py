import datetime
import os
import re

from sarcharts.lib.progressbar import ProgressBar
from sarcharts.lib import util


class Sadf:

    def sar_to_csv(self, inputfile, arg, debuglevel):
        command = f"sadf -d {inputfile} -- {arg}"
        [stdout, stderr] = util.exec_command(debuglevel, command)
        if stderr:
            if "Try to convert it to current format" in stderr:
                # tf = tempfile.NamedTemporaryFile(prefix="sarcharts")
                command = f"sadf -c {inputfile} > /tmp/sarcharts.tmp"
                [stdout, stderr] = util.exec_command(debuglevel, command)
                return self.sar_to_csv(
                    "/tmp/sarcharts.tmp", arg, debuglevel
                    )
            elif "Requested activities not available" in stderr:
                util.debug(debuglevel, 'I', stderr.strip())
            else:
                util.debug(debuglevel, 'W', stderr.strip())
        else:
            out = []
            for line in stdout.split("\n"):
                if line != "":
                    out.append(line.split(";"))
            return out

    def merge_sarfiles(self, debuglevel, sarfiles, outputpath, charts, dfrom, dto):
        pb = ProgressBar()
        pb.all_entries = len(charts) * len(sarfiles)
        pb.start_time = datetime.datetime.now()
        pbi = 0
        for k, v in charts.items():
            content = []
            csvfile = f"{outputpath}/{k}.csv"
            out = False
            for inputfile in sarfiles:
                pbi += 1
                pb.print_bar(
                    pbi,
                    "Get data from " + inputfile.split("/")[-1] + " " + k)
                out = self.sar_to_csv(inputfile, v['arg'], debuglevel)
                if out:
                    headers = out.pop(0)
                    util.debug(debuglevel, 'D',
                               f"Merge {inputfile} to {csvfile}")
                    content = content + out
            if out:
                with open(csvfile, "w") as f:
                    f.write(';'.join(headers) + "\n")
                    content.sort(key=lambda x: x[2])
                    for line in content:
                        if (line[2] != "timestamp" and util.in_date_range(
                                debuglevel, dfrom, dto, line[2])):
                            f.write(';'.join(line) + "\n")
        pb.finish("  Get data.")

    def sar_to_chartjs(
            self, debuglevel, sarfiles, outputpath, charts, dfrom, dto):
        self.merge_sarfiles(
            debuglevel, sarfiles, outputpath, charts, dfrom, dto)
        chartinfo = {
            "notavailable": [],
            "hostname": '',
            "firstdate": '',
            "lastdate": ''
            }
        pb = ProgressBar()
        pb.all_entries = len(charts)
        pb.start_time = datetime.datetime.now()
        pbi = 0
        for k, v in charts.items():
            pbi += 1
            pb.print_bar(pbi, f"Set data for {k} Chart.")
            csvfile = f"{outputpath}/{k}.csv"
            if not os.path.exists(csvfile):
                chartinfo['notavailable'].append(k)
            else:
                with open(csvfile) as f:
                    # set the first data field
                    datastart = 4 if charts[k]['multiple'] else 3
                    # get headers from first line
                    line = f.readline().strip()
                    headers = line.split(";")[datastart:]
                    # get first stats date
                    pos = f.tell()
                    line = f.readline().split(";")
                    chartinfo['hostname'] = line[0]
                    chartinfo['firstdate'] = line[2]
                    # seek file to first stats line
                    f.seek(pos)
                    for line in f:
                        if "LINUX-RESTART" in line or re.match(r"^#", line):
                            continue
                        fields = line.strip().split(";")
                        # set fake item on non multiple charts
                        item = fields[3] if charts[k]['multiple'] else ""
                        # add date field to Chart labels
                        if fields[2] not in charts[k]['labels']:
                            charts[k]['labels'].append(fields[2])
                        if item not in charts[k]['datasets'].keys():
                            charts[k]['datasets'][item] = []
                            for h in headers:
                                charts[k]['datasets'][item].append({
                                    "label": h,
                                    "values": []
                                    })
                        for i in range(len(fields[datastart:])):
                            charts[k]['datasets'][
                                item][i]['values'].append({
                                    'x': fields[2],
                                    'y': fields[i+datastart]
                                    })
                    if line != "":
                        chartinfo['lastdate'] = fields[2]
        pb.finish("  Set Data.")
        return chartinfo
