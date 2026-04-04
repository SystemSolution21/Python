from abc import ABC, abstractmethod


# ── ABSTRACTION ──────────────────────────────────────────
# Defines "what" a payment must do, not "how"
class Payment(ABC):
    @abstractmethod
    def process(self, amount: float) -> str:
        pass

    @abstractmethod
    def refund(self, amount: float) -> str:
        pass


# ── INHERITANCE ──────────────────────────────────────────
# CreditCardPayment IS-A Payment
class CreditCardPayment(Payment):
    def __init__(self, card_number: str, holder: str):
        # ── ENCAPSULATION ─────────────────────────────────
        # Sensitive data is private — no direct access
        self.__card_number = card_number
        self.__holder = holder
        self.__transactions = []  # internal state

    # Controlled access via a public method (getter)
    def get_masked_card(self):
        return f"**** **** **** {self.__card_number[-4:]}"

    def __validate(self, amount):  # private helper
        if amount <= 0:
            raise ValueError("Amount must be positive")

    # ── ABSTRACTION (fulfilled) ───────────────────────────
    # "How" CreditCard processes — hidden from the caller
    def process(self, amount: float) -> str:
        self.__validate(amount)
        self.__transactions.append(("charge", amount))
        return f"✅ Charged ${amount} to {self.get_masked_card()}"

    def refund(self, amount: float) -> str:
        self.__validate(amount)
        self.__transactions.append(("refund", amount))
        return f"↩️  Refunded ${amount} to {self.get_masked_card()}"

    def get_statement(self):
        return self.__transactions  # read-only view


# Another sibling — same interface, different behavior
class PayPalPayment(Payment):
    def __init__(self, email):
        self.__email = email

    def process(self, amount):
        return f"✅ Charged ${amount} via PayPal ({self.__email})"

    def refund(self, amount):
        return f"↩️  Refunded ${amount} via PayPal ({self.__email})"


def main():
    # ── POLYMORPHISM ──────────────────────────────────────────
    # Caller doesn't know or care which payment type it is
    def checkout(payment: Payment, amount: float):
        print(payment.process(amount))

    card = CreditCardPayment("4111111111111234", "John Doe")
    paypal = PayPalPayment("john@email.com")

    checkout(card, 149.99)  # ✅ Charged $149.99 to **** **** **** 1234
    checkout(paypal, 149.99)  # ✅ Charged $149.99 via PayPal (john@email.com)

    # Encapsulation at work:
    # card.__card_number        ❌ AttributeError
    # card.__transactions       ❌ AttributeError
    print(card.get_masked_card())  # ✅ **** **** **** 1234
    print(card.get_statement())  # ✅ [('charge', 149.99)]


if __name__ == "__main__":
    main()
