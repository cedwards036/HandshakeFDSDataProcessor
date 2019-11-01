from src.extract import FDS2019CustomParser, extract
from src.load import SimpleOutputFormatter, CSVWriter, FDS2019CustomFormatter, format_dataset
from src.transform import transform_2019_fds_data

UNDERGRAD_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\raw_response_data\\undergrad_responses_2019_11_01_02_15.csv'
OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\fds_2019_cleaned_data.csv'

mapping_filepaths = {
    'employer_name': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\employer_name_mapping.csv',
    'location': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\location_mapping.csv',
    'cont_ed': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\cont_ed_data_mapping.csv'
}

def main():
    dataset = extract(UNDERGRAD_FILEPATH, FDS2019CustomParser())
    cleaned_dataset = transform_2019_fds_data(dataset, mapping_filepaths)
    response_formatter = SimpleOutputFormatter(FDS2019CustomFormatter())
    formatted_dataset = format_dataset(cleaned_dataset, response_formatter)
    CSVWriter(formatted_dataset).write(OUTPUT_FILEPATH)


if __name__ == '__main__':
    main()
