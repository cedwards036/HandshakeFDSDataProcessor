from src.cleaning_routines.column_orders import shortform_column_order, longform_column_order
from src.extract import FDS2019CustomParser, extract
from src.load import (ShortformFormatter, CSVWriter, FDS2019CustomFormatter,
                      format_dataset, LongformFormatter, FieldRemover)
from src.transform import transform_2019_fds_data

UNDERGRAD_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\raw_response_data\\undergrad_responses_2019_11_04_15_11.csv'
SHORTFORM_OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\cleaned_fds_2019_shortform_data.csv'
LONGFORM_OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\cleaned_fds_2019_longform_data.csv'

mapping_filepaths = {
    'employer_name': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\employer_name_mapping.csv',
    'location': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\location_mapping.csv',
    'cont_ed': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\cont_ed_data_mapping.csv',
    'jhu_degree': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\student_jhu_degree_mapping.csv',
    'demographics': 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files\\student_demographic_mapping.csv'
}

field_remover = FieldRemover(['username', 'email', 'jhed', 'full_name', 'submitted_by'])

def main():
    dataset = extract(UNDERGRAD_FILEPATH, FDS2019CustomParser())
    cleaned_dataset = transform_2019_fds_data(dataset, mapping_filepaths)

    longform_formatter = LongformFormatter(FDS2019CustomFormatter(), longform_column_order)
    formatted_longform_dataset = field_remover.remove_from(format_dataset(cleaned_dataset, longform_formatter))
    CSVWriter(formatted_longform_dataset).write(LONGFORM_OUTPUT_FILEPATH)

    shortform_formatter = ShortformFormatter(FDS2019CustomFormatter(), shortform_column_order)
    formatted_shortform_dataset = format_dataset(cleaned_dataset, shortform_formatter)
    CSVWriter(formatted_shortform_dataset).write(SHORTFORM_OUTPUT_FILEPATH)


if __name__ == '__main__':
    main()
