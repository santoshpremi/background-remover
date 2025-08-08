const elements = {
  fileInput: document.getElementById('fileInput'),
  uploadForm: document.getElementById('uploadForm'),
  previewImage: document.getElementById('previewImage'),
  resultImage: document.getElementById('resultImage'),
  processBtn: document.getElementById('processBtn'),
  downloadBtn: document.getElementById('downloadBtn'),
  formatSelect: document.getElementById('formatSelect'),
  bgColor: document.getElementById('bgColor'),
  fileName: document.getElementById('fileName'),
  progressFill: document.querySelector('.progress-fill'),
  progressContainer: document.getElementById('progressContainer'),
  messageBox: document.getElementById('messageBox'),
  messageTitle: document.getElementById('messageTitle'),
  messageText: document.getElementById('messageText'),
  closeMessage: document.getElementById('closeMessage'),
  dropZone: document.getElementById('dropZone'),
  workCanvas: document.getElementById('workCanvas'),
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
      // Reset result preview state
      elements.resultImage.src = '';
      originalResultBlob = null;
      document.getElementById('resultPlaceholder').style.display = 'block';
      elements.downloadBtn.disabled = true;
      
      // Automatically process the image
      processImage(file);
    };
    reader.readAsDataURL(file);
  }
});

// Process Image Function
async function processImage(file) {
  if (!file) {
      showMessage('No File Selected', 'Please choose an image first!', 'error');
      return;
  }

  elements.progressContainer.style.display = 'block';
  const stop = simulateProgress();

  const formData = new FormData();
  formData.append('file', file);

  try {
      const response = await fetch('/', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Server error');
      const blob = await response.blob();
      originalResultBlob = blob; // Store the original blob
      const url = URL.createObjectURL(blob);
      elements.resultImage.src = url;
      elements.resultImage.style.display = 'block';
      document.getElementById('resultPlaceholder').style.display = 'none';
      elements.downloadBtn.disabled = false;
      
      // Apply initial background color preview
      setTimeout(() => updateResultPreview(), 100);
  } catch (error) {
      showMessage('Error', 'Failed to upload image!', 'error');
  } finally {
      elements.progressContainer.style.display = 'none';
      stop();
  }
}


// New infinite progress animation
function simulateProgress() {
  let progress = 0;
  const interval = setInterval(() => {
    progress += 2;
    if (progress >= 100) progress = 10;
    elements.progressFill.style.width = `${progress}%`;
  }, 50);
  return () => clearInterval(interval);
}

// Drag & Drop Handling
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => e.preventDefault());

const dropZone = elements.dropZone;
dropZone.addEventListener('dragover', () => dropZone.classList.add('dragover'));
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files.length) {
    const file = e.dataTransfer.files[0];
    elements.fileInput.files = e.dataTransfer.files;
    elements.fileName.textContent = file.name;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      elements.previewImage.src = e.target.result;
      elements.previewImage.style.display = 'block';
      document.querySelector('.placeholder').style.display = 'none';
      // Reset result preview state
      elements.resultImage.src = '';
      originalResultBlob = null;
      document.getElementById('resultPlaceholder').style.display = 'block';
      elements.downloadBtn.disabled = true;
      
      // Automatically process the image
      processImage(file);
    };
    reader.readAsDataURL(file);
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

// Download handling with background color/format
elements.formatSelect.addEventListener('change', () => {
  // Keep background color option for both PNG and JPEG
  document.getElementById('bgColorLabel').style.display = 'inline-flex';
});
elements.formatSelect.dispatchEvent(new Event('change'));

// Background color preview
elements.bgColor.addEventListener('input', updateResultPreview);
elements.bgColor.addEventListener('change', updateResultPreview);

let originalResultBlob = null;

function updateResultPreview() {
  if (!originalResultBlob) return;
  
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    const canvas = elements.workCanvas;
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = elements.bgColor.value;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    
    // Update result image with background color
    const dataURL = canvas.toDataURL('image/png');
    elements.resultImage.src = dataURL;
  };
  img.src = URL.createObjectURL(originalResultBlob);
}

elements.downloadBtn.addEventListener('click', () => {
  if (!originalResultBlob) return;
  const format = elements.formatSelect.value;
  
  // Always composite with background color for both PNG and JPEG
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    const canvas = elements.workCanvas;
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = elements.bgColor.value;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      const filename = format === 'png' ? 'bg_remove.png' : 'bg_remove.jpg';
      triggerDownload(url, filename);
      URL.revokeObjectURL(url);
    }, format === 'png' ? 'image/png' : 'image/jpeg', 0.92);
  };
  img.src = URL.createObjectURL(originalResultBlob);
});

function triggerDownload(url, filename) {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}