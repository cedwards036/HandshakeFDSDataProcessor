from typing import List


class FieldRemover:

    def __init__(self, fields_to_remove: List[str]):
        self._fields = fields_to_remove

    def remove_from(self, rows: List[dict]) -> List[dict]:
        return [self._create_row_copy_with_fields_removed(row) for row in rows]

    def _create_row_copy_with_fields_removed(self, row: dict) -> dict:
        row_copy = row.copy()
        for field in self._fields:
            self._remove_field_from_row_copy(field, row_copy)
        return row_copy

    def _remove_field_from_row_copy(self, field: str, row_copy: dict):
        if field not in row_copy:
            raise self.MissingFieldException(f'Field {field} is not in row, and therefore cannot be removed')
        else:
            del row_copy[field]

    class MissingFieldException(Exception):
        pass
