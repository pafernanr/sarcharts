import csv

from sarcharts.lib import util


class Events:

    def getCSVdata(args, charts):
        if args.eventfile:
            with open(args.eventfile) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for row in csv_reader:
                    if not row[0].startswith("#"):
                        if row[1] not in charts.keys():
                            util.debug(
                                args, 'W',
                                f"Host '{row[1]}' from '{args.eventfile}'"
                                + " not in 'sar' data.")
                            continue
                        if util.in_date_range(args, row[0]):
                            charts[row[1]]['xlabels'].append(row[0])
                            if row[2] not in charts[row[1]]['events']:
                                charts[row[1]]['events'][row[2]] = []
                            charts[row[1]]['events'][row[2]].append(
                                   {'date': row[0],
                                    'description': (
                                        row[3]
                                        .replace(r'"', r'\"')
                                        .replace(r'(', r'\(')
                                        .replace(r')', r'\)'))
                                    })

        return charts
