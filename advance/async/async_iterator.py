"""Asynchronous Iterator"""

import asyncio
from typing import Self


class AsyncRange:
    """
    An asynchronous iterator that generates a range of integers.

    This class implements the asynchronous iterator protocol by defining
    __aiter__ and __anext__ methods.
    """

    def __init__(self, start: int, end: int) -> None:
        """
        Initialize the AsyncRange with start and end values.

        Args:
            start: The starting integer.
            end: The ending integer (inclusive).
        """
        self.start: int = start
        self.end: int = end

    def __aiter__(self) -> Self:
        """
        Return the asynchronous iterator object itself.

        Returns:
            The instance of AsyncRange.
        """
        return self

    async def __anext__(self) -> int:
        """
        Return the next integer in the range asynchronously.

        Raises:
            StopAsyncIteration: When the end of the range is reached.
        """
        if self.start > self.end:
            raise StopAsyncIteration
        else:
            await asyncio.sleep(delay=0.1)
            value: int = self.start
            self.start += 1
            return value


async def main() -> None:
    """
    Demonstrate the usage of the AsyncRange iterator using async for.
    """
    async for i in AsyncRange(start=1, end=10):
        print(i, end=" ")


if __name__ == "__main__":
    asyncio.run(main())
