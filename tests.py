import unittest
from compressor import ObjectCompressor


class CompressionTests(unittest.TestCase):
    """
    This is a class unit tests for compress/decompress functions
    """
    def setUp(self):
        self.object_compressor = ObjectCompressor()
        self.example_dictionary = {'one': {'two': 3, 'four': [5, 6, 7]}, 'eight': {'nine': {'ten': 11}}}
        self.example_dictionary_compressed = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11}

        self.custom_object = MyCustomObject()
        self.custom_object.one = MyCustomObject()
        self.custom_object.one.two = 3
        self.custom_object.one.four = [5, 6, 7]
        self.custom_object.eight = MyCustomObject()
        self.custom_object.eight.nine = MyCustomObject()
        self.custom_object.eight.nine.ten = 11

    def test_example_case_compression(self):
        compressed_version = self.object_compressor.compress(self.example_dictionary)
        self.assertEqual(self.example_dictionary_compressed, compressed_version)

    def test_example_caseDecompression(self):
        decompressed_version = self.object_compressor.decompress(self.example_dictionary_compressed)
        self.assertEqual(self.example_dictionary, decompressed_version)

    def test_example_case_compression_and_decompression(self):
        compressed_version = self.object_compressor.compress(self.example_dictionary)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(self.example_dictionary, decompressed_version)

    def test_middle_array_compression(self):
        dictionary_with_middle_array = {'one': {'two': 3, 'four': [{'a': 2.3, 'b': None}, 'c']}, 'eight': {'nine': {'ten': 11}}}
        middle_array_compressed = {'one/two': 3, 'one/four/0/a': 2.3, 'one/four/0/b': None, 'one/four/1': 'c', 'eight/nine/ten': 11}
        compressed_version = self.object_compressor.compress(dictionary_with_middle_array)
        self.assertEqual(middle_array_compressed, compressed_version)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(dictionary_with_middle_array, decompressed_version)

    def test_top_array_compression(self):
        array_object = [{'two': 3}, {'four': [{'a': 2.3, 'b': None}, 'c']}, {'eight': {'nine': {'ten': 11}}}]
        top_array_compressed = {'0/two': 3, '1/four/0/a': 2.3, '1/four/0/b': None, '1/four/1': 'c', '2/eight/nine/ten': 11}
        compressed_version = self.object_compressor.compress(array_object)
        self.assertEqual(top_array_compressed, compressed_version)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(array_object, decompressed_version)

    def test_empty_array_compression(self):
        dictionary_with_empty_array = {'one': {'two': 3, 'four': []}, 'eight': {'nine': {'ten': 11}}}
        empty_dictionary_compressed = {'one/two': 3, 'one/four': [], 'eight/nine/ten': 11}
        compressed_version = self.object_compressor.compress(dictionary_with_empty_array)
        self.assertEqual(empty_dictionary_compressed, compressed_version)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(dictionary_with_empty_array, decompressed_version)

    def test_empty_object_compression(self):
        dictionary_with_empty_container = {'one': {'two': 3, 'four': [5, 6, 7]}, 'eight': {'nine': {}}}
        empty_dictionary_compressed = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine': {}}
        compressed_version = self.object_compressor.compress(dictionary_with_empty_container)
        self.assertEqual(empty_dictionary_compressed, compressed_version)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(dictionary_with_empty_container, decompressed_version)

    def test_string_and_bool_and_float_compression(self):
        object_to_test = {'a': {'d': True}, 'b': 'myString', 'c': 21.89}
        decompressed_object_to_test = {'a/d': True, 'b': 'myString', 'c': 21.89}
        compressed_version = self.object_compressor.compress(object_to_test)
        self.assertEqual(decompressed_object_to_test, compressed_version)
        decompressed_version = self.object_compressor.decompress(compressed_version)
        self.assertEqual(object_to_test, decompressed_version)

    def test_empty_top_level_object_compression(self):
        compressed_version = self.object_compressor.compress({})
        self.assertEqual({}, compressed_version)

    def test_single_value_compression(self):
        compressed_version = self.object_compressor.compress({'a': 1})
        self.assertEqual({'a': 1}, compressed_version)

    def test_single_value_empty_object_compression(self):
        compressed_version = self.object_compressor.compress({'a': {}})
        self.assertEqual({'a': {}}, compressed_version)

    def test_single_value_empty_array_compression(self):
        compressed_version = self.object_compressor.compress({'a': []})
        self.assertEqual({'a': []}, compressed_version)

    def test_empty_top_level_array_compression(self):
        compressed_version = self.object_compressor.compress([])
        self.assertEqual({}, compressed_version)

    def test_single_array_compression(self):
        compressed_version = self.object_compressor.compress({'a': [0, 1, 2]})
        self.assertEqual({'a/0': 0, 'a/1': 1, 'a/2': 2}, compressed_version)

    # These are the tests using a custom Python object instead of dictionary/List as a container
    def test_custom_object_compression(self):
        compressed_version = self.object_compressor.compress(self.custom_object)
        self.assertEqual(self.example_dictionary_compressed, compressed_version)

    def test_empty_array_custom_object_compression(self):
        empty_dictionary_compressed = {'one/two': 3, 'one/four': [], 'eight/nine/ten': 11}
        self.custom_object.one.four = []
        compressed_version = self.object_compressor.compress(self.custom_object)
        self.assertEqual(empty_dictionary_compressed, compressed_version)
        self.custom_object.one.four = [5, 6, 7]

    def test_empty_object_custom_object_compression(self):
        self.custom_object.eight.nine = MyCustomObject()
        empty_object_compressed = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine': {}}
        compressed_version = self.object_compressor.compress(self.custom_object)
        self.assertEqual(empty_object_compressed, compressed_version)
        self.custom_object.eight.nine.ten = 11


class MyCustomObject:
    def __init__(self):
        return


if __name__ == '__main__':
    unittest.main()
