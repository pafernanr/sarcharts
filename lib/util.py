'''
Author: Pablo Fernández Rodríguez
Web: https://github.com/pafernanr/dynflowparser
Licence: GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
'''
import subprocess
import sys


class Util:
    USERS = {}

    def debug(Conf, sev, msg):
        levels = {'D': 0,
                  'I': 1,
                  'W': 2,
                  'E': 3
                  }
        if levels[sev] >= levels[Conf.debug]:
            print(f"[{sev}] {str(msg)}\n")

    def exec_command(Conf, cmd):
        Util.debug(Conf, "D", "execcommand: " + cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout = str(stdout.decode("utf-8"))
        stderr = str(stderr.decode("utf-8"))
        if stderr != "" and "Invalid system activity file:" not in stderr:
            print(cmd + "\n" + stderr)
            sys.exit(1)
        return stdout
