#!/usr/bin/env python
"""
Generate the 2-way metadata comparison for the TEST and BASE testruns.
"""

import argparse
import logging
import json
import yaml
import os
import pandas as pd

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

ARG_PARSER = argparse.ArgumentParser(description="Generate the 2-way metadata \
comparison for the TEST and BASE testruns.")
# ARG_PARSER.add_argument('--config',
#                         dest='config',
#                         action='store',
#                         help='The yaml config file for generating comparison.',
#                         default='generate_2way_metadata.yaml',
#                         required=False)
ARG_PARSER.add_argument('--test',
                        dest='test',
                        action='store',
                        help='The metadata JSON file for TEST testrun.',
                        default='test.testrun_metadata.json',
                        required=False)
ARG_PARSER.add_argument('--base',
                        dest='base',
                        action='store',
                        help='The metadata JSON file for BASE testrun.',
                        default='base.testrun_metadata.json',
                        required=False)
ARG_PARSER.add_argument('--output-format',
                        dest='output_format',
                        action='store',
                        help='The output format, available in [csv, ].',
                        default='csv',
                        required=False)
ARG_PARSER.add_argument('--output',
                        dest='output',
                        action='store',
                        help='The file to store metadata comparison.',
                        default=None,
                        required=False)

ARGS = ARG_PARSER.parse_args()


class metadata_comparison_generator():
    """Generate TestRun Results according to the customized configuration."""
    def __init__(self, ARGS):
        # load config
        # codepath = os.path.split(os.path.abspath(__file__))[0]
        # filename = os.path.join(codepath, ARGS.config)
        # with open(filename, 'r') as f:
        #     c = yaml.safe_load(f)
        #     self.config = c[__class__.__name__]

        # load metadata for test and base testruns
        with open(ARGS.test, 'r') as f:
            self.test = json.load(f)
        with open(ARGS.base, 'r') as f:
            self.base = json.load(f)

        # parse parameters
        self.output = ARGS.output
        self.output_format = ARGS.output_format

        if self.output is None and self.output_format == 'csv':
            fpath = os.path.dirname(ARGS.test)
            fname = '2way_metadata.csv'
            self.output = os.path.join(fpath, fname)

        # init
        self.datatable = []
        self.dataframe = None
        self._parse_data()
        self._build_dataframe()

    def _parse_data(self):
        """Parse data from the metadata dicts.

        Input:
        - self.test: metadata for TEST testrun.
        - self.base: metadata for BASE testrun.
        - self.config: customized configuration. (TBD)
        Output:
        - self.datatable: datatable to be generated.
        """
        data = {}

        # keys = self.test.keys()                           # test
        # keys = list(self.test.keys() & self.base.keys())  # intersection
        keys = list(self.test.keys() | self.base.keys())  # union
        keys.sort()

        for key in keys:
            data['KEY'] = key
            data['TEST'] = self.test.get(key)
            data['BASE'] = self.base.get(key)

            # save to the data table
            self.datatable.append(data.copy())

    def _build_dataframe(self):
        self.dataframe = pd.DataFrame(self.datatable)

    def dump_to_csv(self):
        with open(self.output, 'w') as f:
            f.write(self.dataframe.to_csv())

    def show_vars(self):
        """Print the value of varibles to the stdout."""
        def _show(name, value):
            print('\n> _show(%s):\n' % name)
            print(value)

        _show('self.test', self.test)
        _show('self.base', self.base)
        _show('self.output', self.output)
        _show('self.output_format', self.output_format)
        _show('self.datatable', self.datatable)
        _show('self.dataframe', self.dataframe)


if __name__ == '__main__':
    gen = metadata_comparison_generator(ARGS)
    gen.dump_to_csv()

exit(0)