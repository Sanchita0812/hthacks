from re import template
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory = "templates")

soils = {"Sandy":1, "Loamy":2, "Black":3, "Red":4, "Clayey":5}
crops = {"Maize": 6, "Sugarcane": 7, "Cotton": 8, "Tobacco": 9, "Paddy": 10, "Barley": 11, "Wheat": 12, "Millets": 13, "Oil Seeds": 14, "Pulses": 15, "Ground Nuts": 16}


@app.get('/', response_class=FileResponse)
def home():
    return FileResponse("templates/index.html")


@app.get('/crop', response_class=HTMLResponse)
def calculate_crops(request: Request, crop: str = ""):
    return templates.TemplateResponse("crop.html", {"request": request, "crop_val": crop})

@app.post('/crop', response_class=RedirectResponse, status_code=302)
def calculate_crops_(nitrogen: int = Form(), potassium: int = Form(), phosphorous: int = Form(), humidity: int = Form(), rainfall: int = Form(), ph: int = Form(), temp: int = Form()):
    print(nitrogen, potassium, phosphorous, humidity, rainfall, ph, temp)
    return "/crop?crop=" + ml([[nitrogen, potassium, phosphorous, humidity, rainfall, ph, temp]])[0]

@app.get("/shop", response_class=HTMLResponse)
def shop(request: Request, crop: str = ""):
    return templates.TemplateResponse("shop.html", {"request": request, "crop_type": crop})

@app.get("/about", response_class=FileResponse)
def about():
    return FileResponse("templates/about.html")

@app.get("/fertilizer", response_class=HTMLResponse)
def predict_fert(request: Request, fert: str = ""):
    return templates.TemplateResponse("fertilizer.html", {"request": request, "fert_val": fert})

@app.post('/fertilizer', response_class=RedirectResponse, status_code=302)
def calculate_crops_(nitrogen: int = Form(), potassium: int = Form(), phosphorous: int = Form(), humidity: int = Form(), moisture: int = Form(), soil: str = Form(), crop: str = Form(), temp: int = Form()):
    try:
        soil_ = soils[soil]
        crop_ = crops[crop]
    except:
        return "/fertilizer"
    return "/fertilizer?fert=" + fert_ml([[nitrogen, potassium, phosphorous, humidity, moisture, soil_, crop_, temp]])[0]

def fert_ml(data):
    fert_read = open("model2.pkl", "rb")
    ferts_cv = joblib.load(fert_read)
    result = ferts_cv.predict(data)
    return result

def ml(data):
    crops_read = open("model.pkl", "rb")
    crops_cv = joblib.load(crops_read)
    result = crops_cv.predict(data)
    return result