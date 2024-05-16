import datetime
import os
import sys

import fnmatch
from pathlib import Path
import subprocess


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
    # but it should be converted to a list
    return list(dict(sorted(details.items())).values())


def valid_date(args, d):
    format = "%Y-%m-%d %H:%M:%S"
    try:
        return datetime.datetime.strptime(d, format)
    except ValueError:
        debug(args, 'E', f"ERROR: date '{d}' doesn't match {format}.")


def in_date_range(args, d):
    d = valid_date(args, d)
    if d >= args.fromdate and d <= args.todate:
        return True
    else:
        return False
