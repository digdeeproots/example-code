from src.product import credit, debit, make_journal_entry, customer_deposit, transfer
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

    def total_credits_minus_debits(bank, account):
        return sum(
            sum(c[1] for c in e['credits'] if c[0] == account) - sum(d[1] for d in e['debits'] if d[0] == account) for e
            in bank.ledger)

    class Bank:
        def __init__(self, ledger):
            self.ledger = ledger

    total_a = total_credits_minus_debits(Bank(ledger), "a")
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
    ledger.append(customer_deposit(source, source_starting_balance))

    # Action:
    # Transfer money from source to destination, leaving some money in each
    the_transfer = transfer(source, destination, transfer_amount)
    ledger.append(the_transfer)
    # Outcome:
    # Verify that the new transaction has been added to the ledger.
    assert_that(ledger).contains(the_transfer)
