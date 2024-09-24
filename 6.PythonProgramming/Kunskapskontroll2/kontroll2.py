# ## Fördjupad Pythonprogrammering
#
# Kunskapskontroll 2
#
# Lidiia Kashevarova 
#
#
# Programmet hämtar data från ett API på SCB webbplats (Utfärdade examina vid universitet och högskolor efter yrkesexamen, kön och läsår https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__UF__UF0550__UF0550C/Historisk11b/table/tableViewLayout1/). Statistiken visar antalet män, antalet kvinnor och det totala antalet män och kvinnor som avlagt läkarexamen under perioden från 1932 till 2023. Programmet skapar en ny dataframe, beräknar andelen kvinnor av det totala antalet och lägger till en kolumn med dessa data, skapar SQL-databas och en tabell, sparar data i Excel tabell, visar SQL-tabell med hjälp av  viewer app. 


import json
import requests
import pandas as pd
import sqlite3  
import logging
from tabulate import tabulate
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk

# Configure logging
logging.basicConfig(
    filename='C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\logfile.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    level=logging.INFO)

# JSON query to SCB API 
url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/UF/UF0550/UF0550C/Historisk11b"
query = {
     "query": [
    {
      "code": "Yrkesexamen",
      "selection": {
        "filter": "item",
        "values": [
          "YLÄKA"
        ]
      }
    },
    {
      "code": "Kon",
      "selection": {
        "filter": "item",
        "values": [
          "1.2",
          "1",
          "2"
        ]
      }
    }
  ],
    "response": {
        "format": "json"  
    }
}


# Fetching and processing data from SCB API

try:
    #Send request to SCB API
    response = requests.post(url, json=query)
    response.raise_for_status()
    
    # Retrieve data from the response
    data = response.json()
    
    # Convert JSON to DataFrame
    df = pd.json_normalize(data['data'], sep='_')
    
    # Export DataFrame to CSV
    df.to_csv("C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\scb_data.csv", index=False, encoding="utf-8-sig")
    logging.info("Data has been exported to CSV file.")
    
    # Exception handling
except requests.exceptions.RequestException as e:
    logging.error(f"Error occurred during the API request: {e}")
    raise



# Reading Data from CSV File
try:
    df = pd.read_csv('C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\scb_data.csv', header=None)
except FileNotFoundError:
    logging.error("CSV file could not be found.")
    raise
except pd.errors.EmptyDataError:
    logging.error("CSV file is empty.")
    raise
except Exception as e:
    logging.error(f"Error reading CSV file: {e}")
    raise



# Create a new DataFrame with the required columns

data = {
    'År': [],
    'Män': [],
    'Kvinnor': [],
    'Båda': []
}

#Processing rows from CSV data
for index, row in df.iterrows():
    # Clean the first column by removing brackets and extra spaces
    try:
        values_str = row[0].strip('[]') 
        if not values_str:
            continue   # Skip empty strings
            
        # Split the string by commas and clean up each value
        values = [v.strip().strip("'") for v in values_str.split(',')]
        
        # If the row doesn't have at least 3 values, log a warning and skip it
        if len(values) < 3:
            logging.warning(f"Skipped row due to unexpected format:{values_str}")
            continue
            
        # Extract key, number, and year from the row
        key = values[0]
        number = values[1]
        year = values[2]
        
         # Process the data based on the value of 'number'
        if number == '1':
            data['År'].append(year)
            data['Män'].append(float(row[1].strip('[]').strip("'")) if not pd.isna(row[1]) else 0) #number of men
            data['Kvinnor'].append(0)
            data['Båda'].append(0)
        elif number == '2':
            data['År'].append(year)
            data['Män'].append(0)
            data['Kvinnor'].append(float(row[1].strip('[]').strip("'")) if not pd.isna(row[1]) else 0)#number of women
            data['Båda'].append(0)
        else:
            data['År'].append(year)
            data['Män'].append(0)
            data['Kvinnor'].append(0)
            data['Båda'].append(float(row[1].strip('[]').strip("'")) if not pd.isna(row[1]) else 0) #total

    # Log an error if something goes wrong while processing a row
    except Exception as e:
        logging.error(f"Error processing row {index}: {e}")




# Create a DataFrame with the new structure
df_new = pd.DataFrame(data)

# Group and sum data by year, keeping the year format
df_grouped = df_new.groupby('År').agg({
    'Män': 'sum',
    'Kvinnor': 'sum',
    'Båda': 'sum'
}).reset_index()

# Calculate the proportion of women
df_grouped['Andel Kvinnor'] = (df_grouped['Kvinnor'] / df_grouped['Båda'] * 100).round(2)

# Display the table
print("Antal medicinska examina utfärdade från 1936 till 2023.")
print(tabulate(df_grouped, headers='keys', tablefmt='fancy_grid', stralign='center'))


# Save DataFrame to SQL-database
db_path = 'C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\medicinska_examin.db'
table_name = 'exam_data'

try:
     # Connect to the SQL-database (creates a new one if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

   # Create the table if it doesn't already exist
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        År TEXT PRIMARY KEY,
        Män REAL,
        Kvinnor REAL,
        Båda REAL,
        Andel_Kvinnor REAL
    )
    """)

    # Write the DataFrame to the table
    df_grouped.to_sql(table_name, conn, if_exists='replace', index=False)
    
     # Commit changes and close the connection
    conn.commit()
    conn.close()

    logging.info("The data has been saved in the SQL database.")
    
 # Log the error if saving data to SQL fails    
except Exception as e:
    logging.error(f"Error saving data to SQL: {e}")
    raise


# Save DataFrame to Excel
try:
    excel_path = 'C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\\\medicinska_examin.xlsx'
    df_grouped.to_excel(excel_path, index=False, engine='openpyxl')
    logging.info(f"Data har exporterats till Excel-fil: {excel_path}")

except Exception as e:
    logging.error(f"Error saving data to Excel: {e}")
    raise


# Viewer app for SQL-tabell

class SQLViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Table Viewer")
        
        # Load data from the SQL-database
        self.df = self.load_data_from_sql()
        
        # Create the Treeview widget
        self.tree = ttk.Treeview(root, columns=[col for col in self.df.columns], show='headings')
        self.tree.pack(expand=True, fill='both')
        
        # Scrollbars 
        vsb = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Set column headers and initial column width
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=tk.NO)  
            
        # Display the results in the Treeview
        self.display_results(self.df)

    def load_data_from_sql(self):
        # # Connect to the SQL-database
        conn = sqlite3.connect('C:\\Users\\lidii\\Documents\\ec\\FP\\kunskapskontroll2\\medicinska_examin.db') 
        query = "SELECT * FROM exam_data"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def display_results(self, df_to_display):
        # Clear previous results from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Visa resultat
        for _, row in df_to_display.iterrows():
            self.tree.insert("", "end", values=row.tolist())


# -

# Create the application window
root = tk.Tk()
app = SQLViewerApp(root)
root.mainloop()




