"""
Unit tests for metadata.py
"""

import unittest
import tempfile
import os
from pathlib import Path

from scripts.utils.metadata import add_yaml_frontmatter, update_yaml_frontmatter, get_yaml_frontmatter


class TestMetadata(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.md")
        
        # Create a test file with some content
        with open(self.test_file, 'w') as f:
            f.write("# Test Document\n\nThis is a test document.\n")
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
    
    def test_add_yaml_frontmatter(self):
        """Test that add_yaml_frontmatter adds frontmatter to a file."""
        metadata = {
            'status': 'needs-action',
            'priority': 'high'
        }
        
        result = add_yaml_frontmatter(self.test_file, metadata)
        self.assertTrue(result)
        
        # Check that the file now has frontmatter
        with open(self.test_file, 'r') as f:
            content = f.read()
        
        self.assertIn('---', content)
        self.assertIn('status: needs-action', content)
        self.assertIn('priority: high', content)
        self.assertIn('# Test Document', content)  # Original content should still be there
    
    def test_update_yaml_frontmatter(self):
        """Test that update_yaml_frontmatter updates existing frontmatter."""
        # First, add some initial frontmatter
        initial_metadata = {
            'status': 'needs-action',
            'priority': 'high'
        }
        add_yaml_frontmatter(self.test_file, initial_metadata)
        
        # Now update the frontmatter
        updates = {
            'status': 'pending-approval',
            'reviewer': 'John Doe'
        }
        
        result = update_yaml_frontmatter(self.test_file, updates)
        self.assertTrue(result)
        
        # Check that the frontmatter was updated
        frontmatter = get_yaml_frontmatter(self.test_file)
        self.assertIsNotNone(frontmatter)
        self.assertEqual(frontmatter.get('status'), 'pending-approval')
        self.assertEqual(frontmatter.get('reviewer'), 'John Doe')
        self.assertEqual(frontmatter.get('priority'), 'high')  # Should still be there
    
    def test_get_yaml_frontmatter(self):
        """Test that get_yaml_frontmatter extracts frontmatter correctly."""
        metadata = {
            'status': 'needs-action',
            'priority': 'high',
            'category': 'meeting-notes'
        }
        
        add_yaml_frontmatter(self.test_file, metadata)
        
        frontmatter = get_yaml_frontmatter(self.test_file)
        self.assertIsNotNone(frontmatter)
        self.assertEqual(frontmatter.get('status'), 'needs-action')
        self.assertEqual(frontmatter.get('priority'), 'high')
        self.assertEqual(frontmatter.get('category'), 'meeting-notes')
        # Check that an ID was added automatically
        self.assertIsNotNone(frontmatter.get('id'))
        self.assertIsNotNone(frontmatter.get('created'))
        self.assertIsNotNone(frontmatter.get('updated'))


if __name__ == '__main__':
    unittest.main()