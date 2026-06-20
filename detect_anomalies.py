"""
FraudWatch - Transaction Anomaly Detection System
Step 2: This script queries the transaction database using SQL,
applies z-score statistical analysis in Python, and generates
a suspicious activity report - similar to real AML analyst workflows.
"""

import sqlite3
import statistics

DB_NAME = "transactions.db"
Z_SCORE_THRESHOLD = 2.5  # transactions beyond this many std devs are flagged


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_accounts(conn):
    """SQL query: get list of unique account IDs"""
    rows = conn.execute("SELECT DISTINCT account_id FROM transactions").fetchall()
    return [row["account_id"] for row in rows]


def get_transactions_for_account(conn, account_id):
    """SQL query: get all transactions for one account, ordered by amount"""
    rows = conn.execute(
        "SELECT * FROM transactions WHERE account_id = ? ORDER BY amount DESC",
        (account_id,),
    ).fetchall()
    return rows


def calculate_z_scores(transactions):
    """
    Statistics: calculate mean, standard deviation, and z-score
    for each transaction relative to the account's normal pattern.
    """
    amounts = [t["amount"] for t in transactions]

    if len(amounts) < 2:
        return []

    mean_amount = statistics.mean(amounts)
    std_dev = statistics.stdev(amounts)

    results = []
    for t in transactions:
        if std_dev == 0:
            z_score = 0
        else:
            z_score = (t["amount"] - mean_amount) / std_dev

        results.append({
            "transaction_id": t["id"],
            "account_id": t["account_id"],
            "amount": t["amount"],
            "date": t["transaction_date"],
            "location": t["location"],
            "account_avg": round(mean_amount, 2),
            "z_score": round(z_score, 2),
        })

    return results


def generate_suspicious_activity_report(conn):
    """
    Main report generator: scans every account, flags transactions
    whose z-score exceeds the threshold, and prints a structured report.
    """
    accounts = get_all_accounts(conn)
    flagged_transactions = []

    for account_id in accounts:
        transactions = get_transactions_for_account(conn, account_id)
        scored_transactions = calculate_z_scores(transactions)

        for txn in scored_transactions:
            if abs(txn["z_score"]) >= Z_SCORE_THRESHOLD:
                flagged_transactions.append(txn)

    # Sort by severity (highest z-score first)
    flagged_transactions.sort(key=lambda x: abs(x["z_score"]), reverse=True)

    print("=" * 70)
    print("SUSPICIOUS ACTIVITY REPORT")
    print("=" * 70)
    print(f"Threshold: transactions beyond {Z_SCORE_THRESHOLD} standard deviations\n")

    if not flagged_transactions:
        print("No suspicious transactions found.")
    else:
        for txn in flagged_transactions:
            severity = "HIGH" if abs(txn["z_score"]) >= 4 else "MEDIUM"
            print(f"[{severity}] Account: {txn['account_id']} | "
                  f"Amount: ₹{txn['amount']:.2f} | "
                  f"Account Avg: ₹{txn['account_avg']:.2f} | "
                  f"Z-Score: {txn['z_score']} | "
                  f"Date: {txn['date']} | Location: {txn['location']}")

    print(f"\nTotal flagged: {len(flagged_transactions)} out of "
          f"{sum(len(get_transactions_for_account(conn, a)) for a in accounts)} transactions")

    return flagged_transactions


if __name__ == "__main__":
    conn = get_db()
    generate_suspicious_activity_report(conn)
    conn.close()
