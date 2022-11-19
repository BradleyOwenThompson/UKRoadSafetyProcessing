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
import json
import os
import wget

class DatasetProcessor:
    """
    This script downloads the accident, vehicle, and casualties files, and uses the lookup table to
    make the dataset "human-readable" for analysis. Files can be joined using the 'AccidentIndex'
    column present in the datasets.
    """

    def __init__(self) -> None:
        """ Constructor, defining variables """

        self.__temp_dir = None        # type: str
        self.__data_files = {}        # type: dict

        # Process config.json
        self.__process_config_file()
        self.__check_data_exists()

    
    def __process_config_file(self) -> None:
        """ Configures The Director And Downloads Missing Files """

        # Read config.json
        with open('config.json', 'r', encoding='UTF-8') as file:
            print("Reading config.json")

            json_config = json.load(file)
            self.__temp_dir = json_config["Config"]["Download Dir"]
            self.__data_files = json_config["Files"]

    
    def __check_data_exists(self) -> None:
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


if __name__ == '__main__':
    # Create new Data Processor
    processor = DatasetProcessor()
