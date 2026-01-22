"""
Unit tests for file_handler.py
"""

import unittest
import tempfile
import os
from pathlib import Path

from scripts.utils.file_handler import move_file, copy_file, ensure_directory_exists, is_valid_file_type


class TestFileHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.source_file = os.path.join(self.temp_dir, "test.txt")
        self.dest_file = os.path.join(self.temp_dir, "moved_test.txt")
        
        # Create a test file
        with open(self.source_file, 'w') as f:
            f.write("Test content")
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove test files and directory
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
        if os.path.exists(self.dest_file):
            os.remove(self.dest_file)
        os.rmdir(self.temp_dir)
    
    def test_move_file_success(self):
        """Test that move_file successfully moves a file."""
        result = move_file(self.source_file, self.dest_file)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.dest_file))
    
    def test_copy_file_success(self):
        """Test that copy_file successfully copies a file."""
        result = copy_file(self.source_file, self.dest_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.dest_file))
        
        # Check that content is the same
        with open(self.source_file, 'r') as f1, open(self.dest_file, 'r') as f2:
            self.assertEqual(f1.read(), f2.read())
    
    def test_ensure_directory_exists(self):
        """Test that ensure_directory_exists creates a directory."""
        new_dir = os.path.join(self.temp_dir, "new_dir")
        result = ensure_directory_exists(new_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(new_dir))
    
    def test_is_valid_file_type_txt(self):
        """Test that is_valid_file_type returns True for .txt files."""
        self.assertTrue(is_valid_file_type("test.txt"))
    
    def test_is_valid_file_type_md(self):
        """Test that is_valid_file_type returns True for .md files."""
        self.assertTrue(is_valid_file_type("test.md"))
    
    def test_is_valid_file_type_invalid(self):
        """Test that is_valid_file_type returns False for invalid files."""
        self.assertFalse(is_valid_file_type("test.pdf"))
        self.assertFalse(is_valid_file_type("test.jpg"))


if __name__ == '__main__':
    unittest.main()