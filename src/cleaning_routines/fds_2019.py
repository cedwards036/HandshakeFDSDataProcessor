from src.extract import FDS2019CustomParser, extract
from src.load import (ShortformFormatter, CSVWriter, FDS2019CustomFormatter,
                      format_dataset, ColumnOrder, LongformFormatter, FieldRemover)
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

shortform_column_order = ColumnOrder([
    'response_id',
    'username',
    'email',
    'jhed',
    'full_name',
    'jhu_majors',
    'jhu_colleges',
    'gender',
    'is_first_gen',
    'is_pell_eligible',
    'is_urm',
    'visa_status',
    'response_datetime_utc',
    'outcome',
    'employer_name',
    'employer_industry',
    'employment_category',
    'employment_type',
    'job_function',
    'job_title',
    'found_through_handshake',
    'employed_during_education',
    'offer_date',
    'accept_date',
    'start_date',
    'salary',
    'bonus_amount',
    'other_compensation',
    'is_internship',
    'cont_ed_school',
    'cont_ed_level',
    'cont_ed_degree',
    'cont_ed_major',
    'cont_ed_major_group',
    'fellowship_org',
    'fellowship_name',
    'still_looking_option',
    'not_seeking_option',
    'city',
    'state',
    'country',
    'is_jhu',
    'submitted_by',
    'is_knowledge_response',
    'knowledge_source',
    'is_gap_year',
    'internships_unpaid_count',
    'internships_paid_count',
    'internships_all_count',
    'internships_gained_valuable_skills',
    'internships_connected_with_mentor',
    'internships_may_lead_to_future_opps',
    'internships_gained_clarity',
    'research_unpaid_count',
    'research_paid_count',
    'research_all_count',
    'research_gained_valuable_skills',
    'research_connected_with_mentor',
    'research_may_lead_to_future_opps',
    'research_gained_clarity'
])

longform_column_order = ColumnOrder([
    'response_id',
    'username',
    'email',
    'jhed',
    'full_name',
    'jhu_degree',
    'jhu_major',
    'jhu_college',
    'gender',
    'is_first_gen',
    'is_pell_eligible',
    'is_urm',
    'visa_status',
    'response_datetime_utc',
    'outcome',
    'employer_name',
    'employer_industry',
    'employment_category',
    'employment_type',
    'job_function',
    'job_title',
    'found_through_handshake',
    'employed_during_education',
    'offer_date',
    'accept_date',
    'start_date',
    'salary',
    'bonus_amount',
    'other_compensation',
    'is_internship',
    'cont_ed_school',
    'cont_ed_level',
    'cont_ed_degree',
    'cont_ed_major',
    'cont_ed_major_group',
    'fellowship_org',
    'fellowship_name',
    'still_looking_option',
    'not_seeking_option',
    'city',
    'state',
    'country',
    'is_jhu',
    'submitted_by',
    'is_knowledge_response',
    'knowledge_source',
    'is_gap_year',
    'internships_unpaid_count',
    'internships_paid_count',
    'internships_all_count',
    'internships_gained_valuable_skills',
    'internships_connected_with_mentor',
    'internships_may_lead_to_future_opps',
    'internships_gained_clarity',
    'research_unpaid_count',
    'research_paid_count',
    'research_all_count',
    'research_gained_valuable_skills',
    'research_connected_with_mentor',
    'research_may_lead_to_future_opps',
    'research_gained_clarity'
])

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
