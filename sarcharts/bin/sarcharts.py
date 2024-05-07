#!/usr/bin/python3
import os
import sys

try:
    sys.path.insert(0, os.getcwd())
    from sarcharts import SarCharts
except KeyboardInterrupt:
    raise SystemExit()


def main():
    SarCharts().main()
