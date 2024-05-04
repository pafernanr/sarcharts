import datetime
import re
from pathlib import Path
import os
import subprocess
import sys


def debug(debuglevel, sev, msg):
    levels = {'D': 0,
              'I': 1,
              'W': 2,
              'E': 3
              }
    if levels[sev] >= levels[debuglevel]:
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


def get_sarfiles(Conf):
    sarfiles = []
    filelist = sorted(Path(Conf.inputdir).iterdir(), key=os.path.getmtime)
    # lst = ['this','is','just','a','test']
    # filtered = fnmatch.filter(filelist, 'th?s')
    for i in range(len(filelist)):
        f = filelist[i]
        if f.match('sa[0-9][0-9]'):
            sarfiles.append(str(f))
    return sarfiles


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
