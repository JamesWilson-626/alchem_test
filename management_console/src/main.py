from fastapi import FastAPI, HTTPException
from typing import List
from .models import LogEntry
from . import database_handler

app = FastAPI()

# API Endpoints
@app.post("/logs/", response_model=LogEntry)
def add_log(entry: LogEntry):
    """Add a new log entry."""
    database_handler.add_log(entry)
    return entry

@app.delete("/logs/{log_id}/")
def delete_log(log_id: int):
    """Delete a log entry by ID."""
    if not database_handler.delete_log(log_id):
        raise HTTPException(status_code=404, detail=f"Log with ID {log_id} not found.")
    return {"detail": f"Log with ID {log_id} deleted successfully."}

@app.put("/logs/{log_id}/", response_model=LogEntry)
def update_log(log_id: int, updated_entry: LogEntry):
    """Update an existing log entry."""
    if not database_handler.update_log(log_id, updated_entry):
        raise HTTPException(status_code=404, detail=f"Log with ID {log_id} not found.")
    return updated_entry

@app.get("/logs/{log_id}/", response_model=LogEntry)
def get_log(log_id: int):
    """Retrieve a log entry by ID."""
    log_entry = database_handler.get_log(log_id)
    if not log_entry:
        raise HTTPException(status_code=404, detail=f"Log with ID {log_id} not found.")
    return log_entry

@app.get("/logs/", response_model=List[LogEntry])
def get_all_logs():
    """Retrieve all log entries."""
    return database_handler.get_all_logs()

# Initialize the database when the app starts
@app.on_event("startup")
def on_startup():
    database_handler.initialize_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "management_console.src.main:app", 
        host="127.0.0.1",
        port=8000,
        reload=True
    )