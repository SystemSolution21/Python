# decorator_register.py
"""
This script demonstrates the use of decorators for registering exporters.
"""

import json
from functools import wraps
from typing import Any, Callable

type Data = dict[str, Any]
type ExportFunc = Callable[[Data], None]

exporters: dict[str, ExportFunc] = {}


def register_exporter(format: str) -> Callable[[ExportFunc], ExportFunc]:
    def decorator(func: ExportFunc) -> ExportFunc:
        @wraps(wrapped=func)
        def wrapper(data: Data) -> None:
            print(f"\nExporting data using {format} exporter...")
            return func(data)

        # Register the exporter
        exporters[format] = wrapper
        return wrapper

    return decorator


@register_exporter(format="pdf")
def export_pdf(data: Data) -> None:
    print(data)


@register_exporter(format="csv")
def export_csv(data: Data) -> None:
    # convert data to csv
    csv_data: str = ""
    for key, value in data.items():
        csv_data += f"{key},{value}\n"
    print(csv_data)


@register_exporter(format="json")
def export_json(data: Data) -> None:
    print(json.dumps(data, indent=2))


@register_exporter(format="xml")
def export_xml(data: Data) -> None:
    # convert data to xml
    xml_data: str = ""
    for key, value in data.items():
        xml_data += f"<{key}>{value}</{key}>\n"
    print(xml_data)


def export_data(data: Data, format: str) -> None:
    exporter: Callable[[dict[str, Any]], None] | None = exporters.get(format)
    if exporter is None:
        print(f"Exporter for format {format} not found!")
    else:
        exporter(data)


def main() -> None:
    # Sample data
    data: Data = {"name": "John", "age": 30}

    export_data(data=data, format="pdf")
    export_data(data=data, format="csv")
    export_data(data=data, format="json")
    export_data(data=data, format="xml")
    export_data(data=data, format="yaml")


if __name__ == "__main__":
    main()
