#Testet är utformat för kontroll2.py att skapa och kontrollera Excel filen


import unittest
import pandas as pd
import os

class TestExcelExport(unittest.TestCase):

    # Create a DataFrame
    def test_export_to_excel(self):
        data = {'Year': [2020], 'Men': [100], 'Women': [150], 'Both': [250]}
        df = pd.DataFrame(data)
        df.to_excel('test_output.xlsx', index=False) # Export the DataFrame to an Excel file

        # Check if file exists
        self.assertTrue(os.path.exists('test_output.xlsx'))  # Check Excel file
        os.remove('test_output.xlsx') 

if __name__ == '__main__':
    unittest.main()