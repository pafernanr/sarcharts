import datetime
import os
import sys

import fnmatch
from pathlib import Path
import subprocess


# 'sar' default format on first place for performance
valid_date_formats = ["%Y-%m-%d %H:%M:%S",
                      "%Y-%m-%dT%H:%M:%S%z",
                      "%Y-%m-%dT%H:%M:%S",
                      "%Y-%m-%d %H:%M",
                      "%Y-%m-%d %H",
                      "%Y-%m-%d"
                      # 14/May/2024:14:49:20 +0200 # apache
                      # May 14 14:42:56 # messages
                      ]


def debug(args, sev, msg):
    if args.quiet:
        return
    C = {
        'I': '\033[0;34m',
        'D': '\033[01;36m',
        '': '\033[0;32m',
        'W': '\033[93m',
        'E': '\033[0;31m',
        'RESET': '\033[0m'
        }
    levels = {'D': 0,
              'I': 1,
              'W': 2,
              'E': 3,
              '': 4
              }
    if sev == "":
        print(f"  {str(msg)}")
    elif levels[sev] >= levels[args.debug]:
        print(f"{C[sev]}[{sev}]{C['RESET']} {str(msg)}")
    if sev == 'E':
        sys.exit(1)


def exec_command(args, cmd):
    debug(args, "D", "execcommand: " + cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    stdout = str(stdout.decode(encoding="utf-8", errors="ignore"))
    stderr = str(stderr.decode(encoding="utf-8", errors="ignore"))
    # if stderr != "":
    #    print(cmd + "\n" + stderr)
    #    sys.exit(1)
    return [stdout, stderr]


def get_filelist(filepaths):
    files = []
    for path in filepaths:
        # path is a folder
        if Path(path).is_dir():
            for f in os.listdir(path):
                if fnmatch.fnmatch(f, 'sa??'):
                    files.append(f"{path}/{str(f)}")
        # path is a file
        elif Path(path).is_file():
            files.append(str(path))
    return files


def sortfiles_by_mtime(files):
    details = {}
    for f in files:
        mtime = os.path.getmtime(f)
        details[mtime] = f
    # 'sorted' returns a 'set' hence no duplicates
    # but it still needs to be converted to list
    return list(dict(sorted(details.items())).values())


def valid_date(args, d):
    valid = valid_date_formats
    for v in valid:
        try:
            return datetime.datetime.strptime(d, v)
        except ValueError:
            continue
    debug(args, 'E', f"not a valid date: {d!r}. Valid formats: {str(valid)}")


def in_date_range(args, d):
    d = valid_date(args, d).timestamp()
    # use timestamps to avoid compare offset-naive and offset-aware datetimes
    if d >= args.fromdate.timestamp() and d <= args.todate.timestamp():
        return True
    else:
        return False
