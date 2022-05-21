from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/', response_class=FileResponse)
def home():
    return FileResponse("templates/index.html")
