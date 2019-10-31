from src.extract import FDS2019CustomParser, extract
from src.load import SimpleOutputFormatter, CSVWriter


UNDERGRAD_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\extra_data_gathering\\undergrad_responses_2019_10_29_11_38.csv'
OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\fds_2019_cleaned_data.csv'


def main():
    dataset = extract(UNDERGRAD_FILEPATH, FDS2019CustomParser())
    dataset.apply(lambda response: print(response.to_dict()))
    formatted_dataset = [SimpleOutputFormatter(response).format() for response in dataset]
    CSVWriter(formatted_dataset).write(OUTPUT_FILEPATH)


if __name__ == '__main__':
    main()
