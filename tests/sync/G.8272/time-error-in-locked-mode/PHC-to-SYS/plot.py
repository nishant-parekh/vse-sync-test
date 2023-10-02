#!/usr/bin/env python3

### SPDX-License-Identifier: GPL-2.0-only

"""Plot data for tests under:

sync/G.8272/time-error-in-locked-mode/PHC-to-SYS

Use a symbolic link to specify this file as the plotter for a test.
"""

import sys
from argparse import ArgumentParser

from vse_sync_pp.common import (
    open_input,
    print_loj,
)

from vse_sync_pp.parsers.phc2sys import TimeErrorParser
from vse_sync_pp.plot import Plotter, Axis, TIMESERIES

def main():
    """Plot test data and print files output as JSON to stdout

    To generate an image file, supply the output image prefix (path and stem)
    followed by exactly the same command line args as supplied to the reference
    implementation.
    """
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('prefix', help="output image prefix")
    aparser.add_argument('input')
    args = aparser.parse_args()
    parser = TimeErrorParser()
    plotter = Plotter(TIMESERIES, Axis("Time Error (unfiltered)", parser.y_name))
    with open_input(args.input) as fid:
        for parsed in parser.parse(fid, relative=True):
            plotter.append(parsed)
    output = f'{args.prefix}.png'
    plotter.plot(output)
    item = {
        'path': output,
        'title': "PHC-to-SYS Time Error (unfiltered)",
    }
    # Python exits with error code 1 on EPIPE
    if not print_loj([item]):
        sys.exit(1)

if __name__ == '__main__':
    main()
