#Testet är utformat för kontroll2.py  att kontrollera CSV-filens bearbetning 

import unittest
import pandas as pd
import os

class TestCSVHandling(unittest.TestCase):
    
    # Test reading from a CSV file
    def test_csv_reading(self):
        df = pd.read_csv('scb_data.csv')  # Read the CSV file into a DataFrame
        self.assertIsInstance(df, pd.DataFrame) # Check if the result is an instance of pandas DataFrame
        self.assertFalse(df.empty) # Check if the DataFrame is not empty
     # Test writing to a CSV file
    def test_csv_writing(self):
        data = {'Year': [2020], 'Men': [10], 'Women': [15], 'Both': [25]}
        df = pd.DataFrame(data)
        df.to_csv('test_output.csv', index=False)
        
        # Check if the file exists
        self.assertTrue(os.path.exists('test_output.csv'))
        os.remove('test_output.csv') 
        
    # Test for handling non-existent CSV file    
    def test_csv_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            pd.read_csv('non_existent_file.csv')

if __name__ == '__main__':
    unittest.main()