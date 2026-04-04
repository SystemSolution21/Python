import re
from abc import ABC, abstractmethod
from typing import Any


# ── VALIDATION UTILITIES ─────────────────────────────────
class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class Validators:
    """Collection of validation methods following real-world best practices."""

    @staticmethod
    def validate_amount(
        amount: float, min_amount: float = 0.01, max_amount: float = 999999.99
    ) -> None:
        """
        Validate payment amount.

        Real-world constraints:
        - Must be a number (int or float)
        - Must be positive
        - Must be within reasonable limits (prevent overflow/abuse)
        - Should handle precision (2 decimal places for currency)

        Args:
            amount: The amount to validate
            min_amount: Minimum allowed amount (default: $0.01)
            max_amount: Maximum allowed amount (default: $999,999.99)

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(amount, (int, float)):
            raise ValidationError(
                f"Amount must be a number, got {type(amount).__name__}"
            )

        if amount < min_amount:
            raise ValidationError(f"Amount must be at least ${min_amount:.2f}")

        if amount > max_amount:
            raise ValidationError(f"Amount cannot exceed ${max_amount:,.2f}")

        # Check for reasonable decimal precision (currency should have max 2 decimal places)
        if round(amount, 2) != amount:
            raise ValidationError(
                f"Amount must have at most 2 decimal places, got {amount}"
            )

    @staticmethod
    def validate_card_number(card_number: str) -> None:
        """
        Validate credit card number using industry standards.

        Real-world constraints:
        - Must be a string
        - Must contain only digits (after removing spaces/dashes)
        - Must be 13-19 digits (industry standard)
        - Must pass Luhn algorithm (checksum validation)

        Args:
            card_number: The card number to validate

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(card_number, str):
            raise ValidationError(
                f"Card number must be a string, got {type(card_number).__name__}"
            )

        # Remove common separators
        clean_number = card_number.replace(" ", "").replace("-", "")

        if not clean_number:
            raise ValidationError("Card number cannot be empty")

        if not clean_number.isdigit():
            raise ValidationError("Card number must contain only digits")

        # Check length (13-19 is industry standard)
        if len(clean_number) < 13 or len(clean_number) > 19:
            raise ValidationError(
                f"Card number must be 13-19 digits, got {len(clean_number)}"
            )

        # Luhn algorithm validation (industry-standard checksum)
        if not Validators._luhn_check(clean_number):
            raise ValidationError("Invalid card number (failed Luhn check)")

    @staticmethod
    def _luhn_check(card_number: str) -> bool:
        """
        Implement Luhn algorithm for card validation.

        The Luhn algorithm (mod-10 algorithm) is used by credit card companies
        to distinguish valid card numbers from random sequences.

        Args:
            card_number: Clean card number (digits only)

        Returns:
            True if valid, False otherwise
        """

        def digits_of(n: str) -> list[int]:
            return [int(d) for d in n]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]  # Every second digit from right
        even_digits = digits[-2::-2]  # Remaining digits

        checksum = sum(odd_digits)
        for digit in even_digits:
            checksum += sum(digits_of(str(digit * 2)))

        return checksum % 10 == 0

    @staticmethod
    def validate_holder_name(holder: str) -> None:
        """
        Validate cardholder name.

        Real-world constraints:
        - Must be a string
        - Cannot be empty or only whitespace
        - Must be 2-50 characters (reasonable name length)
        - Should contain only letters, spaces, hyphens, apostrophes
        - Must have at least first and last name (2 parts)

        Args:
            holder: The cardholder name to validate

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(holder, str):
            raise ValidationError(
                f"Holder name must be a string, got {type(holder).__name__}"
            )

        holder_stripped = holder.strip()

        if not holder_stripped:
            raise ValidationError("Holder name cannot be empty")

        if len(holder_stripped) < 2:
            raise ValidationError("Holder name must be at least 2 characters")

        if len(holder_stripped) > 50:
            raise ValidationError("Holder name cannot exceed 50 characters")

        # Allow letters, spaces, hyphens, apostrophes, and periods (e.g., "Mary-Jane O'Brien Jr.")
        if not re.match(r"^[a-zA-Z\s\-'.]+$", holder_stripped):
            raise ValidationError("Holder name contains invalid characters")

        # Should have at least first and last name (at least one space)
        name_parts = holder_stripped.split()
        if len(name_parts) < 2:
            raise ValidationError("Holder name must include first and last name")

    @staticmethod
    def validate_email(email: str) -> None:
        """
        Validate email address.

        Real-world constraints:
        - Must be a string
        - Cannot be empty
        - Must match standard email format
        - Must have valid domain
        - Length constraints (max 254 chars per RFC 5321)

        Args:
            email: The email address to validate

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(email, str):
            raise ValidationError(f"Email must be a string, got {type(email).__name__}")

        email_stripped = email.strip()

        if not email_stripped:
            raise ValidationError("Email cannot be empty")

        if len(email_stripped) > 254:
            raise ValidationError("Email cannot exceed 254 characters")

        # RFC 5322 compliant regex (simplified but robust)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email_stripped):
            raise ValidationError("Invalid email format")

        # Additional check: local part (before @) should be <= 64 chars
        local_part = email_stripped.split("@")[0]
        if len(local_part) > 64:
            raise ValidationError("Email local part cannot exceed 64 characters")


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
    def __init__(self, card_number: str, holder: str) -> None:
        # ── ENCAPSULATION + VALIDATION ────────────────────
        # Using property setters for automatic validation
        self.card_number = card_number  # Triggers validation via @card_number.setter
        self.holder = holder  # Triggers validation via @holder.setter
        self.__transactions: list[Any] = []  # internal state

    # ── PROPERTY: card_number (with validation) ──────────
    @property
    def card_number(self) -> str:
        """Get the card number (private backing field)."""
        return self.__card_number

    @card_number.setter
    def card_number(self, value: str) -> None:
        """
        Set card number with validation.

        Validates using Luhn algorithm and industry standards.
        """
        Validators.validate_card_number(value)
        # Store clean version (digits only)
        self.__card_number = value.replace(" ", "").replace("-", "")

    # ── PROPERTY: holder (with validation) ───────────────
    @property
    def holder(self) -> str:
        """Get the cardholder name."""
        return self.__holder

    @holder.setter
    def holder(self, value: str) -> None:
        """
        Set cardholder name with validation.

        Ensures proper name format and length.
        """
        Validators.validate_holder_name(value)
        self.__holder = value.strip()

    # Controlled access via a public method (getter)
    def get_masked_card(self) -> str:
        """Return masked card number for display (PCI-DSS compliant)."""
        return f"**** **** **** {self.__card_number[-4:]}"

    # ── ABSTRACTION (fulfilled) ───────────────────────────
    # "How" CreditCard processes — hidden from the caller
    def process(self, amount: float) -> str:
        """Process a payment with amount validation."""
        Validators.validate_amount(amount)
        self.__transactions.append(("charge", amount))
        return f"✅ Charged ${amount:.2f} to {self.get_masked_card()}"

    def refund(self, amount: float) -> str:
        """Refund a payment with amount validation."""
        Validators.validate_amount(amount)
        self.__transactions.append(("refund", amount))
        return f"↩️  Refunded ${amount:.2f} to {self.get_masked_card()}"

    def get_statement(self) -> list[Any]:
        """Get transaction history (read-only view)."""
        return (
            self.__transactions.copy()
        )  # Return copy to prevent external modification


