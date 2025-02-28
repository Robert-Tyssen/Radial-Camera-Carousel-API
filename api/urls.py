from django.urls import path
from .views import heartbeat_check

urlpatterns = [
  path('heartbeat-check', heartbeat_check)
]