class AnalysisTask:
  # Represents the analyis process for a single photo and camera pair
  def __init__(self, photo_slot, camera_id):
    self.photo_slot = photo_slot
    self.camera_id = camera_id
    self.status = "NOT COMPLETE"
    self.time_remaining = 0

  # Start the analysis by updating status to IN PROGRESS
  def start_analysis(self):
    self.status = "IN PROGRESS"

  # Complete the analysis by updating status to COMPLETE
  def complete_analysis(self):
    self.status = "COMPLETE"

  # Returns a JSON representation of current state
  def get_state(self):
    return {
      "photo_id": self.photo_slot,
      "camera_id": self.camera_id,
      "status": self.status,
      "time_remaining": self.time_remaining,
    }