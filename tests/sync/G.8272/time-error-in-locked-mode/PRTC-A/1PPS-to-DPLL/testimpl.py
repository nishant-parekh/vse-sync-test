#!/usr/bin/env python3

### SPDX-License-Identifier: GPL-2.0-only

"""A reference implementation of test:

sync/G.8272/time-error-in-locked-mode/PRTC-A/1PPS-to-DPLL
"""

from argparse import ArgumentParser
import json
from os.path import join as joinpath
from os.path import dirname

from vse_sync_pp.common import JsonEncoder
from vse_sync_pp.parsers.dpll import TimeErrorParser
from vse_sync_pp.analyzers.ppsdpll import TimeErrorAnalyzer
from vse_sync_pp.analyzers.analyzer import Config

CONFIG = joinpath(dirname(__file__), 'config.yaml')

def refimpl(filename, encoding='utf-8'):
    """A reference implementation of test:

    sync/G.8272/time-error-in-locked-mode/PRTC-A/1PPS-to-DPLL

    Return a dict with test result, reason, analysis of logs in `filename`.
    """
    parser = TimeErrorParser()
    analyzer = TimeErrorAnalyzer(Config.from_yaml(CONFIG))
    with open(filename, encoding=encoding) as fid:
        analyzer.collect(*parser.parse(fid))
    return {
        'result': analyzer.result,
        'reason': analyzer.reason,
        'analysis': analyzer.analysis,
    }

def main():
    """Run this test and print test output as JSON to stdout"""
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('input', help="log file to analyze")
    args = aparser.parse_args()
    output = refimpl(args.input)
    print(json.dumps(output, cls=JsonEncoder))

if __name__ == '__main__':
    main()
