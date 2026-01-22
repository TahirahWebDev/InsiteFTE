"""
Unit tests for sanitizer.py
"""

import unittest
import os
from pathlib import Path

from scripts.utils.sanitizer import sanitize_filename, handle_duplicate_filename


class TestSanitizer(unittest.TestCase):
    
    def test_sanitize_filename_removes_invalid_chars(self):
        """Test that sanitize_filename removes invalid characters."""
        # Test with various invalid characters
        invalid_names = [
            "test<file>.txt",
            'test"file".txt',
            "test|file.txt",
            "test?file.txt",
            "test*file.txt",
            "test/file.txt",
            "test\\file.txt"
        ]
        
        for name in invalid_names:
            sanitized = sanitize_filename(name)
            # Check that invalid characters are replaced with underscores
            self.assertNotIn('<', sanitized)
            self.assertNotIn('>', sanitized)
            self.assertNotIn('"', sanitized)
            self.assertNotIn('|', sanitized)
            self.assertNotIn('?', sanitized)
            self.assertNotIn('*', sanitized)
            self.assertNotIn('/', sanitized)
            self.assertNotIn('\\', sanitized)
    
    def test_sanitize_filename_preserves_valid_chars(self):
        """Test that sanitize_filename preserves valid characters."""
        valid_name = "test_file-name with spaces (and) symbols!.txt"
        sanitized = sanitize_filename(valid_name)
        # Most characters should remain the same
        self.assertIn('test', sanitized)
        self.assertIn('file', sanitized)
        self.assertIn('-', sanitized)
        self.assertIn('_', sanitized)
        self.assertIn(' ', sanitized)
        self.assertIn('(', sanitized)
        self.assertIn(')', sanitized)
        self.assertIn('!', sanitized)
        self.assertIn('.txt', sanitized)
    
    def test_sanitize_filename_handles_leading_trailing_spaces(self):
        """Test that sanitize_filename handles leading/trailing spaces and periods."""
        name_with_spaces = " .test_file. "
        sanitized = sanitize_filename(name_with_spaces)
        # Leading/trailing spaces and periods should be stripped
        self.assertFalse(sanitized.startswith(' '))
        self.assertFalse(sanitized.endswith(' '))
        self.assertFalse(sanitized.startswith('.'))
        self.assertFalse(sanitized.endswith('.'))
    
    def test_sanitize_filename_empty_result(self):
        """Test that sanitize_filename handles cases that would result in empty string."""
        # This should generate a default name
        empty_result = sanitize_filename("<>?:\"{}|\\\\")  # All invalid chars
        self.assertGreater(len(empty_result), 0)
        self.assertIn("unnamed_file_", empty_result)


if __name__ == '__main__':
    unittest.main()