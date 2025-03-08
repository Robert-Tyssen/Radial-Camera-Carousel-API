class AnalysisTask:
  # Represents the analyis process for a single photo and camera pair
  def __init__(self, photo_slot, camera_id):
    self.photo_slot = photo_slot
    self.camera_id = camera_id
    self.status = "NOT COMPLETE"
    self.time_remaining = 0

  def start_analysis(self):
    self.status = "IN PROGRESS"

  def complete_analysis(self):
    self.status = "COMPLETE"

  def get_state(self):
    # Returns a JSON representation of current state
    return {
      "photo_id": self.photo_slot,
      "camera_id": self.camera_id,
      "status": self.status,
      "time_remaining": self.time_remaining,
    }