import asyncio
from typing import Self


class AsyncRange:
    def __init__(self, start: int, end: int) -> None:
        self.start: int = start
        self.end: int = end

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> int:
        if self.start > self.end:
            raise StopAsyncIteration
        else:
            await asyncio.sleep(delay=0.1)
            value: int = self.start
            self.start += 1
            return value


async def main() -> None:
    async for i in AsyncRange(start=1, end=10):
        print(i, end=" ")


if __name__ == "__main__":
    asyncio.run(main())
