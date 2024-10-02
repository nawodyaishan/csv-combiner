import unittest
import os
import shutil
import pandas as pd
from combine_csv import combine_csv_files, validate_input_directory, validate_output_directory

class TestCombineCSV(unittest.TestCase):
    def setUp(self):
        """Set up directories and files for testing."""
        self.test_input_dir = 'test_input_dir'
        self.test_output_dir = 'test_output_dir'
        os.makedirs(self.test_input_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_input_dir)
        shutil.rmtree(self.test_output_dir)

    def test_successful_combination(self):
        """Test successful combination of CSV files."""
        df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
        df1.to_csv(os.path.join(self.test_input_dir, 'file1.csv'), index=False)
        df2.to_csv(os.path.join(self.test_input_dir, 'file2.csv'), index=False)

        output_file = 'combined.csv'
        combine_csv_files(self.test_input_dir, self.test_output_dir, output_file)

        combined_df = pd.read_csv(os.path.join(self.test_output_dir, output_file))
        self.assertEqual(len(combined_df), 4)
        self.assertListEqual(combined_df['A'].tolist(), [1, 2, 5, 6])

    def test_non_csv_files(self):
        """Test handling of non-CSV files."""
        with open(os.path.join(self.test_input_dir, 'file.txt'), 'w') as f:
            f.write('This is a text file.')

        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df.to_csv(os.path.join(self.test_input_dir, 'file.csv'), index=False)

        output_file = 'combined.csv'
        combine_csv_files(self.test_input_dir, self.test_output_dir, output_file)

        combined_df = pd.read_csv(os.path.join(self.test_output_dir, output_file))
        self.assertEqual(len(combined_df), 2)

    def test_empty_directory(self):
        """Test behavior with an empty directory."""
        output_file = 'combined.csv'
        with self.assertRaises(SystemExit):
            combine_csv_files(self.test_input_dir, self.test_output_dir, output_file)

    def test_invalid_input_directory(self):
        """Test validation of an invalid input directory."""
        invalid_dir = 'non_existent_dir'
        with self.assertRaises(SystemExit):
            validate_input_directory(invalid_dir)

    def test_invalid_output_directory(self):
        """Test validation of an invalid output directory."""
        invalid_dir = '/invalid/output/dir'
        with self.assertRaises(SystemExit):
            validate_output_directory(invalid_dir)

    def test_mismatched_columns(self):
        """Test combining CSV files with mismatched columns."""
        df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
        df1.to_csv(os.path.join(self.test_input_dir, 'file1.csv'), index=False)
        df2.to_csv(os.path.join(self.test_input_dir, 'file2.csv'), index=False)

        output_file = 'combined.csv'
        combine_csv_files(self.test_input_dir, self.test_output_dir, output_file)

        combined_df = pd.read_csv(os.path.join(self.test_output_dir, output_file))
        self.assertEqual(len(combined_df), 4)
        self.assertIn('B', combined_df.columns)
        self.assertIn('C', combined_df.columns)

if __name__ == '__main__':
    unittest.main()
