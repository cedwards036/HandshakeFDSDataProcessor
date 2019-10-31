from src.extract import FDS2019CustomParser
from src.extract import extract

UNDERGRAD_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\extra_data_gathering\\undergrad_responses_2019_10_29_11_38.csv'


def main():
    dataset = extract(UNDERGRAD_FILEPATH, FDS2019CustomParser())
    dataset.apply(lambda response: print(response.to_dict()))

if __name__ == '__main__':
    main()
