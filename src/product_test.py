from src.product import credit, debit, make_journal_entry
from src.testhelpers import test, ARBITRARY
from assertpy import assert_that


@test
def compute_account_balance():
    # Initial state:
    # There is a ledger with 3 transactions: two credits to account A and one debit.
    ledger = []
    ledger.append(make_journal_entry(
        "first",
        credit("a", 100),
        debit("b", 100)
    ))
    ledger.append(make_journal_entry(
        "second",
        credit("a", 25),
        credit("b", 75),
        debit("c", 100)
    ))
    ledger.append(make_journal_entry(
        "third",
        debit("a", 50),
        credit("c", 50)
    ))
    # Action:
    # Compute sum of credits minus debits for account A
    total_a = sum(
        sum(c[1] for c in e['credits'] if c[0] == "a") - sum(d[1] for d in e['debits'] if d[0] == "a") for e in ledger)
    # Outcome:
    # Verify that the sum is correct.
    assert_that(total_a).is_equal_to(75)


@test
def local_transfer():
    # Irrelevant details:
    source_starting_balance = ARBITRARY.many_dollars()
    transfer_amount = ARBITRARY.few_dollars()
    source = ARBITRARY.account_name()
    destination = ARBITRARY.account_name()
    # Initial state:
    # Source and destination accounts exist with money in the source
    # Note, the initial amounts are not needed yet, but will be needed once I
    # add the insufficient funds case, so I'm adding them now.
    ledger = []
    ledger.append(make_journal_entry(
        "customer deposit",
        debit("STD:Cash", source_starting_balance),
        credit(source, source_starting_balance)
    ))
    # Action:
    # Transfer money from source to destination, leaving some money in each
    transfer = make_journal_entry(
        f"Transfer from {source} to {destination}",
        credit(destination, transfer_amount),
        debit(source, transfer_amount)
    )
    ledger.append(transfer)
    # Outcome:
    # Verify that the new transaction has been added to the ledger.
    assert_that(ledger).contains(transfer)
