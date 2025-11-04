# Python Standard Library and Builtins

Python's standard library is a collection of modules that are included with every Python installation. These modules provide access to a wide range of functionality, from file I/O to network programming to data analysis. The standard library is documented in the [Python Standard Library](https://docs.python.org/3/library/index.html) section of the Python documentation.

## Built-in Functions

Python provides a set of built-in functions that are always available. These functions perform common or generic operations. Some of the commonly used built-in functions include:

- `print()`: Prints the specified message to the screen.
- `len()`: Returns the length (the number of items) of an object.
- `type()`: Returns the type of an object.
- `int()`, `float()`, `str()`: Convert a value to an integer, float, or string, respectively.
- `input()`: Reads a line of text from the user.
- `range()`: Generates a sequence of numbers.
- `abs()`: Returns the absolute value of a number.
- `round()`: Rounds a number to a specified number of decimal places.
- `max()`, `min()`: Returns the maximum or minimum value from a sequence of values.
- `sum()`: Returns the sum of all items in a sequence.

## Runtime Services

The runtime services are a set of modules that provide access to the Python interpreter's internal operations. These modules are not part of the standard library, but they are available in every Python installation. Some of the commonly used runtime services include:

- `sys`: Provides access to system-specific parameters and functions.
- `os`: Provides a portable way of using operating system dependent functionality.
- `io`: Provides access to low-level I/O operations.
- `time`: Provides access to time-related functions.
- `datetime`: Provides classes for manipulating dates and times.
- `calendar`: Provides functions for working with calendars.
- `random`: Provides functions for generating random numbers.
- `math`: Provides access to mathematical functions.
- `statistics`: Provides functions for statistical analysis.
- `itertools`: Provides functions for working with iterators.
- `functools`: Provides higher-order functions and operations on callable objects.
- `operator`: Provides functions that correspond to the intrinsic operators of Python.
- `contextlib`: Provides context managers for common tasks.
- `abc`: Provides the infrastructure for defining abstract base classes.
- `typing`: Provides support for type hints.
- `dataclasses`: Provides a decorator and functions for automatically adding generated special methods such as `__init__()` and `__repr__()` to user-defined classes.
- `enum`: Provides support for enumerations.

## Binary Sequence Types — bytes, bytearray, memoryview

The core built-in types for manipulating binary data are bytes and bytearray. They are supported by memoryview which uses the buffer protocol to access the memory of other binary objects without needing to make a copy.

The array module supports efficient storage of basic data types like 32-bit integers and IEEE754 double-precision floating values.
