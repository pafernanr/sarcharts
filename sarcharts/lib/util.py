import datetime
import os
import re
import sys

import fnmatch
from pathlib import Path
import subprocess


def debug(debuglevel, sev, msg):
    levels = {'D': 0,
              'I': 1,
              'W': 2,
              'E': 3,
              '': 4
              }
    if sev == "":
        print(f"{str(msg)}")
    elif levels[sev] >= levels[debuglevel]:
        print(f"[{sev}] {str(msg)}")
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
                    files.append(path + str(f))
        # path is a file
        elif Path(path).is_file():
            files.append(str(path))
    return sortfiles_by_mtime(files)


def sortfiles_by_mtime(files):
    details = {}
    for f in files:
        mtime = os.path.getmtime(f)
        details[mtime] = f
    # 'sorted' returns a 'set' hence no duplicates
    # but it should be converted to a list
    return list(dict(sorted(details.items())).values())


def is_valid_date(Conf, d):
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', d):
        return True
    else:
        debug(Conf, 'E', "ERROR: date '" + d
              + "' doesn't match %Y-%m-%d %H:%M:%S")


def in_date_range(Conf, d):
    if is_valid_date(Conf, d):
        d = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
        if Conf.dfrom and Conf.dto:
            if d >= Conf.dfrom and d <= Conf.dto:
                return True
        else:
            return True
