import os
import sys
import django
import requests
import xml.etree.ElementTree as ET
import pytz
from datetime import datetime
from typing import List, Dict, Any, Optional

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")
django.setup()

from monitoring.models import MachineData


NIST_API_URL = "https://smstestbed.nist.gov/vds/current"


def fetch_nist_data() -> Optional[str]:
    """
    Fetch XML data from the NIST API.

    Returns:
        str: The XML data as a string if the request is successful.
        None: If the request fails.
    """
    response = requests.get(NIST_API_URL)
    if response.status_code == 200:
        return response.text
    print("Failed to retrieve data from NIST API")
    return None


def parse_nist_xml(xml_data: str) -> List[Dict[str, Any]]:
    """
    Parse XML and extract relevant data.

    Args:
        xml_data (str): The XML data as a string.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the extracted data.
    """
    root = ET.fromstring(xml_data)
    ns = {"ns": root.tag.split("}")[0].strip("{")}
    extracted_data = []
    
    utc = pytz.UTC  # Define UTC timezone

    for event in root.findall(".//ns:Events/*", ns):
        timestamp_str = event.attrib.get("timestamp", "")

        # Convert timestamp to a timezone-aware datetime
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
        if timestamp and timestamp.tzinfo is None:  
            timestamp = utc.localize(timestamp)  

        extracted_data.append({
            "data_type": "Events",
            "data_item_id": event.attrib.get("dataItemId", ""),
            "timestamp": timestamp,
            "name": event.tag.split("}")[1] if "}" in event.tag else event.tag,
            "value": event.text.strip() if event.text else None
        })

    return extracted_data


def save_nist_data() -> None:
    """
    Fetch, parse, and save data to the database.
    """
    xml_data = fetch_nist_data()
    if not xml_data:
        print("Failed to retrieve data from NIST API.")
        return

    parsed_data = parse_nist_xml(xml_data)
    for entry in parsed_data:
        MachineData.objects.create(
            data_type=entry["data_type"],
            data_item_id=entry["data_item_id"],
            timestamp=entry["timestamp"],
            name=entry["name"],
            value=entry["value"]
        )

    print(f"Successfully saved {len(parsed_data)} records from NIST API.")


# For testing locally:
if __name__ == "__main__":
    save_nist_data()


# EOF
