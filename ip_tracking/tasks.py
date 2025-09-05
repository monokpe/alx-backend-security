from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    suspicious_by_rate = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=Count("id"))
        .filter(request_count__gt=100)
    )

    for item in suspicious_by_rate:
        SuspiciousIP.objects.update_or_create(
            ip_address=item["ip_address"],
            defaults={
                "reason": f"Exceeded 100 requests in an hour ({item['request_count']} requests)."
            },
        )

    sensitive_paths = ["/admin/", "/login/"]
    suspicious_by_path = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
        .values("ip_address")
        .distinct()
    )

    for item in suspicious_by_path:
        SuspiciousIP.objects.update_or_create(
            ip_address=item["ip_address"],
            defaults={"reason": "Accessed sensitive paths."},
        )
