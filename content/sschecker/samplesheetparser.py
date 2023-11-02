"""
Classes for parsing files used in, and produced by, Illumina's TSO500 app
"""
from collections import Counter, ChainMap
from functools import reduce
import re
from typing import Dict, List, Any

import pandas as pd

# from constants import TMB_FIELDS, MSI_FIELDS
from exceptions import DuplicateKeyError

JSONType = Dict[Dict[str, Any], List[Dict[str, Any]]]


class IlluminaFile(object):
    """
    Class for handling the contents of files outputted
    by the TSO500 local app.

    This class should not be directly used - derived classes are
    available for different types of output (e.g. the samplesheet
    and combined variant output), which should be used to interact
    with those files instead.

    Attributes:
        filename: path to file
        json: contents of the file as a dict

    Refer to derived classes for examples of usage.
    """
    def __init__(self,
                 filename: str = None,
                 delim: str = None,
                 skip: int = 0,
                 tabular_sections: List[str] = [],
                 array_sections: List[str] = []) -> None:
        """
        Inits IlluminaFile with filename, delimiter, the number of
        lines to skip (due to boilerplate lines at the top of some
        output files), and lists of sections to be handled in specific ways
        by `IlluminaFile._read()`. I.e.:

            - `tabular sections` are handled as delimiter-separated data;
            - `array sections` are handled as simple lists of data

        Note that derived classes set many of these arguments as defaults,
        not to be set by the user.

        Args:
            filename: path to file
            delim: file delimiter (e.g. `","` `"\t"` etc.)
            skip: number of lines to skip over before parsing the file
            tabular_sections: List of sections where the data is formatted as
                delimiter-separated data
            array_sections: List of sections where the data is formatted as
                a simple list of entries
        """
        self.filename = filename
        self._tabular_sections = tabular_sections
        self._array_sections = array_sections
        self._delim = delim
        self._skip = skip
        self.json = None

    @property
    def json(self) -> JSONType:
        """
        Contents of file as a dict
        """
        return self._json

    @json.setter
    def json(self, val):
        if val is None:
            self._json = self._read()

    def _read(self) -> str:
        """
        Reads the contents of the imported file into a dict
        """
        with open(self.filename, "r") as f:
            file_contents = {}

            # some files have license/use info at the top. Skip these lines
            if self._skip > 0:
                [next(f) for i in range(self._skip)]

            for line in f:
                line = line.rstrip("\n")

                # skip over lines entirely made of delimiters; these are section breaks
                if re.match(f"^{self._delim}+$", line):
                    continue

                # handle section header
                # a header is always expected to be the first line of a section
                elif line[0] == "[":
                    header = self._extract_header(line)

                    if header in self._tabular_sections:
                        # section head followed by column names. Go to next line in
                        # file here and extract column names. The rest of the
                        # lines can be handled like normal tabular data (CSV, TSV etc.)
                        column_names = f.readline().rstrip().split(self._delim)
                        file_contents[header] = []
                        data_type = "tabular"
                    elif header in self._array_sections:
                        file_contents[header] = []
                        data_type = "array"
                    else:
                        file_contents[header] = {}
                        data_type = "record"

                # handle section data
                else:
                    row = line.split(self._delim)
                    if data_type == "tabular":
                        if len(row) < len(column_names):
                            n_missing_values = len(column_names) - len(row)
                            row += ["NA" for i in range(n_missing_values)]
                        delimited_row = dict(zip(column_names, row))
                        file_contents[header].append(delimited_row)

                    elif data_type == "array":
                        value = row[0]
                        file_contents[header].append(value)

                    else:
                        # i.e. data_type == "record"
                        # Non-TSV formatted KV pairs can be dict'd normally
                        key = row[0]
                        value = row[1]
                        file_contents[header][key] = value

        return file_contents

    @staticmethod
    def _extract_header(header_string: str) -> str:
        """
        Extracts the name of the section header as a string
        """
        return re.search("\[(.+)\]", header_string).group(1)

class IndexSheet(IlluminaFile):
    """
    Class for parsing TSO500-specific index file `TSO-novaseq_UDP_v1.5_chemistry.csv` files.
    Reads the data into JSON format, and allows interaction with
    section data via attributes.

    Basic usage:

        >>> from tso500samplesheetchecker.samplesheetparser import IndexSheet
        >>> samplesheet = IndexSheet("TSO-novaseq_UDP_v1.5_chemistry.csv")
        >>> samplesheet.header

    Attributes:
        filename: path to file
        header: samplesheet header (i.e. analysis metadata)
        reads: read lengths
        settings: various program-specific settings
        data: index data
    """
    def __init__(self, filename):
        super().__init__(
                filename,
                delim=",",
                # TSO customized setting tag
                tabular_sections=["Data"],
                array_sections=[],
                skip=0)
        self.header = None
        self.reads = None
        self.settings = None
        self.site = None
        self.data = None
        self.bclconvert_settings = None
        self.bclconvert_data = None

    @property
    def header(self) -> dict:
        """
        Returns samplesheet header
        """
        return self._header

    @header.setter
    def header(self, val):
        if val is None:
            self._header = self.json["Header"]

    @property
    def reads(self) -> dict:
        """
        Returns read lengths
        """
        return self._reads

    @reads.setter
    def reads(self, val):
        if val is None:
            self._reads = self.json["Reads"]
            
    @property
    def settings(self) -> dict:
        """
        Returns analysis settings
        """
        return self._settings

    @settings.setter
    def settings(self, val):
        if val is None:
            # TSO customized setting tag
            self._settings = self.json["Settings"]

    @property
    def data(self) -> JSONType:
        """
        Returns samplesheet data
        """
        return self._data

    @data.setter
    def data(self, val):
        if val is None:
            # TSO customized setting tag
            self._data = self.json["Data"]                
            
