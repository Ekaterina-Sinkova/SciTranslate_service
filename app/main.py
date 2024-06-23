import json

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.run_nllb import NLLBModel
import tempfile
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Initializing model...")
model = NLLBModel()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/translate/")
async def translate(request: Request):
    data = await request.form()
    text = data["text"]
    translated_text = model.translate(text)
    return JSONResponse({"translation": translated_text})

@app.post("/translate_article/")
async def translate_article(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    contents = await file.read()
    text = contents.decode("utf-8")
    logger.info("Translating text...")
    translated_text = model.translate_article(text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
        translated_text.to_excel(temp.name, index=False)
        temp_path = temp.name

        return FileResponse(temp_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            filename="translated.xlsx")