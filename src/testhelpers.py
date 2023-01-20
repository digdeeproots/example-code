import random


def test(f):
    f.__test__ = True
    return f


class ARBITRARY:
    next_value = 100

    @staticmethod
    def many_dollars():
        return 1000 + random.randint(0, 100)

    @staticmethod
    def few_dollars():
        return random.randint(10, 50)

    @staticmethod
    def account_name():
        ARBITRARY.next_value += 1
        return f"test account:{ARBITRARY.next_value}"
