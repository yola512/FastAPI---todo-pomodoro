from datetime import datetime


# simulating tasks' database
tasks = [
    {
        "id": 1,
        "title": "Nauka FastAPI",
        "description": "Przygotować przykładowe API z dokumentacją",
        "status": "IN_PROGRESS"
    }
]

# simulating pomodoro timers' database
pomodoro_sessions = [
    {
        "task_id": 1,
        "start_time": datetime(2025, 1, 14, 16, 29, 30),
        'end_time': datetime(2025, 1, 14, 18, 29, 30),
        "completed": True
    }
]

# unique id for each task
def generate_id(data):
    return max((item["id"] for item in data), default=0) + 1