# Functions to download data

# Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

# ------------------------------------------------------------------------------------------------------------
def get_list_htmls_EEA (url):
    '''This function takes an url from a query in the European Environment Agency (EEA),
    requests for the htmls to download (csv files) and appends them to a list. It returns the list of htmls.
    Args
    :url: str. the url generated by the query in EEA.
    Return
    :list_of_htmls: list. the list of parsed htmls.
    '''
    res = requests.get(url)
    htmls = res.content
    soup = BeautifulSoup(htmls, 'html.parser')
    list_of_htmls = [i.find('a').get('href') for i in soup.find_all('dt')]
    return list_of_htmls

# ------------------------------------------------------------------------------------------------------------
def save_into_dir_EEA (dir_name, list_htmls):
    '''This function takes a list of csv links and saves the files into the specified directory path
    Args
    :dir_name: str. the directory path.
    :list_htmls: list. the list of csv links to 
    '''
    for i in list_htmls:
        df = pd.read_csv(i)
        df.to_csv(f'../data/EEA/{dir_name}/{i.split("/")[-1]}', index = False)
    return f'files saved successfully!'

# ------------------------------------------------------------------------------------------------------------
def concatenate_csv (dir_name, file_name):
    '''This function concatenates all csv files from a directory path.
    Args
    :dir_name: str. the directory path where the csv files are (path from the current directory).
    :file_name: str. the name of the combined file.
    '''
    # Store the current directory to a variable
    current_dir = os.getcwd()
    # Set working directory to where files are located
    os.chdir(f'../data/EEA/{dir_name}')
    # Match the pattern (‘csv’) and save the list of file names in the ‘all_filenames’ variable
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # Combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # Export to csv
    combined_csv.to_csv(f'{file_name}', index=False, encoding='utf-8-sig')
    # Set working directory back to original
    os.chdir(current_dir)
    return f'files combined successfully!'

# ------------------------------------------------------------------------------------------------------------
def automate_download_pm10 (dict_cities):
    '''This function creates a directory for the specified city and downloads PM10 data from EEA to it
    Args
    :dict_cities: dict. stores de country_code (as key), and the city (as value)
    '''
    for city in dict_cities.values():
        try:
            # create directory
            os.makedirs(f"../data/EEA/{city}")
        except FileExistsError:
            # directory already exists
            pass
    # store current directory
    current_dir = os.getcwd()
    for country, city in dict_cities.items():
        try:
            # request
            url = f'https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?CountryCode={country}&CityName={city}&Pollutant=5&Year_from=2013&Year_to=2022&Station=&Samplingpoint=&Source=E1a&Output=HTML&UpdateDate=&TimeCoverage=Year'
            list_of_htmls = get_list_htmls_EEA(url)
            save_into_dir_EEA(city, list_of_htmls)
            file_name = f'{city}_combined_pm10.csv'
            concatenate_csv(city, file_name)
        except:
            os.chdir(current_dir)
            print(f'An error ocurred during the download of PM10 from {city}')
    return f'files downloaded and combined successfully!'

# ------------------------------------------------------------------------------------------------------------
def automate_download_pm10_nocapital (dict_countries):
    '''This function does the same as the previous one but for the countries without capital in EEA.
    '''
    for country_name in dict_countries.values():
        try:
            os.makedirs(f"../data/EEA/{country_name}")
        except FileExistsError:
            pass
    current_dir = os.getcwd()
    for country_code, country_name in dict_countries.items():
        try:
            url = f'https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?CountryCode={country_code}&CityName=&Pollutant=5&Year_from=2013&Year_to=2022&Station=&Samplingpoint=&Source=E1a&Output=HTML&UpdateDate=&TimeCoverage=Year'
            list_of_htmls = get_list_htmls_EEA(url)
            save_into_dir_EEA(country_name, list_of_htmls)
            file_name = f'{country_name}_combined_pm10.csv'
            concatenate_csv(country_name, file_name)
        except:
            os.chdir(current_dir)
            print(f'An error ocurred during the download of PM10 from {country_name}')
    return f'files downloaded and combined successfully!'