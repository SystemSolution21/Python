# decorator_register.py
"""
This script demonstrates the use of decorators for registering exporters.
"""

import csv
import io
import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from fpdf import FPDF

current_dir: Path = Path(__file__).parent
output_dir: Path = current_dir / "output"
output_dir.mkdir(parents=True, exist_ok=True)

type Data = list[dict[str, Any]]
type ExportFunc = Callable[[Data], None]

exporters: dict[str, ExportFunc] = {}


def register_exporter(format: str) -> Callable[[ExportFunc], ExportFunc]:
    """Register an exporter.
    Args:
        format (str): The format of the exporter.
    """

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
    """Export data to PDF and print debug info to CLI.
    Args:
        data (Data): The data to export.
    """
    current_dir = Path(__file__).parent
    output_dir = current_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_file = output_dir / "data.pdf"
    print(f"[DEBUG] Saving PDF to: {pdf_file}")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    headers = list(data[0].keys())
    print(f"[DEBUG] Headers: {headers}")
    pdf.cell(200, 10, " | ".join(headers), ln=True)

    for i, row in enumerate(data):
        line = " | ".join(str(row.get(h, "")) for h in headers)
        print(f"[DEBUG] Row {i + 1}: {line}")
        pdf.cell(200, 10, line, ln=True)

    pdf.output(str(pdf_file))
    print("[DEBUG] PDF export complete.")


@register_exporter(format="csv")
def export_csv(data: Data) -> None:
    """Export data to csv.
    Args:
        data (Data): The data to export.
    """
    # In-memory csv data
    output = io.StringIO()
    writer: csv.DictWriter[str] = csv.DictWriter(f=output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    csv_data: str = output.getvalue()
    print(csv_data, end="")

    # export csv data to file
    csv_file: Path = output_dir / "data.csv"
    with open(file=csv_file, mode="w", encoding="utf-8", newline="") as file:
        file.write(csv_data)
        print(f"[INFO] CSV saved to: {csv_file}")


@register_exporter(format="json")
def export_json(data: Data) -> None:
    """Export data to json.
    Args:
        data (Data): The data to export.
    """
    # convert data to json
    json_data: str = json.dumps(data, indent=2)
    print(json_data)

    # export json data to file
    json_file: Path = output_dir / "data.json"
    with open(file=json_file, mode="w", encoding="utf-8") as file:
        file.write(json_data)
        print(f"[INFO] JSON saved to: {json_file}")


@register_exporter(format="xml")
def export_xml(data: Data) -> None:
    """Export data to xml.
    Args:
        data (Data): The data to export.
    """
    # convert data to xml
    xml_data: str = ""
    for key, value in data[0].items():
        xml_data += f"<{key}>{value}</{key}>\n"
    print(xml_data, end="")

    # export xml data to file
    xml_file: Path = output_dir / "data.xml"
    with open(file=xml_file, mode="w", encoding="utf-8") as file:
        file.write(xml_data)
        print(f"[INFO] XML saved to: {xml_file}")


def export_data(data: Data, format: str) -> None:
    """Export data to the specified format."""
    exporter = exporters.get(format)
    if exporter is None:
        print(f"\nExporter for format {format} not found!")
    else:
        exporter(data)


def main() -> None:
    # Sample data
    data: Data = [{"name": "John", "age": 30}]

    export_data(data=data, format="pdf")
    export_data(data=data, format="csv")
    export_data(data=data, format="json")
    export_data(data=data, format="xml")
    export_data(data=data, format="yaml")


if __name__ == "__main__":
    main()
