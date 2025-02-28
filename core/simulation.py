from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from core.analysis_task import AnalysisTask
from core.camera import Camera, PhotoCarousel

class AnalysisManager:
  # Initializes the measurement with a provided mapping of each photo slot
  # and the desired camera(s) to analyze each slot
  def __init__(self):   
    # Create representation of cameras and camera positions for analysis
    # Cameras are positioned at every other photo slot in radial arrangement
    self.cameras = {i: Camera(i) for i in range(8)}
    self.camera_positions = {i: i * 2 for i in range(8)}

    # Create representation of the photo carousel
    self.carousel = PhotoCarousel()

    # Status of analysis
    self.analysis_in_progress = False

    # Current analysis tasks
    self.analysis_tasks: dict[tuple[int, int], AnalysisTask] = {}


  def analyze(self, photo_camera_mapping: dict[int, list[int]]):

    print('Starting analysis...')
    self.analysis_in_progress = True

    # Reset the carousel to its original position
    self.carousel.reset_rotation()

    # Instantiate a set of analysis tasks based on photo_camera_mapping input 
    self.analysis_tasks = {
      (slot, camera): AnalysisTask(slot, camera)
      for slot, cameras in photo_camera_mapping.items()
      for camera in cameras
    }

    # Iterate over the sixteen positions for the photo carousel
    for _ in range(16):
      print(f'Rotation step {self.carousel.rotation}')

      # Get the photo slots and cameras which are aligned based on rotation of the carousel
      pairs = self.carousel.get_camera_pairs(self.camera_positions)
      
      # List of parallel tasks to execute based on any (camera, photo) matches
      future_tasks = []

      # All cameras can run in parallel, depending on analysis tasks
      executor = ThreadPoolExecutor(max_workers=len(self.cameras))

      # Check if any of the analysis tasks match with the pairs found above,
      # and if so, queue them for parallel execution
      for ((photo, camera), task) in self.analysis_tasks.items():
        if (photo, camera) in pairs:
          print(f'Match found for photo {photo} camera {camera}')
          # Add tasks to thread pool so they can run concurrently
          future_tasks.append(executor.submit(self.cameras[camera].analyze, task))

      # Wait for all parallel tasks to complete
      for future in as_completed(future_tasks):
        future.result()
      
      # Minor delay to simulate carousel moving to next position
      self.carousel.rotate()
      time.sleep(1)

    print('Analysis complete!')
    self.analysis_in_progress = False

  def get_state(self):
    return {
      'analysis_in_progress': self.analysis_in_progress,
      'camera_states': { id: camera.get_state() for (id, camera) in self.cameras.items()},
      'analysis_tasks': [task.get_state() for (_, task) in self.analysis_tasks.items()]
    }


# Instantiate a global variable that we'll use for reference in the API
global_analysis_manager = AnalysisManager()