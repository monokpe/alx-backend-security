from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(group='sensitive', key='ip')
def sensitive_view(request):
    return HttpResponse("This is a rate-limited view.")

# Example of a login view with rate limiting
# from django.contrib.auth.views import LoginView
# from django.utils.decorators import method_decorator

# class MyLoginView(LoginView):
#     @method_decorator(ratelimit(group='sensitive', key='ip'))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)