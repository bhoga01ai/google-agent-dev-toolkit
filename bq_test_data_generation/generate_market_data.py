#!/usr/bin/env python3
"""
Generate sample historical stock market data and upload to BigQuery.

This script creates 10,000 rows of realistic stock market data including:
- Stock symbols (AAPL, GOOGL, MSFT, TSLA, AMZN, etc.)
- Date ranges (last 2 years)
- OHLCV data (Open, High, Low, Close, Volume)
- Additional metrics (market cap, P/E ratio, etc.)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from google.cloud import bigquery
import os

import vertexai
vertexai.init(
    project=os.getenv("GOOGLE_PROJECT_ID"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
)

def generate_stock_data(num_rows=10000):
    """
    Generate realistic stock market data.
    """
    # Stock symbols to use
    symbols = [
        'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'NFLX',
        'AMD', 'INTC', 'CRM', 'ORCL', 'ADBE', 'PYPL', 'UBER', 'LYFT',
        'ZOOM', 'SHOP', 'SQ', 'ROKU', 'TWTR', 'SNAP', 'PINS', 'SPOT',
        'ZM', 'DOCU', 'OKTA', 'SNOW', 'PLTR', 'COIN'
    ]
    
    # Base prices for each symbol (realistic starting points)
    base_prices = {
        'AAPL': 150, 'GOOGL': 2500, 'MSFT': 300, 'TSLA': 800, 'AMZN': 3200,
        'META': 200, 'NVDA': 400, 'NFLX': 400, 'AMD': 100, 'INTC': 50,
        'CRM': 200, 'ORCL': 80, 'ADBE': 500, 'PYPL': 100, 'UBER': 40,
        'LYFT': 30, 'ZOOM': 100, 'SHOP': 1000, 'SQ': 80, 'ROKU': 60,
        'TWTR': 40, 'SNAP': 20, 'PINS': 25, 'SPOT': 150, 'ZM': 100,
        'DOCU': 80, 'OKTA': 100, 'SNOW': 200, 'PLTR': 15, 'COIN': 150
    }
    
    # Generate date range (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    data = []
    
    # Calculate rows per symbol to reach target
    rows_per_symbol = num_rows // len(symbols)
    remaining_rows = num_rows % len(symbols)
    
    for i, symbol in enumerate(symbols):
        # Add extra rows to first few symbols if needed
        symbol_rows = rows_per_symbol + (1 if i < remaining_rows else 0)
        
        # Generate dates for this symbol
        symbol_dates = pd.date_range(start=start_date, end=end_date, periods=symbol_rows)
        
        # Starting price for this symbol
        current_price = base_prices.get(symbol, 100)
        
        for date in symbol_dates:
            # Generate realistic price movement (random walk with drift)
            daily_return = np.random.normal(0.001, 0.02)  # Small positive drift, 2% daily volatility
            current_price *= (1 + daily_return)
            
            # Ensure price doesn't go negative
            current_price = max(current_price, 1.0)
            
            # Generate OHLC data
            close_price = round(current_price, 2)
            
            # Open price (close of previous day with small gap)
            open_price = round(close_price * (1 + np.random.normal(0, 0.005)), 2)
            
            # High and low prices
            daily_range = abs(np.random.normal(0, 0.015))  # Daily range as % of price
            high_price = round(max(open_price, close_price) * (1 + daily_range), 2)
            low_price = round(min(open_price, close_price) * (1 - daily_range), 2)
            
            # Volume (realistic trading volume)
            base_volume = {
                'AAPL': 50000000, 'GOOGL': 1500000, 'MSFT': 30000000, 'TSLA': 25000000,
                'AMZN': 3000000, 'META': 20000000, 'NVDA': 15000000, 'NFLX': 5000000
            }.get(symbol, 1000000)
            
            volume = int(base_volume * (1 + np.random.normal(0, 0.3)))
            volume = max(volume, 100000)  # Minimum volume
            
            # Additional metrics
            market_cap = round(close_price * random.randint(1000000000, 50000000000) / close_price, 0)
            pe_ratio = round(random.uniform(10, 50), 2) if random.random() > 0.1 else None
            dividend_yield = round(random.uniform(0, 0.05), 4) if random.random() > 0.3 else 0
            
            # Market sector
            sectors = {
                'AAPL': 'Technology', 'GOOGL': 'Technology', 'MSFT': 'Technology',
                'TSLA': 'Automotive', 'AMZN': 'E-commerce', 'META': 'Technology',
                'NVDA': 'Technology', 'NFLX': 'Entertainment', 'AMD': 'Technology',
                'INTC': 'Technology', 'CRM': 'Technology', 'ORCL': 'Technology'
            }
            sector = sectors.get(symbol, 'Technology')
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'symbol': symbol,
                'open_price': open_price,
                'high_price': high_price,
                'low_price': low_price,
                'close_price': close_price,
                'volume': volume,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
                'sector': sector,
                'created_at': datetime.now().isoformat()
            })
    
    return pd.DataFrame(data)

def create_bigquery_dataset_and_table(project_id, dataset_id='hist_stock_market', table_id='daily_prices'):
    """
    Create BigQuery dataset and table if they don't exist.
    """
    client = bigquery.Client(project=project_id)
    
    # Create dataset
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists")
    except:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset.description = "Historical stock market data for analysis"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_id}")
    
    # Define table schema
    schema = [
        bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("open_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("high_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("low_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("close_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("volume", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("market_cap", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("pe_ratio", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("dividend_yield", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("sector", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
    ]
    
    # Create table
    table_ref = dataset_ref.table(table_id)
    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists")
    except:
        table = bigquery.Table(table_ref, schema=schema)
        table.description = "Daily stock price data with OHLCV and fundamental metrics"
        client.create_table(table)
        print(f"Created table {table_id}")
    
    return f"{project_id}.{dataset_id}.{table_id}"

def upload_to_bigquery(df, table_id, project_id):
    """
    Upload DataFrame to BigQuery.
    """
    client = bigquery.Client(project=project_id)
    
    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Overwrite existing data
    )
    
    # Upload data
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete
    
    print(f"Uploaded {len(df)} rows to {table_id}")

def main():
    """
    Main function to generate and upload stock market data.
    """
    # Configuration
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCP_PROJECT') or 'myproject-454701'
    DATASET_ID = 'hist_stock_market'
    TABLE_ID = 'daily_prices'
    NUM_ROWS = 10000
    
    print(f"🏗️  Generating {NUM_ROWS} rows of stock market data...")
    
    # Generate data
    df = generate_stock_data(NUM_ROWS)
    
    print(f"✅ Generated {len(df)} rows of data")
    print(f"📊 Data summary:")
    print(f"   - Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   - Symbols: {', '.join(sorted(df['symbol'].unique()))}")
    print(f"   - Average volume: {df['volume'].mean():,.0f}")
    print(f"   - Price range: ${df['close_price'].min():.2f} - ${df['close_price'].max():.2f}")
    
    # Save to CSV for backup
    csv_filename = f"stock_market_data_{NUM_ROWS}_rows.csv"
    df.to_csv(csv_filename, index=False)
    print(f"💾 Saved data to {csv_filename}")
    
    # Upload to BigQuery
    if PROJECT_ID != 'your-project-id':
        print(f"🚀 Uploading to BigQuery project: {PROJECT_ID}")
        
        # Create dataset and table
        full_table_id = create_bigquery_dataset_and_table(PROJECT_ID, DATASET_ID, TABLE_ID)
        
        # Upload data
        upload_to_bigquery(df, full_table_id, PROJECT_ID)
        
        print(f"✅ Successfully uploaded data to BigQuery!")
        print(f"📍 Table location: {full_table_id}")
        print(f"\n🔍 Sample queries to try:")
        print(f"   SELECT * FROM `{full_table_id}` LIMIT 10;")
        print(f"   SELECT symbol, AVG(close_price) as avg_price FROM `{full_table_id}` GROUP BY symbol ORDER BY avg_price DESC;")
        print(f"   SELECT DATE_TRUNC(date, MONTH) as month, AVG(close_price) as avg_price FROM `{full_table_id}` WHERE symbol = 'AAPL' GROUP BY month ORDER BY month;")
    else:
        print("⚠️  Please set GOOGLE_CLOUD_PROJECT environment variable to upload to BigQuery")
        print("   Example: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        print(f"   Data saved locally as {csv_filename}")

if __name__ == "__main__":
    main()