def credit(account_id, amount):
    return True, account_id, amount


def debit(account_id, amount):
    return False, account_id, amount


def make_journal_entry(description: str, *credits_and_debits):
    return dict(description=description, credits=[(c[1], c[2]) for c in credits_and_debits if c[0]],
                debits=[(d[1], d[2]) for d in credits_and_debits if not d[0]])
