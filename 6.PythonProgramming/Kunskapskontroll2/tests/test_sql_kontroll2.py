#Testet är utformat för kontroll2.py att testa interaktion med SQL-databasen, inklusive att ansluta och skapa tabeller


import unittest
import sqlite3
import pandas as pd
import os 

# Defines a new test case class which contain the test methods 
class TestSQLDatabase(unittest.TestCase):
    
    def setUp(self):
        self.db_path = 'test_database.db'
        self.conn = sqlite3.connect(self.db_path)  #Create a connection to the SQL database
        self.cursor = self.conn.cursor()
        # Create a table for testing 
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_data (
                År TEXT PRIMARY KEY,
                Män REAL,
                Kvinnor REAL,
                Båda REAL,
                Andel_Kvinnor REAL
            )
        """)
        self.conn.commit()
        
    # Test the insertion of data into the database
    def test_insert_data(self):
        data = pd.DataFrame({
            'År': ['2020'],
            'Män': [100],
            'Kvinnor': [150],
            'Båda': [250],
            'Andel_Kvinnor': [60.0]
        })
        
        # Insert the sample data into the database table
        data.to_sql('exam_data', self.conn, if_exists='replace', index=False)
        
        # to verify the insertion
        result = self.cursor.execute('SELECT * FROM exam_data').fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], '2020')  # Year should be 2020

    # Check that test database exists and remove it 
    def tearDown(self):
        self.conn.close()
        os.remove(self.db_path)

if __name__ == '__main__':
    unittest.main()