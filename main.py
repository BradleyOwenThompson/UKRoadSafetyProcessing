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

def init():
    """ Configures The Director And Downloads Missing Files """

    # Read config.json
    with open('config.json', 'r', encoding='UTF-8') as file:
        print("Reading config.json")

        json_config = json.load(file)
        temp_dir = json_config["Config"]["Download Dir"]
        data_files = json_config["Files"]

    # Check If The Download Folder Exists
    if not os.path.exists(temp_dir):
        # Create Folder If Doesn't Existit does not exist
        os.makedirs(temp_dir)
        print("New Directory 'temp' Created")

    # Iterate Over Files Required For Processing
    for file in data_files:
        filename = data_files[file]["friendly file name"]
        download_url = data_files[file]["url"]

        # Check If Files Are Downloaded
        if not os.path.isfile(f"{temp_dir}/{filename}"):
            print(f"Downloading {filename}")

            # Download Missing Files
            downloaded_file = wget.download(download_url, out=f"{temp_dir}/")
            os.rename(downloaded_file, f"{temp_dir}/{filename}")

            print(f"\nDownload Complete - {filename}")
        else:
            print(f"File Already Exists - {filename}")


if __name__ == '__main__':
    init()
