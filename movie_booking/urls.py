from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Booking API",
        default_version="v1",
        description="API docs for Movie Ticket Booking System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ------------------ Swagger JWT settings ------------------
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "USE_SESSION_AUTH": False,  # removes username/password boxes
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("booking.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
