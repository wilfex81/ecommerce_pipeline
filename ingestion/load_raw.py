import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging
import glob

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



load_dotenv()

#connection
db_user = os.getenv('DB_USER', '')
db_password = os.getenv('DB_PASSWORD', '')
db_host = os.getenv('DB_HOST', '')
db_port = os.getenv('DB_PORT', '')
db_name = os.getenv('DB_NAME', '')

engine = create_engine(
	f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
)

# Directory containing the raw data files
raw_data_dir = 'data/raw/'
csv_files = glob.glob(os.path.join(raw_data_dir, '*.csv'))

# loop through each CSV file 
for file in csv_files:
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        
        # Extract the table name from the file name
        table_name = os.path.splitext(os.path.basename(file))[0]
        
        # Load the DataFrame into the PostgreSQL database
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        logging.info(f'Successfully loaded {file} into {table_name} table.')
    except Exception as e:
        logging.error(f'Error loading {file}: {e}')