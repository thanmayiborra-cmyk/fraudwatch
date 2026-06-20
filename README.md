# fraudwatch
Banking transaction anomaly detection system using Python, SQL, SQLite, and Z-score statistical analysis to identify suspicious transactions and generate AML-style activity reports.
# FraudWatch

A transaction anomaly detection system that identifies potentially suspicious banking activity using SQL and statistical analysis — built to simulate the kind of pattern detection used in real-world AML (Anti-Money Laundering) and fraud monitoring workflows.

## What it does

- Generates a sample dataset of bank transactions across multiple accounts and stores it in a SQLite database
- Queries transaction history per account using SQL
- Applies **z-score statistical analysis** in Python to detect transactions that deviate significantly from an account's normal spending pattern
- Classifies flagged transactions by severity (HIGH / MEDIUM) based on how extreme the deviation is
- Outputs a structured "Suspicious Activity Report" — similar in spirit to the kind of report an AML analyst would review

## Why z-score?

Z-score measures how many standard deviations a value is from the average. For each account, the system calculates:

```
z = (transaction_amount - account_average) / account_standard_deviation
```

A transaction with a z-score above 2.5 means it's significantly larger than that account's typical spending — a common, real statistical technique used in fraud and outlier detection.

## Tech stack

- **Python** — data generation, statistical analysis, report generation
- **SQL / SQLite** — transaction storage and querying
- **Statistics** — mean, standard deviation, z-score outlier detection

## How to run it

```bash
python3 setup_data.py        # creates the database and sample transactions
python3 detect_anomalies.py  # runs the analysis and prints the report
```

## Sample output

```
======================================================================
SUSPICIOUS ACTIVITY REPORT
======================================================================
Threshold: transactions beyond 2.5 standard deviations

[HIGH] Account: ACC1010 | Amount: ₹2896.82 | Account Avg: ₹696.77 | Z-Score: 6.61 | Date: 2026-03-29 | Location: Hyderabad
[HIGH] Account: ACC1009 | Amount: ₹18279.09 | Account Avg: ₹3038.20 | Z-Score: 5.25 | Date: 2026-04-24 | Location: Mumbai
[MEDIUM] Account: ACC1001 | Amount: ₹8191.99 | Account Avg: ₹1759.13 | Z-Score: 3.73 | Date: 2026-06-14 | Location: Hyderabad

Total flagged: 27 out of 500 transactions
```

## Project structure

```
fraudwatch/
├── setup_data.py        # generates sample transaction data into SQLite
├── detect_anomalies.py  # SQL queries + z-score analysis + report generation
└── README.md
```

## Possible extensions

- Connect to a real public dataset (e.g. Kaggle credit card fraud datasets)
- Visualize flagged transactions in Power BI
- Add time-based pattern detection (e.g. rapid repeated transactions)
- Export the report to CSV for further review
