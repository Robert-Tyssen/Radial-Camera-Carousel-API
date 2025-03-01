from django.urls import path
from .views import heartbeat_check, analysis_state, demo_analysis, submit_analysis

urlpatterns = [
  path('heartbeat-check', heartbeat_check),
  path('analysis-state', analysis_state),
  path('demo-analysis', demo_analysis),
  path('submit-analysis', submit_analysis),
]