from src.response_dataset import ResponseDataset


def assert_response_datasets_are_equal(test_obj, expected: ResponseDataset, actual: ResponseDataset):
    test_obj.assertEqual(expected.to_list_of_dict(), actual.to_list_of_dict())
