# Radial Camera Carousel API Repository

## Project Overview
This repository is the backend component of the Radial Camera Carousel proof-of-concept.

This application models a rotaing carousel containing slots for up to 16 photos. A set of 8 cameras are radially arranged around the camera such that each camera is aligned with a photo slot at any given time. Each camera analyzes a specific color from the photograph. As the carousel rotates, the cameras will align with different photographs. This design ensures that a full rotation of the carousel will ensure every photo 'visits' each camera.

Users can submit a request containing the desired photo slots to be analyzed, and the desired camera(s) to analyze each photo. A camera measurement takes one minute to complete, and cameras can operate in parallel. As the carousel rotates to each position during its traveral of the camera, the system determines if any photo slots are aligned with a targeted camera for that photo. Any requested photo-camera analyses at the current rotation are then performed in parallel.

## Libraries Used
- Django
- Django Rest Framework (DRF)
- Django CORS Headers

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/Robert-Tyssen/Radial-Camera-Carousel-API.git
cd Radial-Camera-Carousel-API
```

2. **Create a virtual environment (optional but recommended)**
```bash
py -m venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

This app does not currently require any .ENV setup.

5. **(Optional) Add CORS Allowed Origins**

This app has a the following CORS Allowed origins:
```json
CORS_ALLOWED_ORIGINS = [
  "http://localhost:5173",
  "http://127.0.0.1:5173",
]
```
If testing from a front-end running on a different address (e.g. cloud-deployment, etc.), add the address to `CORS_ALLOWED_ORIGINS`, located in `camera_api\settings.py`.

7. **Apply migrations**
```bash
py manage.py migrate
```

6. **Run the development server**
   ```bash
   py manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000/`.
   
   ** After starting the application, take note of the IP address and port on which it is running. This will be needed when using the front-end application.

## Usage

Once the server is running, the app can be accessed by various endpoints. The endpoints are listed below:

### GET /api/heartbeat-check
This method simply returns a known message. The front-end can use this api to validate that it has connected to the correct server. The response is as follows:
```json
{
  "message": "Connection successful!"
}
```

### GET /api/analysis-state
This method will return a JSON structure indicating the current state of the system, including the states of each camera, and the states of any photo-camera analysis tasks. Here is an example response:
```json
{
  "analysis_in_progress": true
  "camera_states": {
    "0": { "status": "IDLE" },
    "1": { "status": "BUSY" },
    "2": { "status": "IDLE" },
    ...
  }
  "analysis_tasks": [
    {
      "photo_id": 1,
      "camera_id": 1,
      "status": "COMPLETE",
      "time_remaining": 0
    },
    {
      "photo_id": 2,
      "camera_id": 4,
      "status": "NOT COMPLETE",
      "time_remaining": 0
    },
    {
      "photo_id": 14,
      "camera_id": 7,
      "status": "IN PROGRESS",
      "time_remaining": 58
    }
  ]
}
```

The `analysis_in_progress` item returns a boolean indicating whether or not analysis is currently ongoing. `analysis_tasks` is a list of the tasks submitted in the most recent analysis. For each task, there is a `photo_id` indicating the id of the photo slot slot, and a `camera_id` indicating the camera. `status` will have a value of COMPLETE, NOT COMPLETE or IN PROGRESS. `time_remaining` returns the amount of time left for any IN PROGRESS task.

Camera ids correspond to the following colors:
```
{
  0: Red,
  1: Orange,
  2: Yellow,
  3: Green,
  4: Blue,
  5: Indigo,
  6: Violet,
  7: Ultraviolet,
}
```

### POST /api/submit-analysis
This method allows a user to submit a set of photo / camera combinations. The `POST` should use `Content-Type: application/json` and supply a payload in a format similar to the following:
```json
{
  "0": [0, 3],
  "6": [0, 1, 2],
}
```
The above corresponds to desired cameras 0 (Red) and 3 (Green) for the first photo slot (`photo_id = 0`), and cameras 0 (Red), 1 (Orange) and 2 (Yellow) for the seventh photo slot (`photo_id = 6`).

The method will fail with the following message and HTTP status code 403 if the endpoint is called while a measurement is already ongoing. Once the measurement is complete (verify using `/api/analysis-state`), a new submission can be performed.
```json
{"error": "analysis-in-progress"}
```

### POST /api/demo-analysis
This method performs a sample measurement with pre-defined photo / camera pairs. The method will return the same 403 response as `/api/submit-analysis` if a measurement is active when the request is submitted.
