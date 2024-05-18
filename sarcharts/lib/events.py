import csv

from sarcharts.lib import util


class Events:

    def getCSVdata(args, charts):
        with open(args.eventfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if row[1] not in charts.keys():
                    util.debug(
                        args, 'W',
                        f"Host '{row[1]}' from '{f}' not in 'sar' data.")
                    continue
                charts[row[1]]['xlabels'].append(row[0])
                if row[2] not in charts[row[1]]['events']:
                    charts[row[1]]['events'][row[2]] = []
                charts[row[1]]['events'][row[2]].append(
                       {'date': row[0], 'text': row[3]})

        return charts
