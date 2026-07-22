from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
)

from django_scalar.views import scalar_viewer 
urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),

    path("api/", include("main.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('scalar/', scalar_viewer, name='scalar-viewer'),
    
]