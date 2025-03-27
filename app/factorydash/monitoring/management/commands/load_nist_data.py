import factorydash  # This will set up the Django environment

import requests
import xml.etree.ElementTree as ET
import pytz
from datetime import datetime
from typing import Generator, Dict, Any, Optional
from django.core.management.base import BaseCommand

from xml.etree.ElementTree import iterparse
from io import StringIO

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
                machine_id=entry["data_item_id"],
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
        """
        Parse XML and extract specified fields with improved performance.
    
        Extracted fields:
        - Events: Availability, EmergencyStop
        - Samples: Xfrt, Yfrt, Zfrt, Xposition, Yposition, Zposition, Temperature, AccumulatedTime, PathFeedRate, RotaryVelocity
        """

        # Specify allowed fields
        ALLOWED_EVENTS = {'Availability', 'EmergencyStop'}
        ALLOWED_SAMPLES = {
            'Xfrt', 'Yfrt', 'Zfrt', 
            'Xposition', 'Yposition', 'Zposition', 
            'Temperature', 'AccumulatedTime', 
            'PathFeedRate', 'RotaryVelocity'
        }

        utc = pytz.UTC  # Define UTC timezone
        
        # Use iterparse for memory-efficient parsing
        for event, elem in iterparse(StringIO(xml_data), events=('end',)):
            # Check if the element is in allowed events or samples
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            
            if tag in ALLOWED_EVENTS or tag in ALLOWED_SAMPLES:
                timestamp_str = elem.attrib.get("timestamp", "").strip()
                
                # Convert timestamp to a timezone-aware datetime
                try:
                    timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
                    if timestamp and timestamp.tzinfo is None:
                        timestamp = utc.localize(timestamp)
                except ValueError:
                    timestamp = None

                record = {
                    "data_type": "Events" if tag in ALLOWED_EVENTS else "Samples",
                    "data_item_id": elem.attrib.get("dataItemId", "").strip(),
                    "timestamp": timestamp,
                    "name": tag,
                    "value": elem.text.strip() if elem.text else None,
                }

                yield record

            # Clear the element to free memory
            if elem.tag.endswith('}Streams'):
                elem.clear()
    
    
    
    
    
    
    
    
    def parse_nist_xml_orig(self, xml_data: str) -> Generator[Dict[str, Any], None, None]:
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
