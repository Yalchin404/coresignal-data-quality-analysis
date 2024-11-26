import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def extract_employees_data(
    input_dir: str = "company_data", output_dir: str = "team"
) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    for json_file in input_path.glob("*.json"):
        try:
            print(f"Processing {json_file.name}")
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            employees_data = data.get("company_featured_employees_collection", [])
            output_file = Path(output_dir) / json_file.name
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(employees_data, f, indent=4)

            print(f"Successfully saved employees data to {output_file}")
            print(f"Found {len(employees_data)} employees")

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {json_file.name}: {str(e)}")
        except KeyError as e:
            print(f"Error: Missing key in {json_file.name}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error processing {json_file.name}: {str(e)}")


def print_summary(input_dir: str = "company_data", output_dir: str = "team") -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists() or not output_path.exists():
        print("Cannot generate summary - one or both directories don't exist")
        return

    input_files = list(input_path.glob("*.json"))
    output_files = list(output_path.glob("*.json"))

    print("\nProcessing Summary:")
    print(f"Total input files: {len(input_files)}")
    print(f"Total output files: {len(output_files)}")
    print("\nDetailed Summary:")
    total_employees = 0

    for file in output_path.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                employee_count = len(data)
                total_employees += employee_count
                print(f"{file.name}: {employee_count} employees")
        except Exception as e:
            print(f"Error reading {file.name}: {str(e)}")

    print(f"\nTotal employees across all companies: {total_employees}")


if __name__ == "__main__":
    extract_employees_data()
    print_summary()
