import unittest
from datetime import datetime

from bw_reconcile_accounts import reconcile_accounts


# Função reconcile_accounts que queremos testar
def reconcile_accounts(transactions1, transactions2):
    transactions1 = [trans for trans in transactions1 if trans]
    transactions2 = [trans for trans in transactions2 if trans]

    def find_latest_match(trans, transactions):
        """Procura a correspondência mais recente para uma transação."""
        latest_match = None
        latest_date = None
        date1 = datetime.strptime(trans[0], "%Y-%m-%d")

        for other in transactions:
            if other[-1] == "FOUND":
                continue

            date2 = datetime.strptime(other[0], "%Y-%m-%d")
            if abs((date1 - date2).days) <= 1 and trans[1:] == other[1:]:
                if latest_match is None or date2 > latest_date:
                    latest_match = other
                    latest_date = date2
        return latest_match

    for i, trans in enumerate(transactions1):
        match = find_latest_match(trans, transactions2)
        if match:
            transactions1[i].append("FOUND")
            match.append("FOUND")
        else:
            transactions1[i].append("MISSING")

    for i, trans in enumerate(transactions2):
        if len(trans) < 5:
            transactions2[i].append("MISSING")

    return transactions1, transactions2


class TestReconcileAccounts(unittest.TestCase):
    def test_reconcile_accounts(self):
        # Cenário 1: Transações simples com correspondências exatas
        transactions1 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
            ["2020-12-05", "Tecnologia", "50.00", "AWS"],
        ]

        transactions2 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-05", "Tecnologia", "49.99", "AWS"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
        ]

        expected_out1 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
            ["2020-12-05", "Tecnologia", "50.00", "AWS", "MISSING"],
        ]

        expected_out2 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
            ["2020-12-05", "Tecnologia", "49.99", "AWS", "MISSING"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
        ]

        out1, out2 = reconcile_accounts(transactions1, transactions2)
        self.assertEqual(out1, expected_out1)
        self.assertEqual(out2, expected_out2)

    def test_reconcile_duplicates(self):
        # Cenário 2: Transações duplicadas com correspondência em uma data exata
        transactions1 = [
            ["2020-12-04", "Financeiro", "100.00", "Google"],
            ["2020-12-04", "Financeiro", "100.00", "Google"],
        ]

        transactions2 = [["2020-12-04", "Financeiro", "100.00", "Google"]]

        expected_out1 = [
            ["2020-12-04", "Financeiro", "100.00", "Google", "FOUND"],
            ["2020-12-04", "Financeiro", "100.00", "Google", "MISSING"],
        ]

        expected_out2 = [["2020-12-04", "Financeiro", "100.00", "Google", "FOUND"]]

        out1, out2 = reconcile_accounts(transactions1, transactions2)
        self.assertEqual(out1, expected_out1)
        self.assertEqual(out2, expected_out2)

    def test_reconcile_adjacent_dates(self):
        # Cenário 3: Correspondências com datas adjacentes
        transactions1 = [["2020-12-05", "Tecnologia", "50.00", "AWS"]]

        transactions2 = [["2020-12-04", "Tecnologia", "50.00", "AWS"]]

        expected_out1 = [["2020-12-05", "Tecnologia", "50.00", "AWS", "FOUND"]]

        expected_out2 = [["2020-12-04", "Tecnologia", "50.00", "AWS", "FOUND"]]

        out1, out2 = reconcile_accounts(transactions1, transactions2)
        self.assertEqual(out1, expected_out1)
        self.assertEqual(out2, expected_out2)

    def test_reconcile_missing_transactions(self):
        # Cenário 4: Transações sem correspondência
        transactions1 = [["2020-12-06", "TI", "200.00", "IBM"]]

        transactions2 = [["2020-12-07", "TI", "300.00", "Microsoft"]]

        expected_out1 = [["2020-12-06", "TI", "200.00", "IBM", "MISSING"]]

        expected_out2 = [["2020-12-07", "TI", "300.00", "Microsoft", "MISSING"]]

        out1, out2 = reconcile_accounts(transactions1, transactions2)
        self.assertEqual(out1, expected_out1)
        self.assertEqual(out2, expected_out2)


if __name__ == "__main__":
    unittest.main()
