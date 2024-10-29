import csv
from datetime import datetime
from pathlib import Path


transactions1 = list(csv.reader(Path("bw_transactions/transactions1.csv").open()))
transactions2 = list(csv.reader(Path("bw_transactions/transactions2.csv").open()))


def check_equal_transactions(row, transactions):
    """Busca por transações iguais em datas anteriores, atuais ou posteriores."""

    lowest_date = None
    lowest_transaction_position = None

    for i, transaction in enumerate(transactions):
        if len(transaction) <= 4:
            transaction.append("MISSING")
        if "FOUND" in transaction:
            continue

        if row[1] in transaction and row[2] in transaction and row[3] in transaction:
            transaction1_date = datetime.strptime(row[0], "%Y-%m-%d")
            transaction2_date = datetime.strptime(transaction[0], "%Y-%m-%d")
            if abs((transaction1_date - transaction2_date).days) <= 1:
                if lowest_date is None or lowest_date > transaction2_date:
                    lowest_date = transaction2_date
                    lowest_transaction_position = i
    if lowest_transaction_position is not None:
        transactions[lowest_transaction_position][4] = "FOUND"
        row.append("FOUND")
    else:
        row.append("MISSING")
    return row


def reconcile_accounts(transactions1, transactions2):
    """Concilia duas listas de transações."""

    for transaction in transactions1:
        check_equal_transactions(transaction, transactions2)
    return transactions1, transactions2


out1, out2 = reconcile_accounts(transactions1, transactions2)
