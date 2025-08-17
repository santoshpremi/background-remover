# Background Remover

This project is a web-based background remover tool that uses AI to automatically remove backgrounds from images. It is built using Python and FastAPI.

<p align="center">
  <img width="400" height="400" src="bg-remover.png">
</p>

## U2NET Small Model

Description: U2NET small is a lightweight version of the U2NET model, optimized for real-time background removal.

### Features:

Lightweight: Smaller model size (4.7 MB) for faster loading. <br/>
Fast Inference: Designed for real-time performance. <br/>
High Accuracy: Maintains high accuracy despite its small size.

## Requirements

Python 3.12+ <br/>
Docker

## Getting Started

### Local Development

1. Clone the Repository: <br/>
   `git clone https://github.com/santoshpremi/background-remover.git ` <br/>
   `cd background-remover`
2. Create a Virtual Environment: <br/>
   `python -m venv venv`<br/>
   `source venv/bin/activate`
3. Install Dependencies: <br/>
   `pip install -r requirements.txt`
4. Run the Application: <br/>
   `uvicorn main:app --host 0.0.0.0 --port 8000` <br/>
   Navigate to http://localhost:8000 to access the app.

### Docker Image (Local & Multi-Arch)

1. **Pull the Docker Image** <br/>
   `docker pull santoshpremi/bg-remover-01:latest` <br/>
   Downloads the latest multi-architecture image from Docker Hub.

2. **Run the Docker Container** <br/>
   `docker run -d -p 8000:80 santoshpremi/bg-remover-01:latest` <br/>

   - `-d`: Runs container in detached mode (background) <br/>
   - `-p 8000:80`: Maps host port 8000 to container port 80

3. **Verify Container Status** <br/>
   `docker ps` <br/>
   Lists running containers. You should see the background remover container.

4. **Access the Application** <br/>
   Navigate to http://localhost:8000

**Multi-Architecture Support:** The Docker image supports both AMD64 and ARM64 architectures, making it compatible with Intel/AMD processors and Apple Silicon (M1/M2) Macs.

## Usage

1. Upload an Image: Click the "Choose File" button or drag an image into the drop zone. <br/>
2. Remove Background: Click the "Download" button to process the image and downloaded.

## Contributing:

1. Fork the Repository: <br/>
   Fork the project on GitHub.
2. Clone the Forked Repository: <br/>
   `git clone https://github.com/santoshpremi/background-remover.git ` <br/>
   `cd background-remover`
3. Create a New Branch: <br/>
   `git checkout -b your-feature-branch`

4. Make Changes: <br/>
   Implement your feature or fix.

5. Commit Changes: <br/>
   `git commit -m "Your commit message"`
6. Push Changes: <br/>
   `git push origin your-feature-branch`
