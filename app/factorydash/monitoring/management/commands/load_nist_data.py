import factorydash  # This will set up the Django environment

import requests
import xml.etree.ElementTree as ET
import pytz
from datetime import datetime
from typing import Generator, Dict, Any, Optional
from django.core.management.base import BaseCommand

from monitoring.models import MachineData


class Command(BaseCommand):
    help = "Fetches and saves XML data from the NIST API."


    def handle(self, *args, **kwargs) -> None:
        """Fetch, parse, and save data to the database."""
        xml_data = self.fetch_nist_data()
        if not xml_data:
            factorydash.logger.error("No XML data received from NIST API.")
            return
        
        count = 0
        parsed_data = self.parse_nist_xml(xml_data)
        for entry in parsed_data:
            MachineData.objects.create(
                data_type=entry["data_type"],
                data_item_id=entry["data_item_id"],
                timestamp=entry["timestamp"],
                name=entry["name"],
                value=entry["value"]
            )
            count += 1

        factorydash.logger.info(f"Successfully saved {count} records from NIST API.")


    def fetch_nist_data(self) -> Optional[str]:
        """Fetch XML data from the NIST API."""
        NIST_API_URL = "https://smstestbed.nist.gov/vds/current"
        response = requests.get(NIST_API_URL)
        if response.status_code == 200:
            factorydash.logger.info("Successfully fetched XML data from NIST API.")
            return response.text
        factorydash.logger.error("Failed to retrieve data from NIST API")
        return None

    
    def parse_nist_xml(self, xml_data: str) -> Generator[Dict[str, Any], None, None]:
        """Parse XML and extract Events, Samples, and Conditions."""
        root = ET.fromstring(xml_data)
        ns = {"ns": root.tag.split("}")[0].strip("{")}
        
        utc = pytz.UTC  # Define UTC timezone

        # Extract data from Events, Samples, and Condition
        for data_type, xpath in [("Events", ".//ns:Events/*"), 
                                 ("Samples", ".//ns:Samples/*"), 
                                 ("Condition", ".//ns:Condition/*")]:
            for element in root.findall(xpath, ns):
                timestamp_str = element.attrib.get("timestamp", "").strip()

                # Convert timestamp to a timezone-aware datetime
                timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
                if timestamp and timestamp.tzinfo is None:
                    timestamp = utc.localize(timestamp)

                record = {
                    "data_type": data_type,
                    "data_item_id": element.attrib.get("dataItemId", "").strip(),
                    "timestamp": timestamp,
                    "name": element.tag.split("}")[1].strip() if "}" in element.tag else element.tag.strip(),
                    "value": element.text.strip() if element.text else None,
                }

                factorydash.logger.info(f"Parsed Record: {record}")  # Log parsed data
                yield record

    
    # EOF
