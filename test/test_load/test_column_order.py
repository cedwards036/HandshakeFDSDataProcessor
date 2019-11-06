import unittest
from collections import OrderedDict

from src.load.column_order import ColumnOrder, NullColumnOrder


class TestColumnOrder(unittest.TestCase):

    def test_returns_empty_ordered_dict_when_given_empty_dict(self):
        self.assertEqual(OrderedDict(), ColumnOrder([]).apply_to({}))

    def test_throws_error_if_column_order_includes_field_not_in_data(self):
        with self.assertRaises(ColumnOrder.UnexpectedColumnNameException):
            ColumnOrder(['field_a']).apply_to({})

    def test_throws_error_if_data_includes_field_not_in_column_order(self):
        with self.assertRaises(ColumnOrder.UnexpectedColumnNameException):
            ColumnOrder([]).apply_to({'field_a': 1})

    def test_with_single_field_row(self):
        self.assertEqual(OrderedDict([('field_a', 1)]), ColumnOrder(['field_a']).apply_to({'field_a': 1}))

    def test_with_multi_field_row(self):
        expected = OrderedDict([('field_a', 1), ('field_b', 2), ('field_c', 3)])
        input_data = {'field_c': 3, 'field_a': 1, 'field_b': 2}
        self.assertEqual(expected, ColumnOrder(['field_a', 'field_b', 'field_c']).apply_to(input_data))


class TestNullColumnOrder(unittest.TestCase):

    def test_returns_empty_ordered_dict_when_given_empty_dict(self):
        self.assertEqual(OrderedDict(), ColumnOrder([]).apply_to({}))

    def test_returns_ordered_dict_equivalent_to_input_dict(self):
        self.assertEqual(OrderedDict([('d', 4), ('a', 1), ('c', 3), ('b', 2)]),
                         NullColumnOrder().apply_to({'d': 4, 'a': 1, 'c': 3, 'b': 2}))
