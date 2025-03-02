const elements = {
  fileInput: document.getElementById('fileInput'),
  uploadForm: document.getElementById('uploadForm'),
  previewImage: document.getElementById('previewImage'),
  processBtn: document.getElementById('processBtn'),
  fileName: document.getElementById('fileName'),
  progressFill: document.querySelector('.progress-fill'),
  progressContainer: document.querySelector('.progress-container'),
  messageBox: document.getElementById('messageBox'),
  messageTitle: document.getElementById('messageTitle'),
  messageText: document.getElementById('messageText'),
  closeMessage: document.getElementById('closeMessage')
};

// File Input Handling
elements.fileInput.addEventListener('change', function() {
  if (this.files.length > 0) {
    const file = this.files[0];
    elements.fileName.textContent = file.name;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      elements.previewImage.src = e.target.result;
      elements.previewImage.style.display = 'block';
      document.querySelector('.placeholder').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }
});

// Process Button Click
elements.processBtn.addEventListener('click', async () => {
  if (!elements.fileInput.files.length) {
      showMessage('No File Selected', 'Please choose an image first!', 'error');
      return;
  }

  elements.progressContainer.style.display = 'block';
  simulateProgress(); // Fake progress bar for show-off

  const formData = new FormData();
  formData.append('file', elements.fileInput.files[0]);

  try {
      await fetch('/', {
          method: 'POST',
          body: formData
      }).then(response => response.blob())  // Convert response to Blob
      .then(blob => {
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "processed.png";
          document.body.appendChild(a);
          a.click();
          URL.revokeObjectURL(url);
      }).catch(error => console.error("Upload error:", error));
  } catch (error) {
      showMessage('Error', 'Failed to upload image!', 'error');
  } finally {
      elements.progressContainer.style.display = 'none';
  }
});


// New infinite progress animation
function simulateProgress() {
  let progress = 0;
  const interval = setInterval(() => {
    progress += 2;
    if (progress >= 100) {
      progress = 0;
    }
    elements.progressFill.style.width = `${progress}%`;
  }, 50);
}

// Drag & Drop Handling
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => e.preventDefault());

const dropZone = document.querySelector('.preview-container');
dropZone.addEventListener('dragover', () => dropZone.classList.add('dragover'));
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files.length) {
    elements.fileInput.files = e.dataTransfer.files;
    elements.fileInput.dispatchEvent(new Event('change'));
  }
});

// Message Box Handling
elements.closeMessage.addEventListener('click', () => {
  elements.messageBox.style.display = 'none';
});

window.addEventListener('click', (e) => {
  if (e.target === elements.messageBox) {
    elements.messageBox.style.display = 'none';
  }
});

function showMessage(title, text, type) {
  elements.messageTitle.textContent = title;
  elements.messageText.textContent = text;
  elements.messageBox.style.display = 'flex';
}