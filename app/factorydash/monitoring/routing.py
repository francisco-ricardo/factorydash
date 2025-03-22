"""
This module defines WebSocket URL routing for the monitoring app in the 
factorydash project.
"""

from django.urls import re_path
from . import consumers
from typing import List
from django.urls import URLPattern

websocket_urlpatterns: List[URLPattern] = [
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
]