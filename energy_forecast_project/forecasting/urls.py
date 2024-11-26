from django.urls import path
from .views import forecast_view
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE")})


urlpatterns = [
      path("api/csrf/", csrf),
    path("api/forecast/", forecast_view),  # API endpoint
    path("", TemplateView.as_view(template_name="react/index.html")),  # React app
]
