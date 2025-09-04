from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
import ipaddress


class Command(BaseCommand):
    help = "Adds an IP address to the blocklist."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="The IP address to block.")

    def handle(self, *args, **options):
        ip_address_str = options["ip_address"]
        try:
            ipaddress.ip_address(ip_address_str)
            ip, created = BlockedIP.objects.get_or_create(ip_address=ip_address_str)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully blocked IP: {ip_address_str}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"IP address {ip_address_str} is already blocked."
                    )
                )
        except ValueError:
            raise CommandError(f'"{ip_address_str}" is not a valid IP address.')
