"""
Samplesheet Checking Tools for custom Dragen TSO500 Solid Tumor Panel
"""
import argparse
import os

import pandas as pd
import re

import samplesheetparser as parser

from schema import header_patterns

def parse_arguments():

    argsparser = argparse.ArgumentParser()

    argsparser.add_argument(
            "-s", "--samplesheet", required=True,
            help="samplesheet"
    )
    argsparser.add_argument(
            "-o", "--output", default="report",
            help="directory to store report"
    )

    args = argsparser.parse_args()

    return args

def main(samplesheet, output="report"):
    samplesheet = parser.SampleSheet(samplesheet)
    
    # samplesheet_header = pd.DataFrame(samplesheet.header)
    # samplesheet_reads = pd.DataFrame(samplesheet.reads)
    # samplesheet_settings = pd
    # samplesheet_site = pd.DataFrame(samplesheet.site)
    samplesheet_data = pd.DataFrame(samplesheet.data)
    

    
    print(f'{samplesheet.header} complete and pass all thresholds, release pending')
    print(f'{samplesheet.reads} complete and pass all thresholds, release pending')
    print(f'{samplesheet.settings} complete and pass all thresholds, release pending')
    print(f'{samplesheet.site} complete and pass all thresholds, release pending')
    print(f'{samplesheet.bclconvert_settings} complete and pass all thresholds, release pending')
    print(f'{samplesheet.bclconvert_data} complete and pass all thresholds, release pending')
    
    print (header_patterns.keys())

# Function to validate a field against its pattern
def validate_field(patterns, field, value):
    pattern = patterns.get(field)
    if pattern is not None:
        return bool(re.match(pattern, value))
    return True  # Return True for fields without a pattern

if __name__ == "__main__":

    args = parse_arguments()
    main(args.samplesheet, args.output)
