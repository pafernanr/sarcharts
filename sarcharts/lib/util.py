import datetime
import os
import re
import sys

import fnmatch
from pathlib import Path
import subprocess


def debug(debuglevel, sev, msg):
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
    elif levels[sev] >= levels[debuglevel]:
        print(f"{C[sev]}[{sev}]{C['RESET']} {str(msg)}")
    if sev == 'E':
        sys.exit(1)


def exec_command(debuglevel, cmd):
    debug(debuglevel, "D", "execcommand: " + cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    stdout = str(stdout.decode("utf-8"))
    stderr = str(stderr.decode("utf-8"))
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


def valid_date(s: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False


def is_valid_date(debuglevel, d):
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', d):
        return True
    else:
        debug(debuglevel, 'E', "ERROR: date '" + d
              + "' doesn't match %Y-%m-%d %H:%M:%S UTC")


def in_date_range(debuglevel, dfrom, dto, d):
    if is_valid_date(debuglevel, d):
        d = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S UTC')
        if dfrom and dto:
            if d >= dfrom and d <= dto:
                return True
        else:
            return True
