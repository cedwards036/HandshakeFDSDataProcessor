import unittest

from src.survey_data_model import JHUDegree
from src.transform.value_map import ValueMap
from src.transform.value_map import ValueMapBuilder


class TestDegreeMapBuilder(unittest.TestCase):
    def test_build_empty_map(self):
        self.assertEqual(ValueMap(), ValueMapBuilder.build_jhu_degree_map([]))

    def test_build_single_degree_mapping(self):
        mapping_data = [{'email': 'astu24@jhu.edu', 'degree': 'B.S.', 'major': 'Computer Science', 'college': 'Whiting School of Engineering'}]
        expected = ValueMap()
        expected.add_mapping('astu24@jhu.edu', [JHUDegree(degree='B.S.', major='Computer Science', college='Whiting School of Engineering')])
        self.assertEqual(expected, ValueMapBuilder.build_jhu_degree_map(mapping_data))

    def test_build_multi_degree_mapping(self):
        mapping_data = [{'email': 'astu24@jhu.edu', 'degree': 'B.S.', 'major': 'Computer Science', 'college': 'Whiting School of Engineering'},
                        {'email': 'astu24@jhu.edu', 'degree': 'B.S.', 'major': 'Mech Eng', 'college': 'Whiting School of Engineering'},
                        {'email': 'astu24@jhu.edu', 'degree': 'B.A.', 'major': 'English', 'college': 'Krieger School of Arts and Sciences'}]
        expected = ValueMap()
        expected.add_mapping('astu24@jhu.edu', [JHUDegree(degree='B.S.', major='Computer Science', college='Whiting School of Engineering'),
                                                JHUDegree(degree='B.S.', major='Mech Eng', college='Whiting School of Engineering'),
                                                JHUDegree(degree='B.A.', major='English', college='Krieger School of Arts and Sciences')])
        self.assertEqual(expected, ValueMapBuilder.build_jhu_degree_map(mapping_data))

    def test_build_multi_student_mapping(self):
        mapping_data = [{'email': 'bstu13@jhu.edu', 'degree': 'B.A.', 'major': 'Mathematics', 'college': 'Krieger School of Arts and Sciences'},
                        {'email': 'astu24@jhu.edu', 'degree': 'B.S.', 'major': 'Mech Eng', 'college': 'Whiting School of Engineering'},
                        {'email': 'astu24@jhu.edu', 'degree': 'B.A.', 'major': 'English', 'college': 'Krieger School of Arts and Sciences'},
                        {'email': 'cstu9@jhu.edu', 'degree': 'B.S.', 'major': 'Electrical Engineering', 'college': 'Whiting School of Engineering'},
                        {'email': 'cstu9@jhu.edu', 'degree': 'B.A.', 'major': 'Writing Seminars', 'college': 'Krieger School of Arts and Sciences'}]
        expected = ValueMap()
        expected.add_mapping('bstu13@jhu.edu', [JHUDegree(degree='B.A.', major='Mathematics', college='Krieger School of Arts and Sciences')])
        expected.add_mapping('astu24@jhu.edu', [JHUDegree(degree='B.S.', major='Mech Eng', college='Whiting School of Engineering'),
                                                JHUDegree(degree='B.A.', major='English', college='Krieger School of Arts and Sciences')])
        expected.add_mapping('cstu9@jhu.edu', [JHUDegree(degree='B.S.', major='Electrical Engineering', college='Whiting School of Engineering'),
                                               JHUDegree(degree='B.A.', major='Writing Seminars', college='Krieger School of Arts and Sciences')])
        self.assertEqual(expected, ValueMapBuilder.build_jhu_degree_map(mapping_data))
