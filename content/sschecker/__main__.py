"""
Samplesheet Checking Tools for custom Dragen TSO500 Solid Tumor Panel
"""
import argparse
import os

import pandas as pd
import re

import samplesheetparser as parser

from schema import header_patterns, reads_patterns, settings_patterns, site_patterns, bclconvert_settings_patterns
from schema import data_patterns, bclconvert_data_patterns

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
    
    samplesheet_data = pd.DataFrame(samplesheet.data)
    bcl_data = pd.DataFrame(samplesheet.bclconvert_data)
        
    ## Validate Header
    print("===============================================================")
    print("Validating Header")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet.header, header_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        raise Exception (f"Invalid keys: {invalid_keys}")
    else:
        print(">> Header is valid")
        
    print("===============================================================")
    print("Validating Reads")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet.reads, reads_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in reads_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print(">> Reads are valid")
    
    print("===============================================================")
    print("Validating Settings")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet.settings, settings_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in settings_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print(">> Settings are valid")
        
    print("===============================================================")
    print("Validating Site")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet.site, site_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in site_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print(">> Site is valid")

    print("===============================================================")
    print("Validating Data")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet_data, data_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in data_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print("> Data structure is valid")
        
    ## validating index_ID, I7_index_ID and I5_index_ID order
    if not is_series_ordered(samplesheet_data.Index_ID):
        raise Exception (f"Index_ID is not ordered")
    if not is_series_ordered(samplesheet_data['I7_Index_ID']):
        raise Exception (f"I7_Index_ID is not ordered")
    if not is_series_ordered(samplesheet_data['I5_Index_ID']):
        raise Exception (f"I5_Index_ID is not ordered")
    
    print ("> Index_ID, I7_Index_ID and I5_Index_ID are ordered")
    print (">> Data is valid")
    
    print("===============================================================")
    print("Validating BCLConvert Settings")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(samplesheet.bclconvert_settings, bclconvert_settings_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in bclconvert_settings_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print(">> BCLConvert Settings are valid")
        
    print("===============================================================")
    print("Validating BCLConvert Data")
    print("===============================================================")
    missing_keys, _, invalid_keys = validate_dict(bcl_data, bclconvert_data_patterns).values()
    if len(missing_keys) > 0:
        raise Exception (f"Missing keys: {missing_keys}")
    elif len(invalid_keys) > 0:
        print (f"Valid Entry has a format of:")
        print ('---------------------------------------------------------------')
        for entry, value in bclconvert_data_patterns.items():
            print (f"{entry}: {value}")
            print ('---------------------------------------------------------------')
        raise Exception (f"Invalid Entry: {invalid_keys}")
    else:
        print(">> BCLConvert Data is valid")
    
    print("===============================================================")
    print("===============================================================")
    print(">> Samplesheet is valid")
    print("===============================================================")
    

# Function to validate a field against its pattern
def validate_field(patterns, field, value):
    pattern = patterns.get(field)
    if pattern is not None:
        return bool(re.match(pattern, value))
    return True  # Return True for fields without a pattern

def validate_dict(data, patterns):
    valid_keys = []
    invalid_keys = []
    missing_keys = set(patterns.keys()) - set(data.keys())

    for field, pattern in patterns.items():
        if field not in data:
            missing_keys.add(field)
        elif isinstance(pattern, str):
            if isinstance(data[field], pd.Series):
                for value in data[field]:
                    if value == pattern:
                        valid_keys.append(value)
                    else:
                        invalid_keys.append(value)
            elif data[field] == pattern:
                valid_keys.append(field)
            else:    
                invalid_keys.append(field)        
                
        elif isinstance(pattern, re.Pattern):
            if isinstance(data[field], pd.Series):
                for value in data[field]:
                    if pattern.match(value):
                        valid_keys.append(value)
                    else:
                        invalid_keys.append(value)
            elif pattern.match(data[field]):
                valid_keys.append(field)            
            else:
                invalid_keys.append(field)
        else:
            invalid_keys.append(field)

    return {
        "missing_keys": list(missing_keys),
        "valid_keys": valid_keys,
        "invalid_keys": invalid_keys
    }

def is_series_ordered(series):
    # Check if the Series is either equal to its sorted version or its reverse sorted version
     return (series.equals(series.sort_values()) or series.equals(series.sort_values(ascending=False)))

if __name__ == "__main__":

    args = parse_arguments()
    main(args.samplesheet, args.output)
