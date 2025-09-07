#!/usr/bin/env python3
"""
Test the BigQuery Data Analyst Agent with the generated historical stock market data.

This script demonstrates how to use the BQ analyst agent to query and analyze
the hist_stock_market dataset that was just created.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bq_data_analyst_agent.agent import create_bq_data_analyst_agent

def test_stock_analysis():
    """
    Test the BQ analyst agent with stock market data queries.
    """
    print("🤖 Initializing BigQuery Data Analyst Agent...")
    
    # Create the agent
    agent = create_bq_data_analyst_agent()
    
    # Create a session
    session = agent.create_session()
    print(f"📋 Created session: {session.name}")
    
    # Test queries for the stock market data
    test_queries = [
        {
            "name": "Basic Data Overview",
            "query": "Can you show me the first 10 rows from the hist_stock_market.daily_prices table to understand the data structure?"
        },
        {
            "name": "Top Performing Stocks",
            "query": "Which stocks have the highest average closing price in the hist_stock_market dataset? Show me the top 10."
        },
        {
            "name": "Volume Analysis",
            "query": "What are the average trading volumes by sector in the hist_stock_market data? Order by volume descending."
        },
        {
            "name": "Price Trend Analysis",
            "query": "Show me the monthly average closing price trend for AAPL over the time period in the dataset."
        },
        {
            "name": "Market Summary",
            "query": "Give me a summary of the hist_stock_market dataset including total number of records, date range, number of unique symbols, and overall price statistics."
        }
    ]
    
    print("\n🔍 Running test queries...\n")
    
    for i, test in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*60}")
        print(f"Query: {test['query']}")
        print("\nResponse:")
        print("-" * 40)
        
        try:
            # Send query to the agent
            response = session.send_message(test['query'])
            
            # Display the response
            if hasattr(response, 'text'):
                print(response.text)
            else:
                print(str(response))
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n")
    
    print("✅ All tests completed!")
    print(f"\n📊 Dataset Info:")
    print(f"   - Table: myproject-454701.hist_stock_market.daily_prices")
    print(f"   - Rows: 10,000")
    print(f"   - Symbols: 30 major stocks")
    print(f"   - Date Range: 2023-09-07 to 2025-09-06")
    print(f"   - Columns: date, symbol, OHLCV data, market_cap, pe_ratio, dividend_yield, sector")

def main():
    """
    Main function to run the BQ analyst tests.
    """
    print("🚀 Testing BigQuery Data Analyst Agent with Stock Market Data")
    print("=" * 70)
    
    try:
        test_stock_analysis()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)