class SampleSheet(IlluminaFile):
    """
    Class for parsing TSO500-specific `*_SampleSheet.csv` files.
    Reads the data into JSON format, and allows interaction with
    section data via attributes.

    Basic usage:

        >>> from tso500samplesheetchecker.samplesheetparser import SampleSheet
        >>> samplesheet = SampleSheet("SampleSheet.csv")
        >>> samplesheet.header

    Attributes:
        filename: path to file
        header: samplesheet header (i.e. analysis metadata)
        reads: read lengths
        tso500s_settings: various program-specific settings
        nswhp: nswhp specific info
        tso500s_data: samplesheet data
        bclconvert_settings: bclconvert settings
        bclconvert_data: bclconvert data
    """
    def __init__(self, filename):
        super().__init__(
                filename,
                delim=",",
                # TSO customized setting tag
                tabular_sections=["TSO500S_Data", "BCLConvert_Data"],
                array_sections=[],
                skip=0)
        self.header = None
        self.reads = None
        self.settings = None
        self.site = None
        self.data = None
        self.bclconvert_settings = None
        self.bclconvert_data = None

    @property
    def header(self) -> dict:
        """
        Returns samplesheet header
        """
        return self._header

    @header.setter
    def header(self, val):
        if val is None:
            self._header = self.json["Header"]

    @property
    def reads(self) -> dict:
        """
        Returns read lengths
        """
        return self._reads

    @reads.setter
    def reads(self, val):
        if val is None:
            self._reads = self.json["Reads"]

    @property
    def settings(self) -> dict:
        """
        Returns analysis settings
        """
        return self._settings

    @settings.setter
    def settings(self, val):
        if val is None:
            # TSO customized setting tag
            self._settings = self.json["TSO500S_Settings"]
    
    @property
    def site(self) -> dict:
        """
        Returns site info
        """
        return self._site
    
    @site.setter
    def site(self, val):
        if val is None:
            self._site = self.json["NSWHP"]

    @property
    def data(self) -> JSONType:
        """
        Returns samplesheet data
        """
        return self._data

    @data.setter
    def data(self, val):
        if val is None:
            # TSO customized setting tag
            self._data = self.json["TSO500S_Data"]
            
    @property
    def bclconvert_settings(self) -> JSONType:
        """
        Returns bclconvert_settings data
        """
        return self._bclconvert_settings
    
    @bclconvert_settings.setter
    def bclconvert_settings(self, val):
        if val is None:
            # TSO customized setting tag
            self._bclconvert_settings = self.json["BCLConvert_Settings"]

    @property
    def bclconvert_data(self) -> JSONType:
        """
        Returns bclconvert data
        """
        return self._bclconvert_data

    @bclconvert_data.setter
    def bclconvert_data(self, val):
        if val is None:
            # TSO customized setting tag
            self._bclconvert_data = self.json["BCLConvert_Data"]
    
def find_duplicate_keys(record: Dict[str, Dict]) -> List:
    """
    finds duplicated keys in a dict of dicts
    """
    all_keys = reduce(lambda x, y: x + list(y.keys()), record, [])
    key_counts = Counter(all_keys)
    duplicate_keys = list(filter(lambda x: key_counts[x] > 1, key_counts))
    return duplicate_keys


def flatten_record(record: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Flattens list of dicts to single dict

    Args:
        record: List of dicts

    Returns:
        a single, flattened dict
    """
    duplicate_keys = find_duplicate_keys(record)

    if len(duplicate_keys) > 0:
        raise DuplicateKeyError(duplicate_keys)

    chain_map = ChainMap(*record)
    return dict(chain_map)


def parse_samplesheet_data(filepath: str) -> pd.DataFrame:
    """
    Parses the TSO500 `*SampleSheet.csv` file, returning the contents
    of the *[Data]* section (i.e., the sample data) as a `pd.DataFrame` object.

    Args:
        filepath: path to samplesheet file

    Returns:
        Contents of *[Data]* section as a `pd.DataFrame` object
    """
    samplesheet = SampleSheet(filepath).data
    return pd.DataFrame(samplesheet)

def parse_index_data(filepath: str) -> pd.DataFrame:
    """
    Parses the TSO500 index `TSO-novaseq-UDP_v1.5_chemistry.csv` file, 
    returning the contents
    of the *[Data]* section (i.e., the sample data) as a `pd.DataFrame` object.

    Args:
        filepath: path to samplesheet file

    Returns:
        Contents of *[Data]* section as a `pd.DataFrame` object
    """
    indexsheet = IndexSheet(filepath).data
    return pd.DataFrame(indexsheet)