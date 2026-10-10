"""
Payment System with Pydantic Validation

This version demonstrates the same real-world validation features using Pydantic,
a modern data validation library that provides:
- Automatic type validation
- Custom validators
- Field constraints
- Better error messages
- JSON serialization
"""

import re
from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── CUSTOM VALIDATORS ────────────────────────────────────
class LuhnValidator:
    """Luhn algorithm implementation for credit card validation."""

    @staticmethod
    def validate(card_number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm.

        The Luhn algorithm (mod-10 algorithm) is used by credit card companies
        to distinguish valid card numbers from random sequences.
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


# ── PYDANTIC MODELS ──────────────────────────────────────
class CreditCardPaymentModel(BaseModel):
    """
    Credit Card Payment with Pydantic validation.

    Pydantic automatically validates on instantiation and provides:
    - Type validation
    - Field constraints (min/max values, regex patterns)
    - Custom validators
    - Immutability (when frozen=True)
    """

    # Configure Pydantic model behavior
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Auto-strip whitespace
        validate_assignment=True,  # Validate on assignment (not just init)
        frozen=False,  # Allow field updates (for demo purposes)
    )

    card_number: str = Field(
        ...,  # Required field
        min_length=13,
        max_length=19,
        description="Credit card number (13-19 digits)",
        examples=["4111111111111111", "5105-1051-0510-5100"],
    )

    holder: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Cardholder name (first and last name required)",
        examples=["John Doe", "Mary-Jane O'Brien Jr."],
    )

    # Private field for transactions (Pydantic v2 style)
    transactions: list[tuple[str, float]] = Field(default_factory=list, exclude=True)

    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        """
        Validate credit card number with Luhn algorithm.

        Pydantic validators:
        - Run after type validation
        - Can transform the value (return modified version)
        - Raise ValueError for validation errors
        """
        # Remove common separators
        clean_number = v.replace(" ", "").replace("-", "")

        if not clean_number:
            raise ValueError("Card number cannot be empty")

        if not clean_number.isdigit():
            raise ValueError("Card number must contain only digits")

        if len(clean_number) < 13 or len(clean_number) > 19:
            raise ValueError(
                f"Card number must be 13-19 digits, got {len(clean_number)}"
            )

        # Luhn algorithm validation
        if not LuhnValidator.validate(clean_number):
            raise ValueError("Invalid card number (failed Luhn check)")

        # Return cleaned version (stored without spaces/dashes)
        return clean_number

    @field_validator("holder")
    @classmethod
    def validate_holder_name(cls, v: str) -> str:
        """
        Validate cardholder name format.

        Requirements:
        - Only letters, spaces, hyphens, apostrophes, periods
        - Must have first and last name (at least 2 parts)
        """
        # Allow letters, spaces, hyphens, apostrophes, and periods
        if not re.match(r"^[a-zA-Z\s\-'.]+$", v):
            raise ValueError("Holder name contains invalid characters")

        # Should have at least first and last name
        name_parts = v.split()
        if len(name_parts) < 2:
            raise ValueError("Holder name must include first and last name")

        return v

    def get_masked_card(self) -> str:
        """Return masked card number for display (PCI-DSS compliant)."""
        return f"**** **** **** {self.card_number[-4:]}"

    def process(self, amount: float) -> str:
        """Process a payment with amount validation."""
        self._validate_amount(amount)
        self.transactions.append(("charge", amount))
        return f"✅ Charged ${amount:.2f} to {self.get_masked_card()}"

    def refund(self, amount: float) -> str:
        """Refund a payment with amount validation."""
        self._validate_amount(amount)
        self.transactions.append(("refund", amount))
        return f"↩️  Refunded ${amount:.2f} to {self.get_masked_card()}"

    def get_statement(self) -> list[tuple[str, float]]:
        """Get transaction history (read-only view)."""
        return self.transactions.copy()

    @staticmethod
    def _validate_amount(
        amount: float, min_amount: float = 0.01, max_amount: float = 999999.99
    ) -> None:
        """
        Validate payment amount.

        Could also be a Pydantic validator, but shown as static method for flexibility.
        """
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Amount must be a number, got {type(amount).__name__}")

        if amount < min_amount:
            raise ValueError(f"Amount must be at least ${min_amount:.2f}")

        if amount > max_amount:
            raise ValueError(f"Amount cannot exceed ${max_amount:,.2f}")

        if round(amount, 2) != amount:
            raise ValueError(f"Amount must have at most 2 decimal places, got {amount}")


