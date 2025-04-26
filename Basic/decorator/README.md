# Decorator

Python decorators are a powerful feature that allows you to modify or extend the behavior of functions or methods without changing their structure. They are applied using the @decorator_name syntax, placed above the function definition. Essentially, a decorator is a function that takes another function as its argument and returns a new function with additional functionality.

## decorator.py: Application & Execution Decorator

The order in which decorators are applied to a function is critical because it determines the sequence in which their behaviors are executed. When multiple decorators are stacked on a function, they are applied from top to bottom but executed from the inside out (i.e., bottom to top). This happens because a decorator wraps the function, and subsequent decorators wrap the already-decorated function.

Execution Flow:
Here’s the breakdown of how the decorators are applied and executed:

- Application Order (Top to Bottom):- @decorator2 is applied first, wrapping my_function.
- @decorator1 is applied next, wrapping the function already wrapped by decorator2.

- Execution Order (Inside Out):- Decorator 1: Before function execution (outer wrapper executes first).
- Decorator 2: Before function execution (inner wrapper executes next).
- The original function (my_function) executes.
- Decorator 2: After function execution (inner wrapper completes).
- Decorator 1: After function execution (outer wrapper completes).

Output:

- decorator1: call before my_function execution
- decorator2: call before my_function execution
- Executing my_function.....
- decorator2: call after my_function execution
- decorator1: call after my_function execution

## auth_log_decorator.py: Authentication and Logging

This script demonstrates the use of decorators for authentication and logging.

The script uses two decorators: authenticate and log_access.

The authenticate decorator checks if a user is authorized to access a function. If the user is not authorized, it logs a warning and returns "Access Denied". If the user is authorized, it calls the function.

The log_access decorator logs the access of a function. It logs the function name and the arguments passed to it before calling the function. It also logs the return value of the function after it is called.

The script also demonstrates the use of multiple decorators on a single function. The order of the decorators matters, as the innermost decorator is executed first.

Output:

- INFO - Accessing: view_profile with arguments: (101,), {}
- Profile of user 101: Alice
- WARNING - Unauthorized access attempt by user 202
- Access Denied
- WARNING - User ID 303 does not exist.
- User does not exist
