class ChartsConf:
    charts = {
        "cpu": {
            "arg": "-P ALL",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [
                '%steal',
                '%idle'
                ]
            },
        "disk": {
            "arg": "-d",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [
                'tps',
                'dtps',
                'bread/s',
                'bwrtn/s',
                'bdscd/s'
                ]
            },
        "hugepages": {
            "arg": "-H",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "inodes": {
            "arg": "-v",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "io": {
            "arg": "-b",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "interrrupts": {
            "arg": "-I",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "load": {
            "arg": "-q LOAD",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [
                'runq-sz',
                'plist-sz',
                'blocked'
                ]
            },
        "memory": {
            "arg": "-r ALL",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [
                'kbmemfree',
                'kbavail',
                'kbmemused',
                'kbbuffers',
                'kbcached',
                'kbcommit',
                '%commit',
                'kbactive',
                'kbinact',
                'kbdirty',
                'kbanonpg',
                'kbslab',
                'kbkstack',
                'kbpgtbl',
                'kbvmused'
                ]
            },
        "mount": {
            "arg": "-F",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netdevice": {
            "arg": "-n DEV",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": [
                'rxpck/s',
                'txpck/s',
                'rxcmp/s',
                'txcmp/s',
                'rxmcst/s',
                '%ifutil'
                ]
            },
        "netdevicee": {
            "arg": "-n EDEV",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netfiberchannel": {
            "arg": "-n FC",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "neticmp": {
            "arg": "-n ICMP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "neticmpe": {
            "arg": "-n EICMP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netip": {
            "arg": "-n IP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netipe": {
            "arg": "-n EIP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netip6": {
            "arg": "-n IP6",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netip6e": {
            "arg": "-n EIP6",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netnfs": {
            "arg": "-n NFS",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netsock": {
            "arg": "-n SOCK",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netsock6": {
            "arg": "-n SOCK6",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "nettcp": {
            "arg": "-n TCP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "nettcpe": {
            "arg": "-n ETCP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netudp": {
            "arg": "-n UDP",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "netudp6": {
            "arg": "-n UDP6",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "paging": {
            "arg": "-B",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [
                'fault/s',
                'majflt/s',
                'pgfree/s',
                'pgscank/s',
                'pgscand/s',
                'pgsteal/s',
                '%vmeff'
                ]
            },
        "powermanagement": {
            "arg": "-m ALL",
            "multiple": True,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "swap": {
            "arg": "-S",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": [
                'kbswpfree',
                'kbswpused',
                'kbswpcad',
                '%swpcad'
                ]
            },
        "tasks": {
            "arg": "-w",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
        "tty": {
            "arg": "-y",
            "multiple": False,
            "datasets": {},
            "labels": [],
            "hidden": []
            },
              }
    colors = ['255, 99, 132',
              '255, 159, 64',
              '255, 205, 86',
              '75, 192, 192',
              '54, 162, 235',
              '153, 102, 255',
              '201, 203, 207',
              '153, 24, 44',
              '54, 157, 72',
              '75, 89, 123',
              '255, 22, 237',
              '99, 215, 99',
              '199, 215, 29',
              '68, 15, 229',
              '88, 115, 67',
              '149, 245, 44']
