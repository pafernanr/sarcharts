import csv

from sarcharts.lib import util


class Metrics:

    def getCSVdata(args, charts):
        # date;hostname;metric1;metric2;...
        if args.metricfile:
            metrics = {}
            with open(args.metricfile) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for r, row in enumerate(csv_reader):
                    if r == 0:
                        for i in range(2, len(row)):
                            metrics[row[i]] = []
                    else:
                        if row[1] not in charts.keys():
                            util.debug(
                                args, 'W',
                                f"Host '{row[1]}' from '{args.metricfile}'"
                                + " not in 'sar' data. Metric ignored!!!")
                            continue
                        if util.in_date_range(args, row[0]):
                            charts[row[1]]['xlabels'].append(row[0])
                            for i in range(len(metrics.keys())):
                                k = list(metrics.keys())[i]
                                metrics[k].append({'x': row[0], 'y': row[i+2]})

            for a in charts[row[1]]['activities']:
                for d in charts[row[1]]['activities'][a]['datasets']:
                    for m in reversed(range(len(metrics.keys()))):
                        metric = list(metrics.keys())[m]
                        values = list(metrics.values())[m]
                        charts[row[1]]['activities'][a]['datasets'][d].insert(0, {
                            "label": f"extrametric_{metric}",
                            "yAxisID": f"y{m}",
                            "values": values
                            })

        return charts
