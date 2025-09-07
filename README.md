# Google Agent Development Toolkit

A comprehensive toolkit for developing AI agents using Google's Agent Development Kit (ADK), featuring specialized agents for financial analysis, education, and BigQuery data analytics.

## 🚀 Features

- **BigQuery Data Analyst Agent**: Specialized agent for analyzing financial market data in BigQuery
- **Financial Advisor Agent**: Multi-agent system for comprehensive financial analysis and trading insights
- **Teaching Assistant Agent**: Educational assistant with Google Search integration
- **Test Data Generation**: Tools for generating realistic stock market data for testing
- **Deployment Tools**: Ready-to-use deployment scripts and configurations

## 📁 Project Structure

```
google-agent-dev-toolkit/
├── bq_data_analyst_agent/          # BigQuery data analysis agent
│   ├── __init__.py
│   └── agent.py                    # Main BQ analyst agent configuration
├── bq_test_generation/             # BigQuery test data generation tools
│   ├── generate_market_data.py     # Generate 10K rows of stock market data
│   ├── requirements_market_data.txt # Dependencies for data generation
│   ├── stock_market_data_10000_rows.csv # Generated sample data
│   └── test_bq_analyst_with_data.py # Test script for BQ analyst
├── financial_advisor_agent/        # Multi-agent financial advisor system
│   ├── agent.py                    # Main financial advisor agent
│   ├── prompt.py                   # Agent prompts and instructions
│   └── sub_agents/                 # Specialized sub-agents
│       ├── data_analyst/           # Data analysis sub-agent
│       ├── execution_analyst/      # Trade execution analysis
│       ├── risk_analyst/           # Risk assessment agent
│       └── trading_analyst/        # Trading strategy agent
├── teaching_assistant_agent/       # Educational assistant agent
│   ├── agent.py                    # Teaching assistant configuration
│   └── prompt.py                   # Educational prompts
├── deployment/                     # Deployment tools and scripts
│   ├── deployment.py               # Main deployment script
│   ├── test_curl_example.sh        # API testing script
│   └── test_deployment.py          # Deployment validation
├── test_bq_agent.py               # BigQuery agent testing
└── pyproject.toml                 # Project dependencies and configuration
```

## 🛠️ Setup

### Prerequisites

- Python 3.13+
- Google Cloud Project with BigQuery enabled
- Google Cloud credentials configured
- UV package manager (recommended) or pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd google-agent-dev-toolkit
   ```

2. **Install dependencies:**
   ```bash
   # Using UV (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

   Required environment variables:
   ```
   GOOGLE_PROJECT_ID=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

4. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth application-default login
   ```

## 🤖 Agents Overview

### BigQuery Data Analyst Agent

**Location:** `bq_data_analyst_agent/`

**Purpose:** Specialized agent for analyzing financial market data stored in BigQuery.

**Features:**
- Access to historical stock market dataset (`hist_stock_market.daily_prices`)
- 10,000 rows of data covering 30 major stocks (Sept 2023 - Sept 2025)
- Financial metrics analysis (OHLCV, market cap, P/E ratios, etc.)
- Sector-based analysis and comparisons
- SQL query generation and optimization

**Usage:**
```python
from bq_data_analyst_agent.agent import bq_analyst

session = bq_analyst.create_session()
response = session.send_message("Show me the top performing stocks by average closing price")
```

### Financial Advisor Agent

**Location:** `financial_advisor_agent/`

**Purpose:** Comprehensive financial advisory system with specialized sub-agents.

**Sub-Agents:**
- **Data Analyst**: Market data analysis and trend identification
- **Risk Analyst**: Risk assessment and portfolio analysis
- **Trading Analyst**: Trading strategy development
- **Execution Analyst**: Trade execution optimization

### Teaching Assistant Agent

**Location:** `teaching_assistant_agent/`

**Purpose:** Educational assistant with Google Search integration for up-to-date information.

**Features:**
- Google Search integration for current information
- Educational content delivery
- Student-friendly explanations

## 📊 Test Data Generation

### Generate Stock Market Data

**Location:** `bq_test_generation/`

Generate realistic historical stock market data for testing:

```bash
# Navigate to test generation folder
cd bq_test_generation

# Install dependencies
uv add -r requirements_market_data.txt

# Generate and upload data to BigQuery
uv run generate_market_data.py
```

**Generated Dataset:**
- **Table:** `myproject-454701.hist_stock_market.daily_prices`
- **Rows:** 10,000 records
- **Stocks:** 30 major companies (AAPL, GOOGL, MSFT, TSLA, etc.)
- **Date Range:** September 2023 - September 2025
- **Schema:** Date, Symbol, OHLCV, Market Cap, P/E Ratio, Dividend Yield, Sector

### Test the BQ Analyst

```bash
cd bq_test_generation
uv run test_bq_analyst_with_data.py
```

## 🚀 Deployment

### Local Development

```bash
# Run agent tests
uv run test_bq_agent.py
```

### Production Deployment

```bash
# Navigate to deployment folder
cd deployment

# Deploy to Google Cloud
uv run deployment.py

# Test the deployment
./test_curl_example.sh
```

## 🧪 Testing

### Run Agent Tests

```bash
# Test BigQuery agent
uv run test_bq_agent.py

# Test with generated data
cd bq_test_generation
uv run test_bq_analyst_with_data.py

# Test deployment
cd deployment
uv run test_deployment.py
```

## 📝 Example Queries

### BigQuery Data Analysis Examples

```sql
-- Top performing stocks
SELECT symbol, AVG(close_price) as avg_price 
FROM `myproject-454701.hist_stock_market.daily_prices` 
GROUP BY symbol 
ORDER BY avg_price DESC;

-- Monthly price trends for AAPL
SELECT DATE_TRUNC(date, MONTH) as month, AVG(close_price) as avg_price 
FROM `myproject-454701.hist_stock_market.daily_prices` 
WHERE symbol = 'AAPL' 
GROUP BY month 
ORDER BY month;

-- Volume analysis by sector
SELECT sector, AVG(volume) as avg_volume 
FROM `myproject-454701.hist_stock_market.daily_prices` 
GROUP BY sector 
ORDER BY avg_volume DESC;
```

## 🔧 Configuration

### Agent Configuration

Agents can be configured through their respective `agent.py` files:

- **Model Selection**: Choose from available Gemini models
- **Instructions**: Customize agent behavior and expertise
- **Tools**: Configure available tools and capabilities
- **Temperature**: Adjust response creativity/consistency

### BigQuery Configuration

Configure BigQuery settings in the data generation scripts:

- **Project ID**: Your Google Cloud project
- **Dataset**: Target BigQuery dataset
- **Table Schema**: Customize data structure
- **Data Volume**: Adjust number of generated records

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the existing issues in the repository
2. Review the Google ADK documentation
3. Create a new issue with detailed information

## 🔗 Related Resources

- [Google Agent Development Kit Documentation](https://google.github.io/adk-docs/)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)

---

**Built with ❤️ using Google Agent Development Kit**