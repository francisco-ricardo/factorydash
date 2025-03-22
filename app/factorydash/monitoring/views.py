"""
This module defines views for the monitoring app in the factorydash project.

Views handle rendering the real-time manufacturing dashboard with NIST machine data.
"""

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from .models import MachineData
from datetime import timedelta
from typing import Optional, Literal, Dict, Any
import factorydash  # For logging


def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Renders the real-time manufacturing dashboard.

    Displays machine metrics filtered by time range, with the latest data highlighted.

    Args:
        request (HttpRequest): The incoming HTTP request, optionally with 'range' GET parameter.

    Returns:
        HttpResponse: Rendered dashboard template with machine data context.
    """
    time_range: Literal['hour', 'day', 'week'] = request.GET.get('range', 'hour')  # type: ignore
    if time_range == 'day':
        cutoff = timezone.now() - timedelta(days=1)
    elif time_range == 'week':
        cutoff = timezone.now() - timedelta(weeks=1)
    else:
        cutoff = timezone.now() - timedelta(hours=1)

    data = MachineData.objects.filter(timestamp__gte=cutoff).order_by('-timestamp')

    latest: Optional[MachineData] = data.first()
    latest_metrics = data[:10]  # Reuse data query for efficiency

    if not latest:
        factorydash.logger.warning(f"No MachineData found for time range: {time_range}, cutoff: {cutoff}")

    context: Dict[str, Any] = {
        'data': data[:50],  # Limit for performance
        'latest_metrics': latest_metrics,
        'last_updated': latest.timestamp if latest else None,
        'time_range': time_range,
    }
    return render(request, 'monitoring/dashboard.html', context)


# EOF
