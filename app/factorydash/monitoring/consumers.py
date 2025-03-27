"""
This module defines WebSocket consumers for the monitoring app in the 
factorydash project.

Consumers handle real-time updates for the dashboard via 
Django Channels.
"""
import factorydash # For logging

import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MachineData
from asgiref.sync import sync_to_async
from django.db.models import Window, F
from django.db.models.functions import RowNumber
from typing import Any

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


    async def receive(self, text_data):
        """
        Handles receiving messages from the client.

        Expects a JSON payload with page number.
        """
        try:
            data = json.loads(text_data)
            page_number = data.get('page', 1)
            await self.send_dashboard_data(page_number)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
        except Exception as e:
            factorydash.logger.error(f"WebSocket receive error: {str(e)}")
            await self.send(text_data=json.dumps({'error': 'Server error'}))


    async def send_dashboard_data(self, page_number: int = 1) -> None:
        """
        Sends updated machine data to the client with pagination.

        Args:
            page_number (int): The number of the page to fetch data from.
        """
        try:
            page_size = 20
            offset = (page_number - 1) * page_size

            # Get the latest overall timestamp
            latest_timestamp = await sync_to_async(
                lambda: MachineData.objects.latest('timestamp').timestamp 
                if MachineData.objects.exists() else timezone.now()
            )()
            last_updated_str = latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Fetch latest entries, prioritizing most recent unique data items
            latest_entries = await sync_to_async(
                lambda: list(
                    MachineData.objects.annotate(
                        row_num=Window(
                            expression=RowNumber(),
                            partition_by=[F('machine_id'), F('name')],
                            order_by=F('timestamp').desc()
                        )
                    )
                    .filter(row_num=1)
                    #.order_by('-timestamp', 'machine_id', 'name')
                    .order_by('machine_id', '-timestamp', 'name')
                    .values('timestamp', 'machine_id', 'name', 'value')
                    [offset:offset+page_size]
                )
            )()

            data = {
                'last_updated': last_updated_str,
                'table_data': latest_entries,
                'has_more': len(latest_entries) == page_size,
            }

            await self.send(text_data=json.dumps(data, default=str))

        except Exception as e:
            factorydash.logger.error(f"Error in send_dashboard_data: {str(e)}")
            await self.send(text_data=json.dumps({'error': str(e)}))



