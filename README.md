# UK Road Safety Data Processing
Processing of Road Safety Data published by The Department Of Transport found on [GOV.UK](https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data).

The UK Government collects and publishes detailed traffic accident information across the country ([Here](https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data)). The information includes, but is not limited to, weather conditions, accident severity, and location information.

This script downloads the accident, vehicle, and casualties files and uses the lookup table to make the dataset "human-readable" for analysis. Files can be joined using the 'AccidentIndex' column in the datasets.

## Files Used:
* Road Safety Data - Casualties 1979 - 2021 
* Road Safety Data - Vehicles 1979 - 2021 
* Road Safety Data - Accidents 1979 - 2021
* Road Safety Open Dataset Data Guide

