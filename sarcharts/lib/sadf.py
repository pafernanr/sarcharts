import datetime
import json

from sarcharts.lib.progressbar import ProgressBar
from sarcharts.lib import util


class Sadf:

    def sar_to_json(self, args, inputfile, arg,):
        command = f"sadf -tj {inputfile} -- {arg}"
        [stdout, stderr] = util.exec_command(args, command)
        if stderr:
            if "Try to convert it to current format" in stderr:
                # tf = tempfile.NamedTemporaryFile(prefix="sarcharts")
                command = f"sadf -c {inputfile} > /tmp/sarcharts.tmp"
                [stdout, stderr] = util.exec_command(args, command)
                return self.sar_to_json(args, "/tmp/sarcharts.tmp", arg)
            elif "Requested activities not available" in stderr:
                util.debug(args, 'I', stderr.strip())
            else:
                util.debug(args, 'W', f"{command}\n    {stderr.strip()}")
        else:
            return json.loads(stdout)

    def merge_sarfiles(self, args, sarfiles):
        data = []
        for inputfile in sarfiles:
            jdata = self.sar_to_json(args, inputfile, '-A')
            if jdata:
                data.append(jdata)
            else:
                util.debug(args, 'W', f"Can't add data from {inputfile}.")
        return data

    def data_normalization(self, act, data):
        if isinstance(data, list) and isinstance(data[0], dict):
            print(f"{act} is type 1")
            headers = ";".join(data[0].keys())
            print(headers)

    def sar_to_chartjs(self, args, sarfiles):
        data = self.merge_sarfiles(args, sarfiles)
        linehead = "# hostname;interval;timestamp"
        pb = ProgressBar()
        pb.quiet = args.quiet
        all_entries = 0
        for idata in range(len(data)):
            for ihost in range(len(data[idata]['sysstat']['hosts'])):
                for istats in range(len(data[idata]['sysstat'][
                        'hosts'][ihost]['statistics'])):
                    all_entries += len(data[idata]['sysstat']['hosts'][
                        ihost]['statistics'][istats].keys())
        pb.all_entries = all_entries

        pb.start_time = datetime.datetime.now()
        pbi = 0
        charts = {}
        for idata in range(len(data)):
            hostsdata = data[idata]['sysstat']['hosts']
            for ihost in range(len(hostsdata)):  # get timestamps for labels
                hdata = hostsdata[ihost]
                nodename = hdata['nodename']
                if nodename not in charts.keys():
                    charts[nodename] = {
                        "sysname": hdata['sysname'],
                        "release": hdata['release'],
                        "machine": hdata['machine'],
                        "number-of-cpus": hdata['number-of-cpus'],
                        "timezone": hdata['timezone'],
                        "xlabels": [],
                        "activities": {},
                        "events": {'Restart': []}
                        }
                for istats in range(len(hdata['restarts'])):
                    for r in hdata['restarts'][istats].values():
                        date = f"{r['date']} {r['time']}"
                        if util.in_date_range(args, date):
                            charts[nodename]['xlabels'].append(date)
                            charts[nodename]['events']['Restart'].append(
                                {'date': date,
                                 'text': f'Restarted at {date}'
                                 })
                for istats in range(len(hdata['statistics'])):
                    for act, adata in hdata['statistics'][istats].items():
                        pbi += 1
                        pb.print_bar(pbi, f"data {act}.")
                        if act == "timestamp":
                            date = f"{adata['date']} {adata['time']}"
                            if (date not in charts[nodename]['xlabels']
                                    and util.in_date_range(args, date)):
                                charts[nodename]['xlabels'].append(date)
                            linedet = f"{hdata['nodename']};{adata['interval']};{date}"
                        else:
                            if isinstance(adata, list):
                                if act not in charts[nodename]['activities'].keys():
                                    line = linehead
                                    for h in adata[0].keys():
                                        line += f";{str(h)}"
                                    charts[nodename]['activities'][act] = {
                                        "content": [line.split(";")],
                                        "multiple": True
                                        }
                                for d in adata:
                                    line = linedet
                                    for v in d.values():
                                        line += f";{str(v)}"
                                    charts[nodename]['activities'][act][
                                        'content'].append(line.split(";"))
                            elif isinstance(adata, dict):
                                d = adata[list(adata.keys())[1]]
                                if isinstance(d, float) or isinstance(d, int):
                                    if (act not in charts[nodename][
                                            'activities'].keys()):
                                        line = linehead
                                        for h in adata.keys():
                                            line += f";{str(h)}"
                                        charts[nodename]['activities'][act] = {
                                            "content": [line.split(";")],
                                            "multiple": False
                                            }
                                    line = linedet
                                    for v in adata.values():
                                        line += f";{str(v)}"
                                    charts[nodename]['activities'][act][
                                        'content'].append(line.split(";"))
                                else:
                                    for subact, subdata in adata.items():
                                        nact = f"{act}_{subact}"
                                        if isinstance(subdata, list):
                                            if (nact not in charts[nodename][
                                                    'activities'].keys()):
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
                                        elif isinstance(subdata, dict):
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

                                        elif isinstance(subdata, float) or isinstance(subdata, int):
                                            if (nact not in charts[nodename][
                                                    'activities'].keys()):
                                                line = f"{linehead};{nact}"
                                                charts[nodename]['activities'][nact] = {
                                                    "content": [line.split(";")],
                                                    "multiple": False
                                                    }
                                            line = f"{linedet};{str(subdata)}"
                                            charts[nodename]['activities'][nact][
                                                'content'].append(line.split(";"))

        pb.finish("  Get data.")
        # write csv files
        for nodename, nodecharts in charts.items():
            for activity, csvdata in charts[nodename]['activities'].items():
                with open(f"{args.outputpath}/sar/{nodename}_{activity}.csv", "w") as f:
                    # workaround for io.cs headers (maybe other activities)
                    n = len(csvdata['content'][1])
                    f.write(";".join(csvdata['content'][0][:n]) + "\n")
                    csvdata['content'].pop(0)
                    csvdata['content'].sort(key=lambda x: x[2])
                    for line in csvdata['content']:
                        if util.in_date_range(args, line[2]):
                            f.write(";".join(line) + "\n")

        # build the chartjs dict
        for nodename, nodecharts in charts.items():
            for activity, csvdata in nodecharts['activities'].items():
                csvfile = f"{args.outputpath}/sar/{nodename}_{activity}.csv"
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
                        # insert a fake item on non multiple nodecharts
                        item = fields[3] if csvdata['multiple'] else ""
                        if item not in charts[nodename]['activities'][activity]['datasets'].keys():
                            charts[nodename]['activities'][activity]['datasets'][item] = []
                            for h in headers:
                                charts[nodename]['activities'][activity]['datasets'][item].append({
                                    "label": h,
                                    "values": []
                                    })

                        for f in range(len(fields[datastart:])):
                            charts[nodename]['activities'][activity]['datasets'][item][f]['values'].append({
                                    'x': fields[2],
                                    'y': fields[f+datastart]
                                    })
        return charts
