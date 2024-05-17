from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
from io import BytesIO
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
    
    # Initialize a temporary file for saving the downloaded image
    temp_file_path = 'temp.png'

    # Stream the download of the image file and save it to the temporary file
    with open(temp_file_path, 'wb') as f:
        while content := await file.read(1024):  # Stream the content in chunks
            f.write(content)

    # Open the downloaded image using PIL
    input_image = Image.open(temp_file_path)

    # Process the image using rembg
    output_image = remove(input_image, post_process_mask=True)

    # Save the processed image to a temporary file
    output_temp_file_path = 'temp_output.png'
    output_image.save(output_temp_file_path, 'PNG')

    # Close and remove the temporary file for the input image
    os.remove(temp_file_path)

    # Return the processed image as a FileResponse
    return FileResponse(output_temp_file_path, media_type='image/png', filename='_rmbg.png')
