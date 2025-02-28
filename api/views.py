from threading import Thread
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.analysis_manager import global_analysis_manager

# Returns a simple success message so front-end can confirm endpoint is correct
@api_view(['GET'])
def heartbeat_check(request):
  return Response({"message": "Connection successful!"})

# Gets the current state of the analysis
@api_view(['GET'])
def analysis_state(request):
  analysis_state = global_analysis_manager.get_state()
  return Response(analysis_state)

# Submits a demonstration analysis request
@api_view(['GET'])
def demo_analysis(request):
  mapping = {0: [1, 2, 3], 1: [2, 5], 2: [1, 4], 14:[7]}
  with global_analysis_manager.lock:
    if global_analysis_manager.analysis_in_progress == False:
      thread = Thread(target = global_analysis_manager.analyze, args = (mapping, ))
      thread.start()
      return Response({"message": "Analysis submitted"})
    else:
      return Response({"error": "Cannot submit, analysis already in progress"})