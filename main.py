from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
import engine
from PIL import Image
from io import BytesIO


# Cap max in-memory upload size to protect free tier RAM (e.g., 10 MB)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 12_000_000  # Pillow safety cap, ~12MP
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    try:
        # Test if the model is working
        import engine
        return {"status": "healthy", "service": "background-remover", "model": "loaded"}
    except Exception as e:
        print(f"Health check failed: {e}")
        return {"status": "unhealthy", "service": "background-remover", "error": str(e)}

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml")

@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt", media_type="text/plain")

@app.post("/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Only image files are allowed."
        )

    # Read with a hard cap
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large: {len(content)} bytes. Maximum allowed: {MAX_UPLOAD_BYTES} bytes"
        )

    try:
        input_image = Image.open(BytesIO(content))
        
        # Validate image format
        if input_image.format not in ['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP']:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported image format: {input_image.format}. Supported formats: JPEG, PNG, BMP, TIFF, WEBP"
            )
        
        # Downscale very large images to reduce memory/latency (longest side 2000px)
        max_side = 2000
        if max(input_image.size) > max_side:
            ratio = max_side / max(input_image.size)
            new_size = (int(input_image.size[0] * ratio), int(input_image.size[1] * ratio))
            input_image = input_image.resize(new_size, Image.LANCZOS)

        output_image = engine.remove_bg(input_image)

        buf = BytesIO()
        output_image.save(buf, format='PNG')
        buf.seek(0)

        return Response(content=buf.getvalue(), media_type='image/png', headers={
            'Content-Disposition': 'attachment; filename="_rmbg.png"'
        })
    except Exception as exc:
        # Log the error for debugging
        print(f"Error processing image: {exc}")
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to process image: {str(exc)}"
        )

