#!/usr/bin/env python3
"""Unit tests for the utils module."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test that get_json returns correct JSON response."""
        test_payload = {"payload": True}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json("http://example.com")

        self.assertEqual(result, test_payload)
        mock_get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result and calls method only once."""

        class TestClass:
            """Test class with memoized property."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # Call property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Check the property returns correct value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Check a_method was called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
