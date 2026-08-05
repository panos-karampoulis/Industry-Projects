# ⚡ Energy Trading Decision Support System

## AI-Based Electricity Market Analytics, Forecasting & Trading Intelligence Platform

---

## 📌 Overview

The **Energy Trading Decision Support System** is an end-to-end analytics platform designed to support electricity market decision-making through:

- Electricity demand forecasting
- Renewable generation analysis
- Day-ahead market price analytics
- Imbalance risk assessment
- Trading signal generation
- Strategy backtesting
- Portfolio performance analysis

The project combines **energy market analytics, machine learning, statistical modelling and financial risk management** into an interactive Streamlit application.

The objective is to simulate a real-world **Energy Trading Analyst / Quantitative Analyst workflow**, where market participants need to forecast system conditions, evaluate risks and support trading decisions.

---

# 🎯 Business Problem

Electricity markets are highly dynamic due to:

- Demand fluctuations
- Renewable generation uncertainty
- Weather dependency
- Market volatility
- Grid imbalance costs
- Price spikes and negative prices

Energy traders and analysts need tools that can answer:

- How will electricity demand evolve?
- What is the expected renewable penetration?
- Is the system exposed to imbalance risk?
- Are market prices likely to increase or decrease?
- Which trading decisions have historically generated value?

This platform provides a data-driven framework to address these questions.

---

# 🏗️ System Architecture


             Energy Market Data
                     |
                     |
                     v

          Data Processing Pipeline

                     |
    ---------------------------------
    |               |               |
    v               v               v

Load Forecasting Price Analytics Risk Engine

    |               |               |

    ---------------------------------

                     |

          Trading Decision Engine

                     |

          Backtesting Framework

                     |

          Streamlit Analytics Dashboard

---

# 🚀 Main Features

## 1. ⚡ Load Forecasting Analytics

Forecast electricity demand using machine learning techniques.

Capabilities:

- Historical load analysis
- Forecast comparison
- Forecast error calculation
- Feature importance analysis

Models evaluated:

- Linear Regression
- Random Forest
- XGBoost
- Prophet


Example features:

- Load lag variables
- Rolling statistics
- Seasonal features
- Renewable generation
- Market prices

---

# 2. 📈 Electricity Market Price Analysis

Analysis of electricity market behaviour:

- Day-ahead prices
- Intraday prices
- Price volatility
- Price spikes
- Negative price events


The system evaluates market conditions using historical price patterns and statistical indicators.

---

# 3. 🌱 Renewable Generation Analytics

Renewable generation monitoring:

- Wind generation
- Solar generation
- Renewable penetration
- Residual load analysis


Key indicators:


Residual Load =
Electricity Demand - Renewable Generation


Residual load is a critical driver of electricity price formation.

---

# 4. ⚠️ Imbalance Risk Engine

The imbalance module estimates operational risk caused by differences between expected and actual system conditions.

Risk factors:

- Load forecast error
- Renewable uncertainty
- Residual load changes
- Market volatility


Outputs:

- Risk score
- Risk category:


LOW
MEDIUM
HIGH


---

# 5. 💹 Trading Decision Engine

The platform generates simulated trading recommendations:

Signals:


BUY
SELL
HOLD



Based on:

- Market price behaviour
- Risk conditions
- Forecast information
- System fundamentals


The goal is not automated trading execution but **decision support**.

---

# 6. 📊 Strategy Backtesting

Historical strategy evaluation:

Metrics:

- Total PnL
- Daily PnL
- Sharpe Ratio
- Profit Factor
- Equity Curve
- Trading frequency


The framework evaluates whether generated signals could have produced historical value.

---

# 7. 📈 Trade Analytics Dashboard

Detailed trading performance analysis:

Includes:

- PnL by signal
- PnL by risk category
- Hourly performance
- Best trading hours
- Worst trading hours
- Country comparison


---

# 🖥️ Streamlit Application


The project contains a multi-page interactive dashboard:


pages/

1_Load_Forecasting.py
2_Imbalance_Risk.py
3_Trading_Decisions.py
4_Market_Comparison.py
5_Model_Performance.py
6_Backtesting_Performance.py
7_Trade_Analytics.py



Dashboard sections:

| Page | Function |
|---|---|
| Load Forecasting | Demand forecasting analytics |
| Imbalance Risk | System risk monitoring |
| Trading Decisions | Market signals |
| Market Comparison | Country analysis |
| Model Performance | ML evaluation |
| Backtesting | Strategy evaluation |
| Trade Analytics | Trading insights |

---

# 📂 Project Structure



Energy-Trading-Decision-Support-System/

│
├── app.py
│
├── pages/
│ ├── 1_Load_Forecasting.py
│ ├── 2_Imbalance_Risk.py
│ ├── 3_Trading_Decisions.py
│ ├── 4_Market_Comparison.py
│ ├── 5_Model_Performance.py
│ ├── 6_Backtesting_Performance.py
│ └── 7_Trade_Analytics.py
│
├── data/
│
│ └── demo/
│
├── models/
│
├── results/
│
├── src/
│
├── requirements.txt
│
└── README.md


---

# 🛠️ Technologies Used

## Programming

- Python


## Data Analysis

- Pandas
- NumPy


## Machine Learning

- Scikit-learn
- XGBoost


## Forecasting

- Prophet
- Statistical modelling techniques


## Visualization

- Streamlit
- Plotly


## Statistics

- Time-series analysis
- Feature engineering
- Risk metrics


---

# 📊 Machine Learning Workflow



Data Collection

    |

Data Cleaning

    |

Feature Engineering

    |

Model Training

    |

Performance Evaluation

    |

Forecast Generation

    |

Trading Decision Support



---

# 📈 Example ML Evaluation Metrics


| Model | MAE | RMSE | MAPE |
|-|-|-|-|
| Linear Regression | 1109 | 1422 | 2.14% |
| Random Forest | 537 | 739 | 1.04% |
| XGBoost | 490 | 650 | 0.95% |
| Prophet | 2820 | 3719 | 5.63% |


XGBoost achieved the strongest forecasting performance among tested approaches.

---

# 🌍 Countries Covered

The framework supports:

- 🇩🇪 Germany
- 🇫🇷 France
- 🇮🇹 Italy
- 🇪🇸 Spain
- 🇳🇱 Netherlands


---

# ▶️ Running the Project Locally


Clone repository:

```bash
git clone https://github.com/panos-karampoulis/industry-projects.git

Navigate:

cd Energy-Trading-Decision-Support-System

Install dependencies:

pip install -r requirements.txt

Run Streamlit:

streamlit run app.py
☁️ Deployment

The dashboard is deployed using:

Streamlit Cloud
GitHub integration
🔮 Future Improvements

Possible extensions:

Real-time ENTSO-E API integration
Weather API integration
Electricity price forecasting models
Deep learning models (LSTM, Transformers)
Automated trading optimisation
Reinforcement learning strategies
Real-time portfolio monitoring
👨‍💻 Author

Panagiotis Karampoulis