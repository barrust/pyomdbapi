"""Unit tests for utility helpers."""

import unittest

from omdb.utilities import camelcase_to_snake_case


class TestCamelcaseToSnakeCase(unittest.TestCase):
    def test_basic_camel_case(self):
        self.assertEqual(camelcase_to_snake_case("CamelCase"), "camel_case")

    def test_existing_omdb_key(self):
        self.assertEqual(camelcase_to_snake_case("imdbID"), "imdb_id")

    def test_acronym_boundary(self):
        self.assertEqual(camelcase_to_snake_case("HTTPServerError"), "http_server_error")

    def test_lowercase_input(self):
        self.assertEqual(camelcase_to_snake_case("already_snake"), "already_snake")

    def test_long_string(self):
        s = "ThisIsALongCamelCaseString" * 1000
        res = ["this_is_a_long_camel_case_string"] * 1000
        self.assertEqual(
            camelcase_to_snake_case(s), "_".join(res)
        )


if __name__ == "__main__":
    unittest.main()
