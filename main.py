"""
    @Author: Bradley Thompson
    @Date: 2022-11-18

    The UK Government collects and publishes detailed traffic accident information across the
    country. The information includes, but is not limited to, weather conditions, accident severity,
    and location information.

    This script downloads the accident, vehicle, and casualties files, and uses the lookup table to
    make the dataset "human-readable" for analysis. Files can be joined using the 'AccidentIndex'
    column present in the datasets.
"""
from enum import Enum

import json
import os
import csv
import wget
import openpyxl


class DatasetProcessor:
    """
    This script downloads the accident, vehicle, and casualties files, and uses the lookup table to
    make the dataset "human-readable" for analysis. Files can be joined using the 'AccidentIndex'
    column present in the datasets.
    """

    class File(Enum):
        """ The files that can be processed"""
        VEHICLES   = "Vehicles"
        ACCIDENTS  = "Accidents"
        CASUALTIES = "Casualties"


    def __init__(self) -> None:
        # Process config.json
        self.config, self.files = self.process_config_file()
        
        # Create folders if they dont exist
        print("\nChecking Folders:")
        for folder in [self.config["download dir"], self.config["processed dir"]]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"{folder} - Created Folder")
            else:
                print(f"{folder} - Already Exists")

        # Download files
        self.download_files()

        # Create lookup dictionary
        self.lookup_dict = self.process_lookups()


    def process_config_file(self) -> None:
        """ Configures The Director And Downloads Missing Files """
        print("\nProcessing config.json:")

        with open('config.json', 'r', encoding='UTF-8') as file:
            json_config = json.load(file)
            config = json_config["Config"]
            files  = json_config["Files"]

        print("Processing Complete")

        return config, files


    def download_files(self) -> None:
        """ Check if the files exist, and download them if they do not """
        print("\nCheck if files have already been downloaded:")
        # Iterate over the files 
        for file in self.files:
            filename = self.files[file]["filename"]

            # Check if file exists locally
            if not os.path.isfile(self.config["download dir"] + "/" + filename):
                print(f"Downloading {filename}")
                downloaded_file = wget.download(self.files[file]["url"], out=self.config["download dir"])
                os.rename(downloaded_file, self.config["download dir"] + "/" + filename)
                print(f"\n Download Complete - {filename} \n")
            else:
                print(f"{filename} already exists")


    def process_lookups(self) -> dict:
        """ Process the Lookup.csv file, trasnforming it into a dictionary """

        print("\nProcessing Lookup File:")

        # Create sets of values to be ignored during processign
        ignore_tables = {table for table in self.files["Lookup"]["ignore table"]}
        ignore_values = {table for table in self.files["Lookup"]["ignore values"]}

        # Load the Excel sheet 
        dataframe = openpyxl.load_workbook(self.config["download dir"] + "/" + self.files["Lookup"]["filename"])["Sheet1"]
        # Create lookup dictionary
        map_cols = {"A": "table", "B": "column", "C": "value", "D": "label"}

        # Iterate through Excel sheet
        lookup_dict = {}
        for row in range(1, dataframe.max_row):
            table, column, value, label = ..., ..., ..., ...

            for col, name in map_cols.items():
                match name:
                    case "table":   table  = str(dataframe[col][row].value)
                    case "column":  column = str(dataframe[col][row].value)
                    case "value":   value  = dataframe[col][row].value
                    case "label":   label  = str(dataframe[col][row].value)

            # Add Table if doesn't exist
            if table not in ignore_tables:
                if table not in lookup_dict:
                    lookup_dict[table] = {}

                # Insert value
                if value not in ignore_values:
                    # Add column if doesn't exist
                    if column not in lookup_dict[table]:
                        lookup_dict[table][str(column)] = {}

                    # Add value
                    lookup_dict[table][column][str(value)] = label

        print("Processed Lookup.xlsx")
        return lookup_dict


    def process_file(self, data_file :File) -> None:
        """ Read a file, replacing keys with values from the lookup file """

        print(f"\nProcessing {data_file.value}")
        # Path of file to be processed
        file_path = f"{self.config['download dir']}/{self.files[data_file.value]['filename']}"

        # Lookup value
        lookup_name = self.files[data_file.value]["lookup"]
        lookup_columns = {key for key in self.lookup_dict[lookup_name].keys()}

        # Processed file
        new_file = True
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader_obj = csv.reader(file)

            # Load desired number of rows into memory, process, and write to .csv
            header = []
            data_content = []

            for row_num, row in enumerate(reader_obj):
                # Record header, or data rows
                if row_num == 0:
                    header = row
                else:
                    data_content.append(row)

                # Process data
                if row_num > 0 and (row_num % self.config["processing_window_size"] == 0):
                    for data_row, vals in enumerate(data_content):
                        for header_col, col in enumerate(header):
                            value = vals[header_col]

                            # if column is in lookup
                            if col in lookup_columns:
                                # if value is in lookup value
                                if value != "-1" and value in self.lookup_dict[lookup_name][col]:
                                    # replace entry with lookup
                                    data_content[data_row][header_col] = self.lookup_dict[lookup_name][col][value]

                            # replace -1 with None
                            if value in {"-1", "NULL"}:
                                data_content[data_row][header_col] = None

                    # Write to file
                    if new_file:
                        self.write_to_file(f"{self.config['processed dir']}/{data_file.value}-processed.csv", data_content, header)
                        new_file = False
                        data_content = []
                    else:
                        self.write_to_file(f"{self.config['processed dir']}/{data_file.value}-processed.csv", data_content)
                        data_content = []

        print(f"Processed {data_file.value}")


    def write_to_file(self, name, content, header=None) -> None:
        """ Write rows to a csv file """
        print(f"Writing to {name}")
        with open(name, 'a', encoding='UTF-8', newline='') as f:
            writer = csv.writer(f, delimiter=',')

            if header is not None: 
                writer.writerow(header)
            writer.writerows(content)
        print("Finished writing")


if __name__ == '__main__':
    # Create new Data Processor
    processor = DatasetProcessor()
    processor.process_file(processor.File.ACCIDENTS)
    processor.process_file(processor.File.CASUALTIES)
    processor.process_file(processor.File.VEHICLES)
