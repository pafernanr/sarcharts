import csv

from sarcharts.lib import util


class Metrics:

    def getCSVdata(args, charts):
        # date;hostname;metric_name;metric_value
        if args.metricfile:
            metrics = {}
            with open(args.metricfile) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for row in csv_reader:
                    if not row[0].startswith("#"):
                        if row[1] not in charts.keys():
                            util.debug(
                                args, 'W',
                                f"Host '{row[1]}' from '{args.metricfile}'"
                                + " not in 'sar' data.")
                            continue
                        if util.in_date_range(args, row[0]):
                            charts[row[1]]['xlabels'].append(row[0])
                            if row[2] not in metrics.keys():
                                metrics[row[2]] = [{'x': row[0], 'y': row[3]}]
                            else:
                                metrics[row[2]].append({'x': row[0], 'y': row[3]})

            for a in charts[row[1]]['activities']:
                for d in charts[row[1]]['activities'][a]['datasets']:
                    for metric, values in metrics.items():
                        charts[row[1]]['activities'][a]['datasets'][d].insert(0, {
                            "label": metric,
                            "yAxisID": 'y1',
                            "values": values
                            })

        return charts
