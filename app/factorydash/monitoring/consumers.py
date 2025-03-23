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
            factorydash.logger.info("WebSocket connected to dashboard group")
        except Exception as e:
            factorydash.logger.error(f"WebSocket connect error: {str(e)}")
            await self.close(code=1011)  # Internal error


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
            # Wrap sync ORM call in sync_to_async
            latest = await sync_to_async(MachineData.objects.latest)('timestamp')
            data = {
                'last_updated': latest.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': latest.value if latest.name == 'temperature' else 'N/A',
                'spindle_speed': latest.value if latest.name == 'spindle_speed' else 'N/A',
            }
            factorydash.logger.info(f"Sending update: {data}")
            await self.send(text_data=json.dumps(data))
        except MachineData.DoesNotExist:
            factorydash.logger.warning("No MachineData available to send")
            await self.send(text_data=json.dumps({
                'last_updated': 'N/A',
                'temperature': 'N/A',
                'spindle_speed': 'N/A',
            }))
        except Exception as e:
            factorydash.logger.error(f"Error in update_data: {str(e)}")

    