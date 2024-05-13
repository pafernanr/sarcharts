import datetime
import json
import os

from sarcharts.lib.progressbar import ProgressBar
from sarcharts.lib import util


class Sadf:

    def sar_to_json(self, inputfile, arg, debuglevel, dfrom, dto):
        command = f"sadf -tj {inputfile} -- {arg}"
        [stdout, stderr] = util.exec_command(debuglevel, command)
        if stderr:
            if "Try to convert it to current format" in stderr:
                # tf = tempfile.NamedTemporaryFile(prefix="sarcharts")
                command = f"sadf -c {inputfile} > /tmp/sarcharts.tmp"
                [stdout, stderr] = util.exec_command(debuglevel, command)
                return self.sar_to_json("/tmp/sarcharts.tmp", arg, debuglevel, dfrom, dto)
            elif "Requested activities not available" in stderr:
                util.debug(debuglevel, 'I', stderr.strip())
            else:
                util.debug(debuglevel, 'W', command)
                util.debug(debuglevel, 'W', stderr.strip())
        else:
            return json.loads(stdout)

    def merge_sarfiles(self, debuglevel, sarfiles, dfrom, dto):
        data = []
        for inputfile in sarfiles:
            jdata = self.sar_to_json(inputfile, '-A', debuglevel, dfrom, dto)
            if jdata:
                data.append(jdata)
            else:
                util.debug(debuglevel, 'W', f"Can't add data from {inputfile}.")
        return data

    def sar_to_chartjs(self, debuglevel, quiet, sarfiles, outputpath, dfrom, dto):
        data = self.merge_sarfiles(debuglevel, sarfiles, dfrom, dto)
        linehead = "# hostname;interval;timestamp"
        pb = ProgressBar()
        pb.quiet = quiet
        pb.all_entries = len(data[0]['sysstat']['hosts'][0]['statistics'])
        pb.start_time = datetime.datetime.now()
        pbi = 0
        charts = {}
        for idata in range(len(data)):
            hostsdata = data[idata]['sysstat']['hosts']
            for ihost in range(len(hostsdata)):  # get timestamps for labels
                hostdata = hostsdata[ihost]
                nodename = hostdata['nodename']
                if nodename not in charts.keys():
                    charts[nodename] = {
                        "sysname": hostdata['sysname'],
                        "release": hostdata['release'],
                        "machine": hostdata['machine'],
                        "number-of-cpus": hostdata['number-of-cpus'],
                        "timezone": hostdata['timezone'],
                        "xlabels": [],
                        "activities": {}
                        }
                for istats in range(len(hostdata['statistics'])):
                    for act, actdata in hostdata['statistics'][istats].items():
                        if act == "timestamp":
                            date = f"{actdata['date']} {actdata['time']}"
                            if date not in charts[nodename]['xlabels']:
                                charts[nodename]['xlabels'].append(date)
                            linedet = f"{hostdata['nodename']};{actdata['interval']};{date}"
                        else:
                            if isinstance(actdata, list):  # cpu
                                if act not in charts[nodename]['activities'].keys():
                                    line = linehead
                                    for h in actdata[0].keys():
                                        line += f";{str(h)}"
                                    charts[nodename]['activities'][act] = {
                                        "content": [line.split(";")],
                                        "multiple": True
                                        }
                                for d in actdata:
                                    line = linedet
                                    for v in d.values():
                                        line += f";{str(v)}"
                                    charts[nodename]['activities'][act]['content'].append(line.split(";"))
                            elif isinstance(actdata, dict):
                                d = actdata[list(actdata.keys())[0]]
                                if isinstance(d, float) or isinstance(d, int):  # proc
                                    if act not in charts[nodename]['activities'].keys():
                                        line = linehead
                                        for h in actdata.keys():
                                            line += f";{str(h)}"
                                        charts[nodename]['activities'][act] = {
                                            "content": [line.split(";")],
                                            "multiple": False
                                            }
                                    line = linedet
                                    for v in actdata.values():
                                        line += f";{str(v)}"
                                    charts[nodename]['activities'][act]['content'].append(line.split(";")) 
                                else:  # network
                                    for subact, subdata in actdata.items():
                                        nact = f"{act}_{subact}"
                                        if isinstance(subdata, list):
                                            if nact not in charts[nodename]['activities'].keys():
                                                line = linehead
                                                for h in subdata[0].keys():
                                                    line += f";{str(h)}"
                                                charts[nodename]['activities'][nact] = {
                                                    "content": [line.split(";")],
                                                    "multiple": True
                                                    }
                                            for sv in subdata:
                                                line = linedet
                                                for v in sv.values():
                                                    line += f";{str(v)}"
                                                charts[nodename]['activities'][nact]['content'].append(line.split(";"))                                        
                                        else:
                                            if nact not in charts[nodename]['activities'].keys():
                                                line = linehead
                                                for h in subdata.keys():
                                                    line += f";{str(h)}"
                                                charts[nodename]['activities'][nact] = {
                                                    "content": [line.split(";")],
                                                    "multiple": False
                                                    }
                                            line = linedet
                                            for v in subdata.values():
                                                line += f";{str(v)}"
                                            charts[nodename]['activities'][nact]['content'].append(line.split(";"))                                        

        # write csv files
        for nodename, nodecharts in charts.items():
            for activity, csvdata in charts[nodename]['activities'].items():
                with open(f"{outputpath}/{nodename}_{activity}.csv", "w") as f:
                    f.write(";".join(csvdata['content'][0]) + "\n")
                    csvdata['content'].pop(0)
                    csvdata['content'].sort(key=lambda x: x[2])
                    for line in csvdata['content']:
                        f.write(";".join(line) + "\n")

        for nodename, nodecharts in charts.items():
            for activity, csvdata in nodecharts['activities'].items():
                csvfile = f"{outputpath}/{nodename}_{activity}.csv"
                pbi += 1
                pb.print_bar(pbi, f"Read {nodename} :: {activity}.")
                with open(csvfile) as f:
                    charts[nodename]['activities'][activity]['datasets'] = {}
                    # set the first data field
                    datastart = 4 if csvdata['multiple'] else 3
                    # get headers from first line
                    line = f.readline().strip()
                    headers = line.split(";")[datastart:]
                    # get first stats date
                    pos = f.tell()
                    line = f.readline().split(";")
                    # seek file to first stats line
                    f.seek(pos)
                    for line in f:
                        fields = line.strip().split(";")
                        # set fake item on non multiple nodecharts
                        item = fields[3] if csvdata['multiple'] else ""
                        if item not in charts[nodename]['activities'][activity]['datasets'].keys():
                            charts[nodename]['activities'][activity]['datasets'][item] = []
                            for h in headers:
                                charts[nodename]['activities'][activity]['datasets'][item].append({
                                    "label": h,
                                    "values": []
                                    })
                        for i in range(len(fields[datastart:])):
                            charts[nodename]['activities'][activity]['datasets'][item][i]['values'].append({
                                    'x': fields[2],
                                    'y': fields[i+datastart]
                                    })
        pb.finish("  Set Data.")
        return charts
