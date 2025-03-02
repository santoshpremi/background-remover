# Background Remover
This project is a web-based background remover tool that uses AI to automatically remove backgrounds from images. <br/>It is built using Python and FastAPI.


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
1. Clone the Repository:  <br/> 
   `git clone https://github.com/santoshpremi/background-remover.git `  <br/> 
    `cd background-remover`
2. Create a Virtual Environment: <br/>
`python -m venv venv`<br/>
`source venv/bin/activate`
3. Install Dependencies: <br/>
`pip install -r requirements.txt`
4. Run the Application: <br/>
`uvicorn main:app --host 0.0.0.0 --port 8000` <br/>
Navigate to http://localhost:8000 to access the app.

### Docker image locally, follow these steps:
1. Pull the Docker Image  <br/> 
`docker pull santoshpremi/bg-remover:latest`  <br/> 
This command downloads the latest version of the image from Docker Hub.
2. Run the Docker Image  <br/> 
`docker run -d -p 80:80 santoshpremi/bg-remover:latest`  <br/> 
-d: Runs the container in detached mode (background).  <br/> 
-p 80:80: Maps port 80 on your host to port 80 in the container.
3. Verify the Container is Running  <br/> 
`docker ps`  <br/> 
This lists all running containers. You should see the background remover container in the list. <br/>
Navigate to http://localhost:8000 to access the app.


## Usage
1. Upload an Image: Click the "Choose File" button or drag an image into the drop zone. <br/>
2. Remove Background: Click the "Download" button to process the image and downloaded.
## Contributing:
1. Fork the Repository:  <br/>
 Fork the project on GitHub.
2. Clone the Forked Repository: <br/>
   `git clone https://github.com/santoshpremi/background-remover.git `  <br/> 
    `cd background-remover`
3. Create a New Branch:  <br/> 
`git checkout -b your-feature-branch`

5. Make Changes:  <br/> 
Implement your feature or fix.

6. Commit Changes: <br/> 
`git commit -m "Your commit message"`
6. Push Changes:  <br/> 
`git push origin your-feature-branch`



