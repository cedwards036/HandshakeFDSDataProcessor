from collections import OrderedDict
from typing import List


class ColumnOrder:

    def __init__(self, column_order: List[str]):
        self._order = column_order

    def apply_to(self, row: dict) -> OrderedDict:
        if not row and not self._order:
            return OrderedDict()
        return self._convert_row_to_ordered_row(row)

    def _convert_row_to_ordered_row(self, row: dict):
        ordered_row = OrderedDict()
        for col_name in self._order:
            self._record_row_column_value(col_name, ordered_row, row)
        self._ensure_all_row_fields_are_accounted_for_in_column_order(row)
        return ordered_row

    def _record_row_column_value(self, col_name: str, ordered_row: OrderedDict, row: dict):
        if col_name not in row:
            raise self.UnexpectedColumnNameException(f'Column name "{col_name}" is specified in column order but is not in the given row')
        else:
            ordered_row[col_name] = row[col_name]

    def _ensure_all_row_fields_are_accounted_for_in_column_order(self, row: dict):
        for key in row:
            if key not in self._order:
                raise self.UnexpectedColumnNameException(f'Column name "{key}" is specified in the row but is not in the given column order')

    class UnexpectedColumnNameException(Exception):
        pass


class NullColumnOrder(ColumnOrder):

    def __init__(self):
        super().__init__([])

    def apply_to(self, row: dict) -> OrderedDict:
        return OrderedDict(row)
