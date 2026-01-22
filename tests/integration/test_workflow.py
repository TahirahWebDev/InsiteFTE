"""
Integration test for end-to-end workflow
"""

import unittest
import tempfile
import os
from pathlib import Path

from scripts.utils.file_handler import move_file
from scripts.utils.sanitizer import sanitize_filename
from scripts.utils.metadata import add_yaml_frontmatter, update_yaml_frontmatter
from scripts.watcher import process_inbox_file


class TestWorkflow(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.inbox_dir = os.path.join(self.temp_dir, "01_Inbox")
        self.needs_action_dir = os.path.join(self.temp_dir, "02_Needs_Action")
        os.makedirs(self.inbox_dir)
        os.makedirs(self.needs_action_dir)
    
    def tearDown(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_processing_workflow(self):
        """Test the full workflow from file creation to metadata addition."""
        # Create a test file in the inbox
        test_file_path = os.path.join(self.inbox_dir, "test_document.md")
        with open(test_file_path, 'w') as f:
            f.write("# Test Document\n\nThis is a test document.\n")
        
        # Process the file as if it was detected in the inbox
        # We'll simulate the processing steps manually since we can't easily mock the full config
        original_path = Path(test_file_path)
        
        # Step 1: Sanitize the filename
        sanitized_name = sanitize_filename(original_path.name)
        sanitized_path = original_path.with_name(sanitized_name)
        
        # If the name changed, we'd move the file (but for this test we'll just continue)
        if str(original_path) != str(sanitized_path):
            # In a real scenario, we'd move the file here
            pass
        
        # Step 2: Add YAML frontmatter with initial metadata
        initial_metadata = {
            'status': 'needs-action',
            'original_filename': original_path.name
        }
        
        result = add_yaml_frontmatter(str(sanitized_path), initial_metadata)
        self.assertTrue(result)
        
        # Step 3: Verify the file has the expected content
        with open(sanitized_path, 'r') as f:
            content = f.read()
        
        self.assertIn('---', content)
        self.assertIn('status: needs-action', content)
        self.assertIn('# Test Document', content)
        
        # Step 4: Update the status to simulate progression through the workflow
        update_result = update_yaml_frontmatter(str(sanitized_path), {'status': 'pending-approval'})
        self.assertTrue(update_result)
        
        # Step 5: Verify the status was updated
        updated_content = open(sanitized_path, 'r').read()
        self.assertIn('status: pending-approval', updated_content)
        
        # Step 6: Move the file to the next folder in the workflow
        target_path = os.path.join(self.needs_action_dir, sanitized_path.name)
        move_result = move_file(sanitized_path, target_path)
        self.assertTrue(move_result)
        self.assertFalse(os.path.exists(sanitized_path))
        self.assertTrue(os.path.exists(target_path))


if __name__ == '__main__':
    unittest.main()