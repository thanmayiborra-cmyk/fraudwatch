"""
FraudWatch - Transaction Anomaly Detection System
Step 1: This script creates a sample bank transaction dataset and loads it into SQLite.
(If you download a real dataset from Kaggle instead, skip this and use that CSV.)
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "transactions.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            location TEXT
        )
    """)
    conn.commit()
    return conn


def generate_sample_data(conn, num_accounts=10, transactions_per_account=50):
    """
    Generates realistic transaction data for sample accounts.
    Most transactions are 'normal' (clustered around an average),
    with a few intentionally unusual ones mixed in to simulate fraud.
    """
    cursor = conn.cursor()
    locations = ["Hyderabad", "Mumbai", "Delhi", "Bengaluru", "Chennai"]

    for acc_num in range(1, num_accounts + 1):
        account_id = f"ACC{1000 + acc_num}"
        # Each account has its own typical spending range
        normal_avg = random.randint(500, 5000)

        for _ in range(transactions_per_account):
            # 90% normal transactions, 10% unusual (simulated anomalies)
            if random.random() < 0.9:
                amount = round(random.gauss(normal_avg, normal_avg * 0.15), 2)
            else:
                # Anomaly: much higher than usual
                amount = round(normal_avg * random.uniform(4, 8), 2)

            amount = max(amount, 10)  # no negative amounts
            days_ago = random.randint(0, 90)
            txn_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            location = random.choice(locations)

            cursor.execute(
                "INSERT INTO transactions (account_id, amount, transaction_date, location) VALUES (?, ?, ?, ?)",
                (account_id, amount, txn_date, location),
            )

    conn.commit()
    print(f"Generated {num_accounts * transactions_per_account} transactions for {num_accounts} accounts.")


if __name__ == "__main__":
    conn = create_database()
    generate_sample_data(conn)
    conn.close()
    print(f"Database created: {DB_NAME}")
