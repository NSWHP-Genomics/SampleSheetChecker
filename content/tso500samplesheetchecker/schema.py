"""
SampleSheet schema standard
"""

# Define regular expression patterns for Header
header_patterns = {
    'FileFormatVersion': r'^[0-9]+$',
    'Investigator Name': r'^[A-Z]+$',  # Assuming uppercase letters only
    'RunName': r'^\d{6}_\d{2}$',  # Format: 6 digits, underscore, 2 digits
    'Date': r'^\d{2}/\d{2}/\d{4}$',  # Format: 2 digits, slash, 2 digits, slash, 4 digits
    'InstrumentType': r'^[A-Za-z0-9 ]+$',
    'InstrumentPlatform': r'^\.{3}$',  # Exactly three dots
    'Assay': r'^[A-Z0-9 ]+$',  # Assuming uppercase letters and digits only
    'Index Adapters': r'^[A-Za-z0-9/ ]+$',  # Alphanumeric, slashes, and spaces
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

nswhp_patterns = {
    'Sequencing Site': 'JHH',
    'Instrument ID': 'A00532'
}

data_patterns = {
    'Sample_ID': r'^\d+-\d{8}-(D|R)$',  # Matches the pattern: Digits-Digits-D or Digits-Digits-R
    'Sample_Name': r'^\d+-\d{8}-(D|R)$',  # Matches the same pattern as Sample_ID
    'Sample_Plate': r'^\w+$',  # Matches one or more word characters
    'Sample_Well': r'^\w+$',  # Matches one or more word characters
    'Index_ID': r'^\w+$',  # Matches one or more word characters
    'index': r'^[ACGT]+$',  # Matches a sequence of A, C, G, or T
    'index2': r'^[ACGT]+$',  # Matches a sequence of A, C, G, or T
    'I7_Index_ID': r'^\w+$',  # Matches one or more word characters
    'I5_Index_ID': r'^\w+$',  # Matches one or more word characters
    'Project': r'^[\w\s-]+$',  # Matches word characters, spaces, and hyphens
    'Description': r'^\d+-[A-Z]+$',  # Matches the pattern: Digits-UppercaseLetter(s)
    'Pair_ID': r'^\d+$',  # Matches one or more digits
    'Sample_Type': r'^[A-Z]+$',  # Matches one or more uppercase letters
}

bclconvert_patterns = {
    'SoftwareVersion': '3.6.3',
    'AdapterRead1': 'CTGTCTCTTATACACATCTCCGAGCCCACGAGAC',
    'AdapterRead2': 'CTGTCTCTTATACACATCTGACGCTGCCGACGA',
    'AdapterBehavior': 'trim',
    'MinimumTrimmedReadLength': '35',
    'MaskShortReads': '35',
    'OverrideCycles': 'U7N1Y93;I10;I10;U7N1Y93'
}

bclconvert_data_patterns = {
    'Sample_ID': r'^\d+-\d{8}-[DR]$',  # Matches the pattern: Digits-Digits-D or Digits-Digits-R
    'index': r'^[ACGT]+$',  # Matches a sequence of A, C, G, or T
    'index2': r'^[ACGT]+$',  # Matches a sequence of A, C, G, or T
}