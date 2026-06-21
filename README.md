# FraudWatch

A small project to detect unusual transactions in banking data using SQL and basic statistics. Built this to practice SQL queries on a real-ish dataset and apply some actual stats (not just Excel formulas) to flag outliers - the kind of thing AML/fraud teams do at a basic level.

## What it does

- Generates a sample set of bank transactions across 10 accounts (500 transactions total)
- Stores everything in a SQLite database
- For each account, calculates the average transaction amount and standard deviation
- Flags any transaction that's more than 2.5 standard deviations away from that account's normal pattern (this is called a z-score)
- Prints out a report of flagged transactions, sorted by how extreme they are

## Why z-score

Wanted something more than "transactions over a fixed amount get flagged" since that doesn't account for the fact that different accounts have very different normal spending levels. Z-score adjusts for that - it flags based on how unusual a transaction is for that specific account, not against some fixed number.

z = (transaction_amount - account_average) / account_standard_deviation

## How to run

python3 setup_data.py
python3 detect_anomalies.py

## Sample output

[HIGH] Account: ACC1010 | Amount: 2896.82 | Account Avg: 696.77 | Z-Score: 6.61
[HIGH] Account: ACC1009 | Amount: 18279.09 | Account Avg: 3038.20 | Z-Score: 5.25
[MEDIUM] Account: ACC1001 | Amount: 8191.99 | Account Avg: 1759.13 | Z-Score: 3.73

Total flagged: 27 out of 500 transactions

## Notes

The data here is randomly generated, not real transactions - just wanted a realistic-ish dataset to test the logic on. Real fraud detection systems obviously use a lot more than just z-score (machine learning models, rule engines, network analysis between accounts, etc.) but this covers the basic statistical idea.

## Possible next steps

- Try it on a real public dataset (Kaggle has a few credit card fraud ones)
- Add time-based patterns - like flagging a bunch of transactions happening too close together
- Visualize the flagged transactions in Power BI
