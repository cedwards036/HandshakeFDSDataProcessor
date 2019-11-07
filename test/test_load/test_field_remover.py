import unittest
from collections import OrderedDict

from src.load.field_remover import FieldRemover


class TestFieldRemover(unittest.TestCase):

    def test_removes_no_fields_if_given_no_fields_to_remove(self):
        remover = FieldRemover([])
        input_data = [{'a': 1, 'b': 2, 'c': 3}]
        self.assertEqual(input_data, remover.remove_from(input_data))

    def test_throws_error_if_input_row_doesnt_contain_a_field_to_be_removed(self):
        remover = FieldRemover(['a', 'b'])
        input_data = [{'a': 1, 'b': 2}, {'a': 1}]
        with self.assertRaises(FieldRemover.MissingFieldException):
            remover.remove_from(input_data)

    def test_removes_single_field_from_single_row(self):
        remover = FieldRemover(['b'])
        input_data = [{'a': 1, 'b': 2, 'c': 3}]
        expected = [{'a': 1, 'c': 3}]
        self.assertEqual(expected, remover.remove_from(input_data))

    def test_removes_multiple_fields_from_single_row(self):
        remover = FieldRemover(['b', 'd', 'e'])
        input_data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
        expected = [{'a': 1, 'c': 3}]
        self.assertEqual(expected, remover.remove_from(input_data))

    def test_removes_all_fields_from_row(self):
        remover = FieldRemover(['a', 'b', 'c'])
        input_data = [{'a': 1, 'b': 2, 'c': 3}]
        expected = [{}]
        self.assertEqual(expected, remover.remove_from(input_data))

    def test_removes_fields_from_multiple_rows(self):
        remover = FieldRemover(['a', 'c', 'e'])
        input_data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5},
                      {'a': 11, 'b': 12, 'c': 13, 'd': 14, 'e': 15},
                      {'a': 21, 'b': 22, 'c': 23, 'd': 24, 'e': 25}]
        expected = [{'b': 2, 'd': 4},
                    {'b': 12, 'd': 14},
                    {'b': 22, 'd': 24}]
        self.assertEqual(expected, remover.remove_from(input_data))

    def test_field_remover_preserves_order_for_ordered_dict(self):
        remover = FieldRemover(['b', 'd', ])
        input_data = [OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 3)])]
        expected = [OrderedDict([('a', 1), ('c', 3), ('e', 3)])]
        self.assertEqual(expected, remover.remove_from(input_data))
