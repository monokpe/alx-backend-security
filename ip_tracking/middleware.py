from .models import RequestLog, BlockedIP
from ipware import get_client_ip
from django.core.cache import cache


from typing import Callable
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden


class IPLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        self.blocked_ips = set(BlockedIP.objects.values_list("ip_address", flat=True))

    def __call__(self, request: HttpRequest) -> HttpResponse:
        ip, _ = get_client_ip(request)
        if ip in self.blocked_ips:
            return HttpResponseForbidden("Your IP has been blocked.")

        country = None
        city = None

        if ip:
            cache_key = f"geolocation_{ip}"
            geolocation_data = cache.get(cache_key)

            if not geolocation_data:

                if hasattr(request, "geolocation"):
                    country_data = getattr(request.geolocation, "country", {})
                    country = (
                        country_data.get("name")
                        if isinstance(country_data, dict)
                        else None
                    )
                    city = getattr(request.geolocation, "city", None)

                    geolocation_data = {"country": country, "city": city}

                    cache.set(cache_key, geolocation_data, timeout=86400)

            if geolocation_data:
                country = geolocation_data.get("country")
                city = geolocation_data.get("city")

            RequestLog.objects.create(
                ip_address=ip, path=request.path, country=country, city=city
            )

        response = self.get_response(request)
        return response

    def refresh_blocked_ips(self) -> None:
        """
        Refreshes the cached set of blocked IPs.
        This can be called periodically or after an IP is blocked.
        """
        self.blocked_ips = set(BlockedIP.objects.values_list("ip_address", flat=True))
