import requests
import pandas as pd
import toml
import numpy as np

# Fetch country codes from World Bank API
def get_country_codes():
    url = f"http://api.worldbank.org/v2/country"  
    params = {"format": "json", "per_page": 300}
    
    response = requests.get(url, params=params)
    countries = response.json()[1]
    return countries

# Fetch data from the API using config.toml and covert into a dataframe
def data_fetching(base_url):
    for i in wb['countries']['list']:
        for key, value in wb['series'].items():
            country.append(i)
            indicator.append(value)
            url = f"{base_url}/{country_code[i]}/indicator/{value}"
            
            # Fetch all years at once
            params = {
                "date": f"{wb['time']['start_year']}:{wb['time']['end_year']}", 
                "format": "json",
                "per_page": 1000
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            #error
            if data[1] is not None:
                for r in data[1]:
                    year_data[f"year_{r['date']}"].append(r['value'] if r['value'] is not None else np.nan)
            else:
                for year in range(wb['time']['start_year'], wb['time']['end_year'] + 1):
                    year_data[f"year_{year}"].append(np.nan)
    df = pd.DataFrame(
        {
            "country": country,
            "indicator": indicator,
            **year_data  # unpacks all the year columns            
        }
    )
    return df

#Value added shares computation
def share_computation(df, indicator, key, gdp):
    year_cols = [col for col in df.columns if col.startswith('year_')]
    share_ind = df[df['indicator'] == indicator]
    share_ind = share_ind[['country'] + year_cols]
    share_ind = share_ind.set_index('country')
    # Get GDP values
    gdp_shares = df[df['indicator'] == gdp]
    gdp_shares = gdp_shares[['country'] + year_cols].set_index('country')
    # Divide by GDP to get actual share
    share_ind = (share_ind / gdp_shares) * 100
    col_name = key.split('_')[0] + '_shares'
    share_ind.columns = [f"{col_name}_{col.split('_')[1]}" for col in share_ind.columns]
    return share_ind

#Compound annual growth rate (CAGR)
def CAGR(start_year, end_year, df, key, values):
    #Get data
    year_cols = [col for col in df.columns if col.startswith('year_')]
    temp_df = df[df['indicator'] == values][['country'] + year_cols].set_index('country')
    # Calculate CAGR
    cagr = ((temp_df[f"year_{end_year}"] / temp_df[f"year_{start_year}"]) ** (1/(end_year-start_year)) -1) * 100
    cagr.name = f"{key.split('_')[0]}_CAGR"
    return cagr.to_frame()

#Summary table
def summary_table(df, start_year, end_year):
    #rename columns
    cols = [col for col in df.columns if col.endswith(str(start_year)) or 
                                      col.endswith(str(end_year)) or 
                                      col.endswith('CAGR')]

    compact = df[cols]
    return compact
    

if __name__=="__main__":

    # 1) Data Collection Requirements
    print('1) Data Collection started')
    # Load config
    with open("config.toml", "r") as f:
        wb = toml.load(f)

    #get all the country details from the API and map the Country code with respective Country
    count_code = get_country_codes()

    #Mapping the country code and country
    country_code = {}
    for i in count_code:
        if i['name'] in wb['countries']['list']:
            country_code[i['name']] = i['iso2Code']

    # creating list to first create a list, then dataframe by combining them
    country = []
    indicator = []
    year_data = {}
    for year in range(wb["time"]["start_year"], wb["time"]["end_year"] + 1):
        year_data[f"year_{year}"] = []

    print("2) Fetching data from the API and storing in dataframe")
    #Data Fetching
    base_url = 'http://api.worldbank.org/v2/country'
    data_frame = data_fetching(base_url)

    #Handling missing values
    year_cols = [col for col in data_frame.columns if col.startswith('year_')]
    data_frame[year_cols] = data_frame[year_cols].ffill(axis=1)

    #convert the dataframe into CSV file and save it locally
    data_frame.to_csv('world_bank_data.csv')
    print("3) Data Collection completed, please find the data stored as 'world_bank_data.csv'")

    # 2) Analysis Task

    #load the csv file
    print("4) Data Analysis task begun")
    df_data = pd.read_csv('world_bank_data.csv', sep = ',')

    #Value‑added shares
    print("5) Value added shared computation")
    new_df = pd.DataFrame()

    for key, values in wb['series'].items():
        if key.startswith('gdp'):
            gdp = values
            break

    for key, values in wb['series'].items():
        if not key.startswith('gdp'):
            print(f"    Calculating value added share for {key}")
            #error from here, add columns inside exiting df
            if new_df.empty:
                new_df = share_computation(df_data, wb['series'][key], key, gdp)
            else:
                new_df = new_df.merge(share_computation(df_data, wb['series'][key], key, gdp), left_index=True, right_index=True)

    #Growth trends (2000–2025)
    
    print(f"6) Growth trends CAGR computation from {wb['time']['start_year']} to {wb['time']['end_year']}")
    for key, values in wb['series'].items():
        print(f"    Calculating CAGR for {key}")
        new_df = new_df.merge(CAGR(wb['time']['start_year'], wb['time']['end_year'], df_data, key, values), left_index=True, right_index=True)
    
    # 3) Summary table
    print("7) Creating Summary table")
    summary_df = summary_table(new_df, wb['time']['start_year'], wb['time']['end_year'])

    #convert into CSV
    summary_df.to_csv('summary_table.csv')
    print("8) Summary table is available as 'summary_table.csv'")