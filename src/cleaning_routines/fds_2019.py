from src.cleaning_routines.column_orders import shortform_column_order, longform_column_order
from src.extract import FDS2019CustomParser, extract
from src.load import (ShortformFormatter, CSVWriter, FDS2019CustomFormatter,
                      format_dataset, LongformFormatter, FieldRemover)
from src.transform import transform_2019_fds_data

INPUT_DATA_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\raw_response_data\\all_responses_2019_12_17.csv'
SHORTFORM_OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\cleaned_fds_2019_shortform_data.csv'
LONGFORM_OUTPUT_FILEPATH = 'S:\\Reporting & Data\\First Destination Survey\\2019\\cleaned_fds_2019_longform_data.csv'
MAPPING_FILES_DIR = 'S:\\Reporting & Data\\First Destination Survey\\2019\\value_mapping_files'

mapping_filepaths = {
    'employer_name': f'{MAPPING_FILES_DIR}\\employer_name_mapping.csv',
    'location': f'{MAPPING_FILES_DIR}\\location_mapping.csv',
    'missing_locations': f'{MAPPING_FILES_DIR}\\missing_location_mapping.csv',
    'cont_ed': f'{MAPPING_FILES_DIR}\\cont_ed_data_mapping.csv',
    'jhu_degree': f'{MAPPING_FILES_DIR}\\student_jhu_degree_mapping.csv',
    'demographics': f'{MAPPING_FILES_DIR}\\student_demographic_mapping.csv',
    'job_function': f'{MAPPING_FILES_DIR}\\job_function_mapping.csv',
    'salary': f'{MAPPING_FILES_DIR}\\salary_mapping.csv',
    'outcome': f'{MAPPING_FILES_DIR}\\outcome_mapping.csv',
    'fellowship': f'{MAPPING_FILES_DIR}\\fellowship_recoding.csv'
}

field_remover = FieldRemover(['username', 'email', 'jhed', 'full_name', 'submitted_by'])

def main():
    dataset = extract(INPUT_DATA_FILEPATH, FDS2019CustomParser())
    cleaned_dataset = transform_2019_fds_data(dataset, mapping_filepaths)

    longform_formatter = LongformFormatter(FDS2019CustomFormatter(), longform_column_order)
    formatted_longform_dataset = field_remover.remove_from(format_dataset(cleaned_dataset, longform_formatter))
    CSVWriter(formatted_longform_dataset).write(LONGFORM_OUTPUT_FILEPATH)

    shortform_formatter = ShortformFormatter(FDS2019CustomFormatter(), shortform_column_order)
    formatted_shortform_dataset = format_dataset(cleaned_dataset, shortform_formatter)
    CSVWriter(formatted_shortform_dataset).write(SHORTFORM_OUTPUT_FILEPATH)


if __name__ == '__main__':
    main()
