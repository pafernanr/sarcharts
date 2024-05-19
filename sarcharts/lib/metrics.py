import csv

from sarcharts.lib import util


class Metrics:

    def getCSVdata(args, charts):
        # date;hostname;metric_name;metric_value
        if args.metricfile:
            values = []
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
                        charts[row[1]]['xlabels'].append(row[0])
                        values.append({'x': row[0], 'y': row[3]})

            for a in charts[row[1]]['activities']:
                for d in charts[row[1]]['activities'][a]['datasets']:
                    charts[row[1]]['activities'][a]['datasets'][d].append({
                        "label": row[2],
                        "yAxisID": 'y1',
                        "type": 'line',
                        "values": values
                        })

        return charts
