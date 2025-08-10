# main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from api.handler import handle_complaint

app = FastAPI()

# Define request schema
class Complaint(BaseModel):
    user_id: str
    message: str

@app.post("/complaint")
def receive_complaint(complaint: Complaint):
    result = handle_complaint(complaint.user_id, complaint.message)
    return result
