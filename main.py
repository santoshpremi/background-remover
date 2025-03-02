from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import engine
from PIL import Image
from io import BytesIO
import tempfile


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/styles.css")
async def styles():
    return FileResponse("static/styles.css")

@app.get("/script.js")
async def script():
    return FileResponse("static/script.js")

@app.post("/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file:
        return 'No file uploaded', 400

    input_image = Image.open(BytesIO(await file.read()))
    output_image = engine.remove_bg(input_image)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        output_image.save(temp_file, 'PNG')
        temp_file_path = temp_file.name
    
    return FileResponse(temp_file_path, media_type='image/png', filename='_rmbg.png')

