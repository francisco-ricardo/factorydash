"""
This module defines WebSocket consumers for the monitoring app in the 
factorydash project.

Consumers handle real-time updates for the dashboard via 
Django Channels.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MachineData
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
        await self.channel_layer.group_add('dashboard', self.channel_name)
        await self.accept()


    async def disconnect(self, close_code: int) -> None:
        """
        Handles WebSocket disconnection.

        Removes the client from the 'dashboard' group.

        Args:
            close_code (int): The WebSocket close code.
        """
        await self.channel_layer.group_discard('dashboard', self.channel_name)


    async def update_data(self, event: Dict[str, Any]) -> None:
        """
        Sends updated machine data to the client.

        Args:
            event (Dict[str, Any]): The event data from the channel layer.
        """
        latest = MachineData.objects.latest('timestamp')
        await self.send(text_data=json.dumps({
            'last_updated': latest.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': latest.value if latest.name == 'temperature' else None,
            'spindle_speed': latest.value if latest.name == 'spindle_speed' else None,
            # Add other metrics based on name/value pairs
        }))

    