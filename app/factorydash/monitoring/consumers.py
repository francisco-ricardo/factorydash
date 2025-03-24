"""
This module defines WebSocket consumers for the monitoring app in the 
factorydash project.

Consumers handle real-time updates for the dashboard via 
Django Channels.
"""
import factorydash # For logging

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MachineData
from asgiref.sync import sync_to_async
from django.utils import timezone
from datetime import timedelta
from typing import Dict, Any

class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time dashboard updates.

    Broadcasts the latest machine data to connected clients.
    """

    async def connect(self) -> None:
        """
        Handles WebSocket connection establishment.

        Adds the client to the 'dashboard' group.
        """
        try:
            await self.channel_layer.group_add('dashboard', self.channel_name)
            await self.accept()            
        except Exception as e:
            factorydash.logger.error(f"WebSocket connect error: {str(e)}")
            await self.close(code=1011)  # Internal error
        else:
            factorydash.logger.info("WebSocket connected to dashboard group")


    async def disconnect(self, close_code: int) -> None:
        """
        Handles WebSocket disconnection.

        Removes the client from the 'dashboard' group.

        Args:
            close_code (int): The WebSocket close code.
        """
        await self.channel_layer.group_discard('dashboard', self.channel_name)
        factorydash.logger.info(f"WebSocket disconnected with code: {close_code}")


    async def update_data(self, event: Dict[str, Any]) -> None:
        """
        Sends updated machine data to the client.

        Args:
            event (Dict[str, Any]): The event data from the channel layer.
        """
        try:
            latest = await sync_to_async(MachineData.objects.latest)('timestamp')
            last_updated_str = latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')

            all_entries = await sync_to_async(
                lambda: list(MachineData.objects.order_by('name', '-timestamp').all())
            )()

            latest_entries_dict: Dict[str, MachineData] = {}
            for entry in all_entries:
                if entry.name not in latest_entries_dict:
                    latest_entries_dict[entry.name] = entry

            # Sort by data_item_id and then by timestamp
            sorted_entries = sorted(
                latest_entries_dict.values(),
                key=lambda entry: (entry.data_item_id, -entry.timestamp.timestamp())
            )

            table_data: List[Dict[str, Any]] = []
            for entry in sorted_entries:
                table_data.append({
                    'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'data_item_id': entry.data_item_id,
                    'name': entry.name,
                    'value': entry.value,
                })

            data = {
                'last_updated': last_updated_str,
                'table_data': table_data,
            }

            await self.send(text_data=json.dumps(data))

        except MachineData.DoesNotExist:
            factorydash.logger.warning("No MachineData available to send")
            await self.send(text_data=json.dumps({
                'last_updated': 'N/A',
                'table_data': [],
            }))

        except Exception as e:
            factorydash.logger.error(f"Error in update_data: {str(e)}")
            await self.send(text_data=json.dumps({'error': 'Server error'}))

        else:
            factorydash.logger.info(f"Data updated: {data}")