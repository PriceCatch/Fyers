'''
Copyright (c) 2025 S V SUDHARSHAN a.k.a PriceCatch.
visit http://github.com/PriceCatch for more code and info.
Watch my technical analysis videos at https://www.youtube.com/@PriceCatch

Licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.

Attribution:
- The first two lines must be placed in comments at the header of your code.

- purpose: This script will retain only EQ and BE series symbols from the Symbols Master Json.
- This json file is available at this url: https://public.fyers.in/sym_details/NSE_CM_sym_master.json
- The filtered json file is used in my other scripts for fetching historical data and live data.
'''
import json
import os

INPUT_JSON_FILE_PATH = "/Users/svsud/Downloads/NSE_CM_sym_master.json"
OUTPUT_JSON_FILE_PATH = "/Users/svsud/Downloads/filtered_nse_cm_sym_master.json"

# --- Filtering Logic ---
def filter_nse_master_data(file_path: str) -> list:
    """
    Loads JSON data (assumed to be a dictionary) and filters records 
    based on exSeries, tradeStatus, and isin criteria.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"An error occurred during file reading: {e}")
        return []

    # 3. Prepare Records to Process
    if isinstance(data, dict):
        # extract values from the json dictionary
        records_to_process = list(data.values())
        print(f"Total original records found (from dictionary values): {len(records_to_process)}")
    elif isinstance(data, list):
        # If the root is a list, process it directly
        records_to_process = data
        print(f"Total original records found (from list): {len(records_to_process)}")
    else:
        print("Error: JSON root is neither a dictionary nor a list. Cannot process.")
        return []

    # Filter Function
    def passes_filters(record: dict) -> bool:
        ex_series = record.get('exSeries')
        trade_status = record.get('tradeStatus')
        isin = record.get('isin')

        # Criteria 1: exSeries must be "EQ" or "BE"
        series_match = (ex_series in ["EQ", "BE"])

        # Criteria 2: tradeStatus must be 1
        status_match = (trade_status == 1)

        # Criteria 3: isin must start with "INE" or "INF"
        isin_match = (
            isinstance(isin, str) and 
            (isin.startswith("INE") or isin.startswith("INF"))
        )

        return series_match and status_match and isin_match

    # 4. Apply Filters
    filtered_data = [record for record in records_to_process if passes_filters(record)]

    return filtered_data

# Execute

retained_data = filter_nse_master_data(INPUT_JSON_FILE_PATH)

print(f"Total records retained after filtering: {len(retained_data)}")

with open(OUTPUT_JSON_FILE_PATH, 'w', encoding='utf-8') as f:
    json.dump(retained_data, f, indent=4)

# EOF.
