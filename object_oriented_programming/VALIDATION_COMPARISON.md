# Validation Comparison: Manual vs Pydantic

This document compares two approaches to implementing property validation in Python:

1. **Manual validation** using `@property` decorators (`main.py`)
2. **Pydantic validation** using BaseModel (`main_pydantic.py`)

Both implementations provide the same real-world validation features following industry best practices.

---

## 📊 Feature Comparison

| Feature | Manual (`main.py`) | Pydantic (`main_pydantic.py`) |
| --------- | ------------------- | ------------------------------ |
| **Type Validation** | Manual `isinstance()` checks | ✅ Automatic |
| **Field Constraints** | Custom validators | ✅ Built-in `Field()` constraints |
| **Email Validation** | Custom regex | ✅ `EmailStr` or custom validator |
| **Luhn Algorithm** | Custom implementation | Custom implementation |
| **Validation Timing** | On property assignment | On instantiation + assignment |
| **Error Messages** | Custom `ValidationError` | ✅ Detailed `ValidationError` |
| **JSON Serialization** | Manual implementation | ✅ Built-in `model_dump_json()` |
| **Dict Creation** | Not supported | ✅ `Model(**dict)` |
| **Whitespace Handling** | Manual `.strip()` | ✅ Automatic |
| **Code Verbosity** | More verbose | Less boilerplate |
| **Dependencies** | None (stdlib only) | `pydantic` package |

---

## ✅ Validation Features (Both Implementations)

### 1. **Amount Validation**

- Type checking (int/float only)
- Minimum value: $0.01
- Maximum value: $999,999.99
- Decimal precision: 2 places max
- Prevents overflow and abuse

### 2. **Credit Card Number Validation**

- **Luhn algorithm** (industry-standard checksum)
- Length: 13-19 digits
- Format flexibility: accepts "4111-1111-1111-1111" or "4111 1111 1111 1111"
- Automatic normalization (removes spaces/dashes)
- Type validation (string required)

### 3. **Cardholder Name Validation**

- Non-empty requirement
- Length: 2-50 characters
- Character whitelist: letters, spaces, `-`, `'`, `.`
- First + Last name required (min 2 words)
- Handles complex names: "Mary-Jane O'Brien Jr."

### 4. **Email Validation**

- RFC 5322 compliant regex
- Max length: 254 characters (RFC 5321)
- Local part max: 64 characters
- Automatic normalization (lowercase, trim)
- Format validation (must have `@` and domain)

---

## 🔧 Code Examples

### Manual Property Validation (`main.py`)

```python
class CreditCardPayment(Payment):
    def __init__(self, card_number: str, holder: str) -> None:
        self.card_number = card_number  # Triggers @card_number.setter
        self.holder = holder
    
    @property
    def card_number(self) -> str:
        return self.__card_number
    
    @card_number.setter
    def card_number(self, value: str) -> None:
        Validators.validate_card_number(value)
        self.__card_number = value.replace(" ", "").replace("-", "")
    
    def process(self, amount: float) -> str:
        Validators.validate_amount(amount)
        # ... process payment
```

**Pros:**

- ✅ No external dependencies
- ✅ Full control over validation logic
- ✅ Explicit and readable
- ✅ Works with any Python version

**Cons:**

- ❌ More boilerplate code
- ❌ Manual type checking required
- ❌ No built-in serialization
- ❌ More code to maintain

### Pydantic Validation (`main_pydantic.py`)

```python
class CreditCardPaymentModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    card_number: str = Field(..., min_length=13, max_length=19)
    holder: str = Field(..., min_length=2, max_length=50)
    
    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        # Clean and validate
        clean = v.replace(" ", "").replace("-", "")
        if not LuhnValidator.validate(clean):
            raise ValueError("Invalid card number")
        return clean
```

**Pros:**

- ✅ Less boilerplate code
- ✅ Automatic type validation
- ✅ Built-in JSON/dict support
- ✅ Better error messages
- ✅ IDE autocomplete support
- ✅ OpenAPI schema generation

**Cons:**

- ❌ External dependency (`pydantic`)
- ❌ Learning curve for Pydantic API
- ❌ Some advanced features require understanding Pydantic internals

---

## 🎯 When to Use Each Approach

### Use **Manual Validation** (`main.py`) when

- No external dependencies allowed
- Full control over validation logic needed
- Working with legacy Python versions
- Simple validation requirements
- Educational purposes (learning OOP concepts)

### Use **Pydantic** (`main_pydantic.py`) when

- Building APIs (FastAPI integration)
- Need JSON serialization
- Working with configuration files
- Complex data models
- Want comprehensive validation with less code
- Building production applications

---

## 🧪 Testing Both Implementations

Run the manual validation version:

```bash
python object_oriented_programming/main.py
```

Run the Pydantic validation version:

```bash
python object_oriented_programming/main_pydantic.py
```

Both scripts include comprehensive test suites demonstrating:

- ✅ Valid transactions
- ❌ Invalid input handling (14+ test cases)
- 🎯 Edge cases (formatted card numbers, special characters)

---

## 📚 Key Takeaways

1. **Same Features, Different Approaches**: Both implement identical validation logic
2. **Trade-offs**: Manual = more control, Pydantic = less code
3. **Production Ready**: Both are suitable for real-world applications
4. **Best Practices Applied**: Luhn algorithm, RFC compliance, PCI-DSS masking
5. **Extensibility**: Both can be extended with additional validators

---

## 🔗 Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PCI-DSS Compliance](https://www.pcisecuritystandards.org/)
- [Luhn Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm)
- [RFC 5322 (Email)](https://datatracker.ietf.org/doc/html/rfc5322)

---

**Created**: 2026-04-04  
**Files**: `main.py`, `main_pydantic.py`
