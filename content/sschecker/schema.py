"""
SampleSheet schema standard
"""
import re

# Define regular expression patterns for Header
header_patterns = {
    'FileFormatVersion': re.compile(r'^[0-9]+$'),  # Matches one or more digits
    'Investigator Name': re.compile(r'^[A-Za-z ]+$'),  # Assuming alphabetic letters only
    'RunName': re.compile(r'^\d{6}_\d{2}$'),  # Format: 6 digits, underscore, 2 digits
    'Date': re.compile(r'^\d{1,2}/\d{1,2}/\d{4}$'),  # Format: 2 digits, slash, 2 digits, slash, 4 digits
    'InstrumentType': 'NovaSeq6000',
    'InstrumentPlatform': re.compile(r'^\.{3}$'),  # Exactly three dots
    'Assay': re.compile(r'^[A-Z0-9 ]+$'),  # Assuming uppercase letters and digits only
    'Index Adapters': re.compile(r'^[A-Za-z0-9/ ]+$'),  # Alphanumeric, slashes, and spaces
}

settings_patterns = {
    'SoftwareVersion': '1.0.0',
    'AdapterRead1': 'CTGTCTCTTATACACATCTCCGAGCCCACGAGAC',
    'AdapterRead2': 'CTGTCTCTTATACACATCTGACGCTGCCGACGA',
    'AdapterBehavior': 'trim',
    'MinimumTrimmedReadLength': '35',
    'MaskShortReads': '35',
    'OverrideCycles': 'U7N1Y93;I10;I10;U7N1Y93'
}

reads_patterns = {
    'Read1Cycles': '101',
    'Read2Cycles': '101',
    'Index1Cycles': '10',
    'Index2Cycles': '10'
}

site_patterns = {
    'Sequencing Site': 'JHH',
    'Instrument ID': 'A00532'
}

data_patterns = {
    'Sample_ID': re.compile(r'^(?:\d+|NTC)-\d{8}-(D|R)$'),  # Digits-Digits-D or Digits-Digits-R
    'Sample_Name': re.compile(r'^(?:\d+|NTC)-\d{8}-(D|R)$'),  # Same pattern as Sample_ID
    'Index_ID': re.compile(r'^\w+$'),  # One or more word characters
    'index': re.compile(r'^[ACGT]+$'),  # A sequence of A, C, G, or T
    'index2': re.compile(r'^[ACGT]+$'),  # A sequence of A, C, G, or T
    'I7_Index_ID': re.compile(r'^\w+$'),  # One or more word characters
    'I5_Index_ID': re.compile(r'^\w+$'),  # One or more word characters
    'Description': re.compile(r'^(?:\d+|NTC)-(RNA|DNA)+$'),  # Digits-UppercaseLetter(s)
    'Pair_ID': re.compile(r'^(?:\d|NTC)+$'),  # One or more digits
    'Sample_Type': re.compile(r'^(RNA|DNA)+$'),  # One or more uppercase letters
}

bclconvert_settings_patterns = {
    'SoftwareVersion': '3.6.3',
    'AdapterRead1': 'CTGTCTCTTATACACATCTCCGAGCCCACGAGAC',
    'AdapterRead2': 'CTGTCTCTTATACACATCTGACGCTGCCGACGA',
    'AdapterBehavior': 'trim',
    'MinimumTrimmedReadLength': '35',
    'MaskShortReads': '35',
    'OverrideCycles': 'U7N1Y93;I10;I10;U7N1Y93'
}

bclconvert_data_patterns = {
    'Sample_ID': re.compile(r'^(?:\d+|NTC)-\d{8}-[DR]$'),  # Matches the pattern: Digits-Digits-D or Digits-Digits-R
    'index': re.compile(r'^[ACGT]+$'),  # Matches a sequence of A, C, G, or T
    'index2': re.compile(r'^[ACGT]+$'),  # Matches a sequence of A, C, G, or T
}