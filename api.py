from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory = "templates")


@app.get('/', response_class=FileResponse)
def home():
    return FileResponse("templates/index.html")


@app.get('/crop', response_class=HTMLResponse)
def calculate_crops(request: Request, crop: str = ""):
    return templates.TemplateResponse("crop.html", {"request": request, "crop_val": crop})

@app.post('/crop', response_class=RedirectResponse, status_code=302)
def calculate_crops(nitrogen: int = Form(), potassium: int = Form(), phosphorous: int = Form(), humidity: int = Form(), rainfall: int = Form(), ph: int = Form(), temp: int = Form()):
    print(nitrogen, potassium, phosphorous, humidity, rainfall, ph, temp)
    return "/crop?crop=" + ml([[nitrogen, potassium, phosphorous, humidity, rainfall, ph, temp]])[0]

@app.get("/shop", response_class=HTMLResponse)
def shop(request: Request, crop: str = ""):
    return templates.TemplateResponse("shop.html", {"request": request, "crop_type": crop})


def ml(data):
    crops_read = open("model.pkl", "rb")
    crops_cv = joblib.load(crops_read)
    result = crops_cv.predict(data)
    return result