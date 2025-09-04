from .models import RequestLog, BlockedIP
from ipware import get_client_ip


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
        if ip:
            # Ensure path is a string and not None
            path = getattr(request, "path", "/")
            RequestLog.objects.create(ip_address=ip, path=path)

        response = self.get_response(request)
        return response

    def refresh_blocked_ips(self) -> None:
        """
        Refreshes the cached set of blocked IPs.
        This can be called periodically or after an IP is blocked.
        """
        self.blocked_ips = set(BlockedIP.objects.values_list("ip_address", flat=True))
