import pandas as pd
from sqlalchemy import create_engine, text
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

# Directory containing the raw data files
raw_data_dir = 'data/raw/'

engine = create_engine(
	f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
)

def create_raw_schema():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()
        logging.info('Raw schema created or already exists.')

# Map CSV files to table names
datasets = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}


csv_files = glob.glob(os.path.join(raw_data_dir, '*.csv'))


if __name__ == "__main__":
    # Create the raw schema
    create_raw_schema()

    # loop through each CSV file 
    for file in csv_files:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            
            # Extract the table name from the file name
            table_name = datasets.get(os.path.basename(file))
            
            # Load the DataFrame into the PostgreSQL database
            df.to_sql(table_name, engine, schema="raw", if_exists='replace', index=False)
            
            logging.info(f'Successfully loaded {file} into {table_name} table.')
        except Exception as e:
            logging.error(f'Error loading {file}: {e}')