let dropZone = document.getElementById("dropZone");
let fileInput = document.getElementById("fileInput");
let uploadForm = document.getElementById("uploadForm");
let removeBackgroundBtn = document.getElementById("removeBackgroundBtn");
let popup = document.getElementById("popup");
let fileNameSpan = document.getElementById("fileName");

function showPopup(event) {
    event.preventDefault();
    popup.style.display = "block";
}

function closePopup() {
    popup.style.display = "none";
}

function displayFileName(input) {
    if (input.files.length > 0) {
        fileName = input.files[0].name ;
        styleName = fileName.slice(0,7) + '...' + fileName.slice(-7);
        fileNameSpan.textContent = styleName; // Display the file name in the label
    } else {
        fileNameSpan.textContent = ""; // Reset label if no file is selected
    }
}


fileInput.addEventListener('change', function() {
    displayFileName(this);
});

removeBackgroundBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default form submission
    if (fileInput.files.length > 0) {
        uploadForm.submit(); // Submit the form manually
    } else {
        showPopup(event);
    }
});

dropZone.addEventListener("dragover", function (e) {
    e.preventDefault(); // Prevent the default behavior
    e.stopPropagation();
    this.classList.add("dragover");
});

dropZone.addEventListener("dragleave", function (e) {
    this.classList.remove("dragover");
});

dropZone.addEventListener("drop", function (e) {
    e.preventDefault(); // Prevent the default behavior
    e.stopPropagation();
    this.classList.remove("dragover");

    let dt = new DataTransfer(); // Create a new DataTransfer object
    let files = e.dataTransfer.files;

    for (let i = 0; i < files.length; i++) {
        dt.items.add(files[i]); // Add files to the DataTransfer object
    }

    fileInput.files = dt.files; // Assign the files to the file input
    displayFileName(fileInput);
});
