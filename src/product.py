def credit(account_id, amount):
    return True, account_id, amount


def debit(account_id, amount):
    return False, account_id, amount


def make_journal_entry(description: str, *credits_and_debits):
    return dict(description=description, credits=[(c[1], c[2]) for c in credits_and_debits if c[0]],
                debits=[(d[1], d[2]) for d in credits_and_debits if not d[0]])


def customer_deposit(account, amount):
    return make_journal_entry(
        "customer deposit",
        debit("STD:Cash", amount),
        credit(account, amount)
    )


def transfer(source, destination, amount):
    return make_journal_entry(
        f"Transfer from {source} to {destination}",
        credit(destination, amount),
        debit(source, amount)
    )


class Bank:
    def __init__(self):
        self.ledger = []

    def total_credits_minus_debits(self, account):
        return sum(
            sum(c[1] for c in e['credits'] if c[0] == account) - sum(d[1] for d in e['debits'] if d[0] == account)
            for e
            in self.ledger)

    def record(self, entry):
        self.ledger.append(entry)
