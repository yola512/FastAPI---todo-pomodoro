from fastapi import FastAPI
from app.routes import router

app = FastAPI( 
    title="TODO with Pomodoro", 
    description="Manage tasks using Pomodoro timers",
    version="0.0.1"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello world!"}