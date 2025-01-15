from datetime import datetime


# simulating tasks' database
tasks = []

# simulating pomodoro timers' database
pomodoro_sessions = []

# unique id for each task
def generate_id(data):
    return max((item["id"] for item in data), default=0) + 1