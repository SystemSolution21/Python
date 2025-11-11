# Logging in Python

Logging is a way to record messages that describe the flow of a program. It is a useful tool for debugging and monitoring applications. Python provides a built-in logging module that can be used to log messages.

## Basic Logging

The basic configuration for logging can be done using the `basicConfig` function. This function takes a number of arguments that can be used to configure the logging module. The most common arguments are:

- `level`: The minimum level of messages to log. The default is `WARNING`.
- `format`: The format of the log messages.
- `datefmt`: The format of the date and time in the log messages.
- `filename`: The name of the file to log to.
- `filemode`: The mode to open the log file in. The default is `a` (append).
- `style`: The style of the log messages. The default is `%` (old style). The other option is `{` (new style).

## Custom Logging

Custom logging allows you to create multiple loggers with different configurations. This is useful when you want to log messages from different parts of your application with different levels of detail.

## Project Structure

```current directory
├── logging
│   ├── logs
│   │   ├── custom_logging.log
│   │   ├── errors.log
│   │   ├── payment.log
│   │   ├── root_logging.log
│   │   └── slack_warnings.log
│   ├── src
│   │   ├── __init__.py
│   │   ├── custom_logging.py
│   │   ├── filter_examples.py
│   │   └── payment.py
│   ├── FILTER_BEST_PRACTICES.md
│   ├── logging.md
│   └── .env
```
