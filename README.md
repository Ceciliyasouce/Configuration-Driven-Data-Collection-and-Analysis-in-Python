# Configuration‑Driven Data Collection and Analysis using Python

## Project purpose
- The project focuses on developing a reproducible, configure-driven Python pipeline that automatically collects annual macroeconomic data from world bank API.
- The project uses TOML configuration file to fully control countries, time and indicator parameters used to fetch data from world bank API.
- This make the pipeline flexible and easy to adapt without changing the code.
- Beyond data collect, the project focus on reshaping the raw API response to make them more interpretable.
- This helps us to easity interpret the underlying data which was done by examining each value added shares country wise.
- Furthermore, CAGR computation gave insight on the trends between advanced and emerging economies over the period.

## Explanation of the TOML configuration
-  The TOML configuration file serves as the single control point for the entire pipeline no code changes are needed to modify what data is collected.
-  It contains three input parameters:
    - countries: a list of country names for which data is fetched. The pipeline automatically maps these names to valid World Bank country codes via the API before making any data requests.
    - time: a dictionary with two keys namely start_year and end_year, defining the time horizon over which data is collected. The pipeline fetches annual data for every year within this range.
    - series: a dictionary of indicators where each key is a human-readable name and the value is the corresponding World Bank indicator code (e.g. "NY.GDP.MKTP.KD"). The pipeline iterates over all indicators and fetches data for each one.
- The main goal of using a config file is to ensure the project is fully reproducible i.e. anyone can modify the countries, time range, or indicators simply by editing the TOML file, without touching the underlying Python code.

## Instructions to run the project
1. Create a virtual environment
    ```bash
    python3 -m venv myvenv
    ```
2. Activate virtual environment
    ```bash
    source myvenv/bin/activate
    ```
3. Install packages
    ```bash
    pip3 install -r requirements.txt
    ```
4. Run the python code 'config_driven_data.py'
    ```bash
    python3 config_driven_data.py
    ```
5. Result
    The code generates two output csv files namely: world_bank_data.csv & summary_table.csv

## Description of output files
1. world_bank_data.csv
    - The world_bank_data.csv is the data fetched from the API using the parameters in TOML configuration file.
    - The missing values in data is handles using forward fill method.
    - So all the missing values are filled in with values from previous year if avaialable, except for start year.
2. summary_table.csv    
    - This table will contain the:
        - Value added shares for industry and manufacturing indicator for start year and end year
        - Growth trends CAGR for all the indicators.
    - In my summary table will have value added shares for industry and manufacturing and CAGR calculation for all the indicators in TOML file.

## Brief discussion of analytical findings
1. Which countries show signs of de‑industrialization?
    - From the summary table it is evident that Italy shows clear de-industrialization where
        - Industry share declining (CAGR = -0.0368)
        - Manufacturing share also declining (CAGR = -0.0516)
        - GDP growth also very low at 0.364.
2. Is manufacturing declining faster than total industry?
    - In Italy, yes manufacturing is declining faster than total industry as we can see:
        - Industry CAGR = -0.036%
        - Manufacturing CAGR = -0.051%
    - Also in Canada, manufacturing is declining faster than total industry which is evident from the calculated figues:
        - Industry CAGR = 1.05%
        - Manufacturing CAGR = -0.35%
    -In other countries like Germany, Netherlands and Denmark the manufacturing industry is actually growing faster.
3. Are trends different between advanced and emerging economies?
    - Yes the trends between advanced and emerging economies are very evident from the above figures.
    - Advanced ecomonies show low growth:
        - Germany: 0.97% GDP CAGR
        - France: 1.18% GDP CAGR
        - Italy: 0.36% GDP CAGR
        - Japan: 0.57% GDP CAGR
    - Emerging economies show high growth:
        - China: 7.80% GDP CAGR
        - Turkiye: 4.73% GDP CAGR
    - Other countires show moderate growth.

## Assumptions and limitations:
    Assumptions:
        - Null values can be handled during data analysis stage, where null values were filled using forward fill method.
        - Country names mismatch could be handled appropriately to ensure correct data retrieval.
        
    Limitations:
        1. Data Availability:
            - 2025 data is not yet avaialable in World Bank API, so it is filled with 2024 values using forward fill.
            - Some countires like US have missing values for all years for indicators Industry and Manufacturing due to which computing value added shares were impossible.
        2. Country Mapping:
            - Country name in TOML must exactly match World Bank API names.
            - Some countires had a different spelling Turkey in TOML and Turkiye in API, caused mapping failure.
                - The country name in TOML file was changed to Turkiye to ensure fetching of data.

## References
1. CAGR formula: https://www.investopedia.com/terms/c/cagr.asp

