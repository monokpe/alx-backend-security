# ALX Backend Security

A Django project for tracking, logging, and securing incoming requests with advanced middleware, geolocation, rate limiting, and suspicious activity detection.

## Features

- **IP Logging Middleware**: Logs the IP address, timestamp, path, country, and city of every incoming request.
- **Blocked IPs**: Block specific IP addresses from accessing the application.
- **Suspicious IP Detection**: Detects and logs suspicious IPs based on request rate and access to sensitive paths using scheduled Celery tasks.
- **Geolocation Support**: Integrates with geolocation middleware to enrich logs with country and city information.
- **Rate Limiting**: Uses `django_ratelimit` to protect sensitive views from abuse.
- **Management Commands**: Easily block IPs via custom Django management commands.
- **Celery Integration**: Periodic tasks for automated security checks.

## Setup

### Prerequisites

- Python 3.8+
- Django 5.x
- Redis (for Celery broker)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/monokpe/alx-backend-security.git
   cd alx-backend-security
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install django-ipware django_ratelimit celery redis
   ```
3. Apply migrations:
   ```sh
   python manage.py migrate
   ```
4. Run the development server:
   ```sh
   python manage.py runserver
   ```
5. Start Celery worker and beat:
   ```sh
   celery -A ip_tracking worker -l info
   celery -A ip_tracking beat -l info
   ```

## Usage

- **Blocking an IP:**
  ```sh
  python manage.py block_ip <ip_address>
  ```
- **Rate-Limited View:**
  Example in `ip_tracking/views.py`:
  ```python
  @ratelimit(group='sensitive', key='ip')
  def sensitive_view(request):
      ...
  ```
- **Suspicious IPs:**
  Detected and stored in the `SuspiciousIP` model. Scheduled hourly by Celery.

## Project Structure

```
manage.py
ip_tracking/
    __init__.py
    asgi.py
    middleware.py
    models.py
    settings.py
    tasks.py
    urls.py
    views.py
    wsgi.py
    management/
        commands/
            block_ip.py
```

## Security Best Practices

- Keep your `SECRET_KEY` safe and never expose it publicly.
- Set `DEBUG = False` in production.
- Use strong password validation and HTTPS.
- Regularly monitor and update dependencies.

## License

This project is licensed under the MIT License.

## Author

[monokpe](https://github.com/monokpe)
