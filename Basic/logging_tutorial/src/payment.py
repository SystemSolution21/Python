# payment.py
import logging
import random
import time
from pathlib import Path

# Create log file
log_file: Path = Path(__file__).parent.parent / "logs" / "payment.log"

# Configure logging
logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.DEBUG,
    # format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    format="{asctime} - {levelname} - {module} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger: logging.Logger = logging.getLogger(name=__name__)


# Inventory availability
def check_inventory(item_id: str, quantity: int) -> str:
    """Check inventory availability."""

    logger.debug(f"Checking inventory | item: {item_id} | quantity: {quantity}")
    time.sleep(1)
    if random.choice([True, False]):
        raise Exception("Inventory service down!")

    logger.info(f"Inventory available | item: {item_id} | quantity: {quantity}")
    return "available"


# Payment processing
def process_payment(user_id: str, amount: float) -> str:
    """Process payment."""

    logger.debug(f"Processing payment | user: {user_id} | amount: {amount}")
    time.sleep(1)
    if random.choice([True, False]):
        logger.warning(f"Payment gateway is slow | user: {user_id}")

    logger.info(f"Payment processed | user: {user_id} | amount: {amount}")
    return "processed"


# Order confirmation
def confirm_order(
    order_id: str, user_id: str, item_id: str, quantity: int, amount: float
) -> str:
    """Confirm order."""
    logger.info(
        f"Order confirmed | user: {user_id} | order: {order_id} | item: {item_id} | quantity: {quantity} | amount: {amount}"
    )
    return "confirmed"


# Order handling
def handle_order(
    order_id: str, user_id: str, item_id: str, quantity: int, amount: float
) -> str:
    """Handle order."""

    logger.info(
        f"New order received | order: {order_id} | user: {user_id} | item: {item_id} | quantity: {quantity} | amount: {amount}"
    )

    try:
        check_inventory(item_id, quantity)
        process_payment(user_id, amount)
        confirm_order(order_id, user_id, item_id, quantity, amount)
        logger.info(f"Order processed successfully | order: {order_id}")
        return "Order completed"
    except Exception as e:
        logger.error(f"Order failed | Order: {order_id} | Reason: {e}")
        return "Order failed"


def main() -> None:
    """Simulate multiple orders."""

    for i in range(1, 4, 1):
        order_id: str = f"Order_{i}"
        user_id: str = f"User_{i}"
        item_id: str = f"Item_{i}"
        quantity: int = i
        amount: float = quantity * 10.00

        handle_order(
            order_id=order_id,
            user_id=user_id,
            item_id=item_id,
            quantity=quantity,
            amount=amount,
        )


if __name__ == "__main__":
    main()