class PayPalPaymentModel(BaseModel):
    """
    PayPal Payment with Pydantic validation.

    Uses custom email validation with regex pattern.
    Note: For production, install email-validator: pip install 'pydantic[email]'
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    # Custom email validation using string type + validator
    email: str = Field(
        ...,
        min_length=3,
        max_length=254,
        description="PayPal email address",
        examples=["john@email.com", "user@example.com"],
    )

    @field_validator("email")
    @classmethod
    def validate_and_normalize_email(cls, v: str) -> str:
        """
        Validate and normalize email address.

        For production use, install: pip install 'pydantic[email]'
        and use: from pydantic import EmailStr
        """
        # RFC 5322 compliant regex (simplified but robust)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")

        # Additional check: local part (before @) should be <= 64 chars
        local_part = v.split("@")[0]
        if len(local_part) > 64:
            raise ValueError("Email local part cannot exceed 64 characters")

        # Normalize to lowercase
        return v.lower()

    def process(self, amount: float) -> str:
        """Process a PayPal payment with amount validation."""
        CreditCardPaymentModel._validate_amount(amount)
        return f"✅ Charged ${amount:.2f} via PayPal ({self.email})"

    def refund(self, amount: float) -> str:
        """Refund a PayPal payment with amount validation."""
        CreditCardPaymentModel._validate_amount(amount)
        return f"↩️  Refunded ${amount:.2f} via PayPal ({self.email})"


# ── ABSTRACTION WITH POLYMORPHISM ────────────────────────
class Payment(ABC):
    """Abstract base class for payments (polymorphism)."""

    @abstractmethod
    def process(self, amount: float) -> str:
        pass

    @abstractmethod
    def refund(self, amount: float) -> str:
        pass


# Wrap Pydantic models to implement Payment interface
class CreditCardPayment(Payment):
    """Credit card payment wrapper."""

    def __init__(self, card_number: str, holder: str) -> None:
        self._model = CreditCardPaymentModel(card_number=card_number, holder=holder)

    def process(self, amount: float) -> str:
        return self._model.process(amount)

    def refund(self, amount: float) -> str:
        return self._model.refund(amount)

    def get_masked_card(self) -> str:
        return self._model.get_masked_card()

    def get_statement(self) -> list[tuple[str, float]]:
        return self._model.get_statement()

    @property
    def model(self) -> CreditCardPaymentModel:
        """Access underlying Pydantic model."""
        return self._model


class PayPalPayment(Payment):
    """PayPal payment wrapper."""

    def __init__(self, email: str) -> None:
        self._model = PayPalPaymentModel(email=email)

    def process(self, amount: float) -> str:
        return self._model.process(amount)

    def refund(self, amount: float) -> str:
        return self._model.refund(amount)

    @property
    def email(self) -> str:
        return self._model.email

    @property
    def model(self) -> PayPalPaymentModel:
        """Access underlying Pydantic model."""
        return self._model


# ── MAIN FUNCTION ────────────────────────────────────────
def main():
    print("=" * 80)
    print("PYDANTIC-BASED PAYMENT SYSTEM WITH REAL-WORLD VALIDATION")
    print("=" * 80)
    print("\n🔍 Key Pydantic Features Demonstrated:")
    print("   • Automatic type validation")
    print("   • Field constraints (min/max length, patterns)")
    print("   • Custom validators with @field_validator")
    print("   • Built-in EmailStr type")
    print("   • Whitespace stripping and normalization")
    print("   • Validation on assignment")
    print("   • Better error messages with detailed context")

    # ── POLYMORPHISM ──────────────────────────────────────────
    def checkout(payment: Payment, amount: float) -> None:
        print(payment.process(amount=amount))

    print("\n\n✅ VALID TRANSACTIONS:")
    print("-" * 80)

    # Valid credit card (passes Luhn check)
    card = CreditCardPayment(card_number="4111111111111111", holder="John Doe")
    paypal = PayPalPayment(email="john@email.com")

    checkout(payment=card, amount=149.99)
    checkout(payment=paypal, amount=149.99)

    print(f"\nMasked card: {card.get_masked_card()}")
    print(f"Statement: {card.get_statement()}")

    # Test refund
    print(f"\n{card.refund(amount=50.00)}")
    print(f"Updated statement: {card.get_statement()}")

    # ── PYDANTIC-SPECIFIC FEATURES ────────────────────────────
    print("\n\n🎯 PYDANTIC-SPECIFIC FEATURES:")
    print("-" * 80)

    # 1. JSON serialization
    print("1. JSON Serialization:")
    card_json = card.model.model_dump_json(indent=2, exclude={"transactions"})
    print(f"   {card_json}")

    # 2. Model validation with dict
    print("\n2. Create from dictionary:")
    card_dict = {"card_number": "5105 1051 0510 5100", "holder": "Jane Smith"}
    card2 = CreditCardPaymentModel(
        card_number=card_dict["card_number"], holder=card_dict["holder"]
    )
    print(f"   Created: {card2.get_masked_card()}")

    # 3. Field info and schema
    print("\n3. Pydantic automatically strips whitespace:")
    paypal2 = PayPalPayment(email="  JOHN.DOE@EXAMPLE.COM  ")
    print("   Input: '  JOHN.DOE@EXAMPLE.COM  '")
    print(f"   Normalized: '{paypal2.email}'")

    # 4. Validation on assignment (if validate_assignment=True)
    print("\n4. Validation on assignment:")
    try:
        card.model.holder = "Invalid123"  # Will fail validation
    except Exception as e:
        print(f"   ✓ Assignment validation caught: {type(e).__name__}")

    # ── VALIDATION ERROR EXAMPLES ─────────────────────────────
    print("\n\n❌ PYDANTIC VALIDATION ERROR EXAMPLES:")
    print("-" * 80)

    from pydantic import ValidationError

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
        # Invalid card numbers
        (
            lambda: CreditCardPayment("1234567890123456", "John Doe"),
            "Invalid card (fails Luhn check)",
        ),
        (lambda: CreditCardPayment("411111", "John Doe"), "Card number too short"),
        (
            lambda: CreditCardPayment("invalid-card", "John Doe"),
            "Non-numeric card number",
        ),
        # Invalid holder names
        (lambda: CreditCardPayment("4111111111111111", ""), "Empty holder name"),
        (lambda: CreditCardPayment("4111111111111111", "J"), "Holder name too short"),
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
    ]

    for i, (test_func, description) in enumerate(test_cases, 1):
        try:
            test_func()
            print(f"{i:2d}. {description}: ⚠️  SHOULD HAVE FAILED!")
        except (ValidationError, ValueError) as e:
            # Pydantic raises ValidationError, our custom validators raise ValueError
            error_msg = (
                str(e).split("\n")[0] if isinstance(e, ValidationError) else str(e)
            )
            print(f"{i:2d}. {description}: ✓ Caught → {error_msg[:60]}...")

    # ── PYDANTIC ERROR DETAILS ────────────────────────────────
    print("\n\n📋 PYDANTIC DETAILED ERROR EXAMPLE:")
    print("-" * 80)
    try:
        # Multiple validation errors at once
        _ = CreditCardPaymentModel(
            card_number="123",  # Too short
            holder="X",  # Too short
        )
    except ValidationError as e:
        print("Pydantic provides detailed validation errors:")
        print(f"  Error count: {e.error_count()}")
        for error in e.errors():
            print(f"  • Field: {error['loc'][0]}")
            print(f"    Type: {error['type']}")
            print(f"    Message: {error['msg']}")

    print("\n\n✅ ADDITIONAL VALID EXAMPLES:")
    print("-" * 80)

    # Test with formatted card numbers
    card3 = CreditCardPayment(
        card_number="5105-1051-0510-5100", holder="Mary-Jane O'Brien"
    )
    print(f"Card with dashes: {card3.get_masked_card()}")

    card4 = CreditCardPayment(
        card_number="3782 822463 10005", holder="Robert Smith Jr."
    )
    print(f"Card with spaces: {card4.get_masked_card()}")

    print("\n" + "=" * 80)
    print("✅ ALL PYDANTIC VALIDATION TESTS COMPLETED")
    print("=" * 80)
    print("\n💡 PYDANTIC ADVANTAGES:")
    print("   ✓ Less boilerplate code (no need for @property decorators)")
    print("   ✓ Automatic type coercion and validation")
    print("   ✓ Built-in JSON/dict serialization")
    print("   ✓ Detailed, structured error messages")
    print("   ✓ IDE autocomplete support")
    print("   ✓ OpenAPI/JSON Schema generation")
    print("=" * 80)


if __name__ == "__main__":
    main()
