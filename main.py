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
import wget
import openpyxl


class DatasetProcessor:
    """
    This script downloads the accident, vehicle, and casualties files, and uses the lookup table to
    make the dataset "human-readable" for analysis. Files can be joined using the 'AccidentIndex'
    column present in the datasets.
    """

    class File(Enum):
        """ Define constants for the files"""

        LOOKUP     = "Lookup"
        VEHICLES   = "Vehicles"
        ACCIDENTS  = "Accidents"
        CASUALTIES = "Casualties"


    def __init__(self) -> None:
        """ Constructor, defining variables """

        # Fields
        self.__temp_dir = None        # type: str
        self.__data_files = {}        # type: dict
        self.lookups = {}             # type: dict

        # Process config.json
        self.__temp_dir, self.__data_files = self.__process_config_file()

        self.__download_data()
        self.lookups = self.__process_lookups()


    def __process_config_file(self) -> None:
        """ Configures The Director And Downloads Missing Files """

        temp_dir = None # type: str
        data_files = {} # type: dict

        # Read config.json
        with open('config.json', 'r', encoding='UTF-8') as file:
            print("Reading config.json")

            json_config = json.load(file)
            temp_dir = json_config["Config"]["Download Dir"]
            data_files = json_config["Files"]

        return temp_dir, data_files


    def __download_data(self) -> None:
        """ Check if the temp folder and data exist, download missing data """

        # Check If The Download Folder Exists
        if not os.path.exists(self.__temp_dir):
            # Create Folder If Doesn't Existit does not exist
            os.makedirs(self.__temp_dir)
            print("New Directory 'temp' Created")

        # Iterate Over Files Required For Processing
        for file in self.__data_files:
            filename = self.__data_files[file]["friendly file name"]
            download_url = self.__data_files[file]["url"]

            # Check If Files Are Downloaded
            if not os.path.isfile(f"{self.__temp_dir}/{filename}"):
                print(f"Downloading {filename}\n")

                # Download Missing Files
                downloaded_file = wget.download(download_url, out=f"{self.__temp_dir}/")
                os.rename(downloaded_file, f"{self.__temp_dir}/{filename}")

                print(f"\n Download Complete - {filename} \n")
            else:
                print(f"File Already Exists - {filename}")


    def __process_lookups(self) -> dict:
        """ Process the Lookup.csv file, trasnforming it into a dictionary """

        print("Processing Lookup.xlsx")

        lookup_dict = {}

        # Load the Excel sheet 
        lookup_path = f"{self.__temp_dir}/{self.__data_files['Lookup']['friendly file name']}"
        dataframe = openpyxl.load_workbook(lookup_path)["Sheet1"]

        # Create lookup dictionary
        map_cols = {"A": "table", "B": "column", "C": "value", "D": "label"}
        
        # Iterate through Excel sheet
        for row in range(1, dataframe.max_row):
            table, column, value, label = ..., ..., ..., ...
            for col, name in map_cols.items():
                match name:
                    case "table":   table = dataframe[col][row].value
                    case "column": column = dataframe[col][row].value
                    case "value":   value = dataframe[col][row].value
                    case "label":   label = dataframe[col][row].value

            # Add Table if doesn't exist 
            if table not in lookup_dict.keys():
                lookup_dict[table] = {}

            # Insert value
            if value is not None :
                # Add Column if doesn't exist
                if column not in lookup_dict[table].keys():
                    lookup_dict[table][column] = {}

                # Add value
                lookup_dict[table][column][value] = label

        print("Completed Processing Lookup.xlsx")

        return lookup_dict



if __name__ == '__main__':
    # Create new Data Processor
    processor = DatasetProcessor()
