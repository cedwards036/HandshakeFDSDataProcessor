from src.extract import FDS2019CustomParser, extract
from src.load import SimpleOutputFormatter, CSVWriter, FDS2019CustomFormatter, format_dataset
from src.transform import transform_2019_fds_data


UNDERGRAD_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\extra_data_gathering\\undergrad_responses_2019_10_29_11_38.csv'
LOCATION_MAP_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\location_mapping.csv'
OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\fds_2019_cleaned_data.csv'


def main():
    dataset = extract(UNDERGRAD_FILEPATH, FDS2019CustomParser())
    cleaned_dataset = transform_2019_fds_data(dataset, LOCATION_MAP_FILEPATH)
    response_formatter = SimpleOutputFormatter(FDS2019CustomFormatter())
    formatted_dataset = format_dataset(cleaned_dataset, response_formatter)
    CSVWriter(formatted_dataset).write(OUTPUT_FILEPATH)


if __name__ == '__main__':
    main()
