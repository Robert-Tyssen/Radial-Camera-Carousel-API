import threading
import time
from core.analysis_task import AnalysisTask

class PhotoCarousel:
  # Class representing a rotating photo carousel containing 16 slots
  # Includes a list of slots [0, ..., 15], and a current rotation position
  def __init__(self, init_position = 0):
    self.slots = list(range(16))
    self.rotation = (init_position) % 16

  def rotate(self):
    # Increment the position by 1, and roll back over to 0 once last position is reached
    # Simulates a radially arranged set of 16 slots
    self.rotation = (self.rotation + 1) % 16

  def reset_rotation(self):
    # Resets the rotation to the neutral position
    # (i.e. photo slot 1 aligned with camera slot 1, photo 3 with camera 2, etc.)
    self.rotation = 0

  def get_camera_pairs(self, camera_positions: dict[int, int]):
    # Cameras are radially arranged around the device in fixed position
    # This means every other photo slot will 'pair' with a camera
    # The pairing depends on the current position of the carousel
    aligned_pairs: list[tuple[int, int]] = []
    for camera_id, position in camera_positions.items():
      aligned_slot = (position - self.rotation) % 16
      aligned_pairs.append((aligned_slot, camera_id))

    return aligned_pairs


class Camera:
  # Class representing a camera within the system
  def __init__(self, id: int):
    self.id = id
    self.status = "IDLE"
    self.lock = threading.Lock()

  def analyze(self, task: AnalysisTask):
    # Starts the analysis task if its not already complete
    with self.lock:
      # Do nothing if task is already in progress or completed
      if task.status != "NOT COMPLETE":
          return
      
      print(f'Starting analysis for Photo {task.photo_slot} - Camera {task.camera_id}')
      
      self.status = "BUSY"
      task.start_analysis()
      task.time_remaining = 60

      while task.time_remaining > 0:
        time.sleep(1)
        task.time_remaining -= 1

      self.status = "IDLE"
      task.complete_analysis()

      print(f'Finished analysis for Photo {task.photo_slot} - Camera {task.camera_id}')

  def get_state(self):
    # Returns a simple JSON representation of current state
    return {
      "status": self.status,
    }