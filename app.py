from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
import json
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FEEDBACK_FILE = "feedback.json"

app.mount("/fastapi_ke_andar", StaticFiles(directory="./static"),name="static")
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("feedbackform.html",{"request":request})

@app.post("/submit", response_class=HTMLResponse)
async def  submit_form(request:Request, name:str = Form(...),email: str = Form(...), feedback: str= Form(...)):
    feedback_data = []
    if Path(FEEDBACK_FILE).exists():
        with open(FEEDBACK_FILE, "r") as file:
            feedback_data = json.load(file)
            
    feedback_data.append({"name":name, "email":email, "feedback":feedback})
    
    with open(FEEDBACK_FILE, "w") as file:
        json.dump(feedback_data, file, indent=4)
        
    return templates.TemplateResponse("thankyou.html",{"request":request, "name":name})
    
