from threading import Thread
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.analysis_manager import global_analysis_manager
from api.serializers import AnalysisSubmissionSerializer

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
    
# Submits an analysis with the provided request
@api_view(['POST'])
def submit_analysis(request):
  # Create a serializer to parse the 
  serializer = AnalysisSubmissionSerializer(data=request.data)

  # Validate the request data and trigger the analysis if everything is okay
  if serializer.is_valid():
    submitted_data = serializer.validated_data
    print(submitted_data)
    # Attempt to fetch a lock to start the analysis on a new thread
    with global_analysis_manager.lock:
      # Start analysis on a new thread, or fail if one is already in progress
      if global_analysis_manager.analysis_in_progress == False:
        thread = Thread(target = global_analysis_manager.analyze, args = (submitted_data, ))
        thread.start()
        return Response({"message": "Submitted"})
      else:
        return Response({"error": "analysis-in-progress"}, status=status.HTTP_403_FORBIDDEN)
  
  # Request was invalid - return an error
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  