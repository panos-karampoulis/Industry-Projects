# Energy Market Reporting & Analytics Pipeline

## Project Overview

This project implements an end-to-end data analytics pipeline for an energy trading environment.

The goal is to transform raw market data stored in a MySQL data warehouse into business-ready insights through automated data extraction, analysis, visualization, and reporting.

The project combines SQL, Python, Pandas, Excel automation, and data visualization techniques to simulate a real-world Data Analyst / BI Analyst workflow.

---

## Architecture

```
MySQL Data Warehouse
        |
        |
        v
SQLAlchemy Data Connection
        |
        |
        v
Python Analytics Pipeline
        |
        |
        +----------------+
        |                |
        v                v
   Pandas Analysis   Visualization
        |                |
        +----------------+
                 |
                 v
        Automated Excel Report
```

---

## Technologies Used

* Python 3
* MySQL
* SQLAlchemy
* Pandas
* Matplotlib
* OpenPyXL
* Excel Reporting
* Git / GitHub

---

## Project Structure

```
Energy-Market-Reporting

├── config
│   └── config.example.py
│
├── python
│   ├── database.py
│   ├── extract_data.py
│   ├── create_charts.py
│   ├── generate_report.py
│   └── create_excel_report.py
│
├── sql
│
├── charts
│   ├── market_volume.png
│   ├── trader_pnl.png
│   └── renewable_mix.png
│
├── reports
│
├── requirements.txt
│
└── README.md
```

---

## Database Views Used

The project consumes analytical views from the `energy_dw` database:

### Executive Dashboard

`vw_executive_dashboard`

Provides:

* Total trades
* Total traded volume
* Total trade value
* Net P&L

---

### Market Analysis

`vw_market_analysis`

Provides:

* Trading volume by market
* Trade value
* Average trade price

Markets analyzed:

* Day Ahead Market
* Intraday Market
* Balancing Market
* Forward Market
* Ancillary Services

---

### Trader Performance

`vw_trader_performance`

Provides:

* Trader activity
* Trading volume
* Profit & Loss performance

---

### Renewable Analysis

`vw_renewable_analysis`

Provides:

* Renewable trading volume
* Non-renewable trading volume
* Market value distribution

---

## Automated Reporting

The pipeline generates an Excel report containing:

### Executive Summary

Key business metrics:

* Total Trades
* Total Volume
* Total Trade Value
* Net P&L

### Market Analysis

Includes market-level trading performance.

### Trader Performance

Includes trader-level P&L analysis.

### Renewable Analysis

Includes renewable energy contribution analysis.

---

## Visualizations

The project automatically creates:

### Market Trading Volume

Shows trading volume distribution across energy markets.

### Trader P&L Performance

Shows trader profitability analysis.

### Renewable Energy Mix

Shows renewable vs non-renewable trading activity.

---

## How To Run

### 1. Clone repository

```
git clone <repository-url>
```

### 2. Create virtual environment

```
python -m venv .venv
```

### 3. Activate environment

Windows:

```
.venv\Scripts\activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Configure database

Create:

```
config/config.py
```

based on:

```
config/config.example.py
```

Add your MySQL credentials.

---

### 6. Run pipeline

Generate charts:

```
python python/create_charts.py
```

Generate Excel report:

```
python python/create_excel_report.py
```

---

## Business Insights Generated

The analysis provides visibility into:

* Energy market activity
* Trading volume distribution
* Trader performance
* Profitability trends
* Renewable energy participation

---

## Skills Demonstrated

* SQL Data Warehousing
* Database Integration
* Python Automation
* Data Cleaning & Transformation
* Business Intelligence Reporting
* Data Visualization
* Excel Automation
* Analytics Pipeline Development

---

## Future Improvements

Possible extensions:

* Power BI dashboard integration
* Automated scheduled reporting
* Cloud database deployment
* Machine learning forecasting models
* Market price prediction analysis

---