# Another sibling — same interface, different behavior
class PayPalPayment(Payment):
    def __init__(self, email: str) -> None:
        # ── ENCAPSULATION + VALIDATION ────────────────────
        self.email = email  # Triggers validation via @email.setter

    # ── PROPERTY: email (with validation) ────────────────
    @property
    def email(self) -> str:
        """Get the PayPal email address."""
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        """
        Set PayPal email with validation.

        Ensures valid email format per RFC standards.
        """
        Validators.validate_email(value)
        self.__email = value.strip().lower()  # Normalize to lowercase

    def process(self, amount: float) -> str:
        """Process a PayPal payment with amount validation."""
        Validators.validate_amount(amount)
        return f"✅ Charged ${amount:.2f} via PayPal ({self.__email})"

    def refund(self, amount: float) -> str:
        """Refund a PayPal payment with amount validation."""
        Validators.validate_amount(amount)
        return f"↩️  Refunded ${amount:.2f} via PayPal ({self.__email})"


def main():
    print("=" * 80)
    print("PAYMENT SYSTEM WITH REAL-WORLD VALIDATION")
    print("=" * 80)

    # ── POLYMORPHISM ──────────────────────────────────────────
    # Caller doesn't know or care which payment type it is
    def checkout(payment: Payment, amount: float) -> None:
        print(payment.process(amount=amount))

    print("\n✅ VALID TRANSACTIONS:")
    print("-" * 80)

    # Valid credit card (passes Luhn check)
    card = CreditCardPayment(card_number="4111111111111111", holder="John Doe")
    paypal: PayPalPayment = PayPalPayment(email="john@email.com")

    checkout(payment=card, amount=149.99)
    checkout(payment=paypal, amount=149.99)

    # Encapsulation at work:
    # card.__card_number        ❌ AttributeError
    # card.__transactions       ❌ AttributeError
    print(f"\nMasked card: {card.get_masked_card()}")
    print(f"Statement: {card.get_statement()}")

    # Test refund
    print(f"\n{card.refund(amount=50.00)}")
    print(f"Updated statement: {card.get_statement()}")

    # ── VALIDATION DEMONSTRATIONS ─────────────────────────────
    print("\n\n❌ VALIDATION ERROR EXAMPLES:")
    print("-" * 80)

    # Test various validation failures
    test_cases = [
        # Invalid amounts
        (
            lambda: CreditCardPayment("4111111111111111", "John Doe").process(-10.00),
            "Negative amount",
        ),
        (
            lambda: CreditCardPayment("4111111111111111", "John Doe").process(
                1000000.00
            ),
            "Amount exceeds limit",
        ),
        (
            lambda: CreditCardPayment("4111111111111111", "John Doe").process(10.999),
            "Too many decimal places",
        ),
        # Invalid card numbers
        (
            lambda: CreditCardPayment("1234567890123456", "John Doe"),
            "Invalid card (fails Luhn check)",
        ),
        (
            lambda: CreditCardPayment("411111", "John Doe"),
            "Card number too short",
        ),
        (
            lambda: CreditCardPayment("invalid-card", "John Doe"),
            "Non-numeric card number",
        ),
        # Invalid holder names
        (lambda: CreditCardPayment("4111111111111111", ""), "Empty holder name"),
        (
            lambda: CreditCardPayment("4111111111111111", "J"),
            "Holder name too short",
        ),
        (
            lambda: CreditCardPayment("4111111111111111", "John"),
            "Missing last name",
        ),
        (
            lambda: CreditCardPayment("4111111111111111", "John123 Doe"),
            "Invalid characters in name",
        ),
        # Invalid emails
        (lambda: PayPalPayment("invalid-email"), "Invalid email format"),
        (lambda: PayPalPayment(""), "Empty email"),
        (lambda: PayPalPayment("no-domain@"), "Email missing domain"),
        (lambda: PayPalPayment("@nodomain.com"), "Email missing local part"),
    ]

    for i, (test_func, description) in enumerate(test_cases, 1):
        try:
            test_func()
            print(f"{i:2d}. {description}: ⚠️  SHOULD HAVE FAILED!")
        except ValidationError as e:
            print(f"{i:2d}. {description}: ✓ Caught → {e}")
        except Exception as e:
            print(f"{i:2d}. {description}: ⚠️  Unexpected error → {type(e).__name__}")

    # ── ADDITIONAL VALID EXAMPLES ─────────────────────────────
    print("\n\n✅ ADDITIONAL VALID EXAMPLES:")
    print("-" * 80)

    # Test with formatted card number (spaces/dashes) - Using valid test cards
    # These are standard test card numbers that pass Luhn validation
    card2 = CreditCardPayment(
        card_number="5105-1051-0510-5100", holder="Mary-Jane O'Brien"
    )
    print(f"Card with dashes: {card2.get_masked_card()}")

    card3 = CreditCardPayment(
        card_number="3782 822463 10005", holder="Robert Smith Jr."
    )
    print(f"Card with spaces: {card3.get_masked_card()}")

    # Test email normalization
    paypal2 = PayPalPayment(email="  JOHN.DOE@EXAMPLE.COM  ")
    print(f"Normalized email: {paypal2.email}")

    # Test different valid amounts
    valid_amounts = [0.01, 10.50, 999.99, 999999.99]
    print(f"\nValid amounts: {valid_amounts}")
    for amt in valid_amounts:
        try:
            Validators.validate_amount(amt)
            print(f"  ${amt:,.2f} ✓")
        except ValidationError as e:
            print(f"  ${amt:,.2f} ✗ {e}")

    print("\n" + "=" * 80)
    print("✅ ALL VALIDATION TESTS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
