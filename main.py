from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
from io import BytesIO
import tempfile
import uvicorn
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def index():
    return FileResponse("static/html/index.html")

@app.get("/styles.css")
async def styles():
    return FileResponse("static/css/styles.css")

@app.get("/script.js")
async def script():
    return FileResponse("static/js/script.js")

@app.post("/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file:
        return 'No file uploaded', 400

    input_image = Image.open(BytesIO(await file.read()))
    output_image = remove(input_image, post_process_mask=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        output_image.save(temp_file, 'PNG')
        temp_file_path = temp_file.name
    
    return FileResponse(temp_file_path, media_type='image/png', filename='_rmbg.png')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))