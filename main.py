import json
import os
from pathlib import Path
import requests
import time
from typing import List, Optional


API_KEY = os.getenv("CORESIGNAL_API_KEY")


def fetch_company_detail(company_id: int, api_key: str) -> Optional[dict]:
    url = f"https://api.coresignal.com/cdapi/v1/professional_network/company/collect/{company_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching details for company ID {company_id}: {str(e)}")
        return None


def fetch_company_data(
    websites: List[str], api_key: str, output_dir: str = "company_data"
) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    search_url = (
        "https://api.coresignal.com/cdapi/v1/professional_network/company/search/filter"
    )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    for website in websites:
        try:
            print(f"\nProcessing website: {website}")
            payload = json.dumps({"website": website})
            search_response = requests.post(search_url, headers=headers, data=payload)
            search_response.raise_for_status()

            company_ids = search_response.json()
            filename = f"{website.replace('.', '_')}.json"
            filepath = Path(output_dir) / filename

            if not company_ids:
                print(f"No company IDs found for {website}")
                continue

            print(f"Found {company_ids} company IDs. Using first ID: {company_ids[0]}")
            company_details = fetch_company_detail(company_ids[0], api_key)

            if company_details:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(company_details, f, indent=4)
                print(f"Successfully saved company details for {website} to {filepath}")
            else:
                print(f"Failed to fetch company details for {website}")

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error processing {website}: {str(e)}")
            if hasattr(e.response, "text"):
                print(f"Response content: {e.response.text}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {website}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error processing {website}: {str(e)}")


def read_websites_from_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    websites_to_process = [
        "www.ezyev.in",
    ]

    fetch_company_data(websites_to_process, API_KEY)
