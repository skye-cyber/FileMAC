class FileHandler {
  constructor() {
    this.setupGlobalFileHandlers();
  }

  setupFileDropZone(dropZoneId, inputId, multiple = true) {
    const dropZone = document.getElementById(dropZoneId);
    const fileInput = document.getElementById(inputId);

    if (!dropZone || !fileInput) return;

    fileInput.multiple = multiple;

    // Click to select files
    dropZone.addEventListener("click", () => fileInput.click());

    // Drag and drop handlers
    this.setupDragAndDrop(dropZone, fileInput, multiple);

    // File input change handler
    fileInput.addEventListener("change", () => {
      this.updateFileList(dropZoneId, fileInput.files);
    });
  }

  openFileSelector(dropZoneId) {
    const inputElement = document.getElementById(`${dropZoneId}-input`);
    inputElement?.click();
  }

  setupDragAndDrop(dropZone, fileInput, multiple) {
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");

      if (multiple) {
        fileInput.files = e.dataTransfer.files;
      } else {
        fileInput.files =
          e.dataTransfer.files.length > 0
            ? [e.dataTransfer.files[0]]
            : new DataTransfer().files;
      }
      this.updateFileList(dropZone.id, fileInput.files);
    });
  }

  updateFileList(dropZoneId, files) {
    const dropZone = document.getElementById(dropZoneId);
    const fileList = dropZone.querySelector(".file-list");
    const placeholder = dropZone.querySelector(".drop-placeholder");

    if (files.length > 0) {
      if (placeholder) placeholder.classList.add("hidden");
      fileList.innerHTML = "";

      Array.from(files).forEach((file, index) => {
        const fileItem = this.createFileItem(file, dropZoneId, index);
        fileList.appendChild(fileItem);
      });
    } else {
      if (placeholder) placeholder.classList.remove("hidden");
      fileList.innerHTML = "";
    }
  }

  createFileItem(file, dropZoneId, index) {
    const fileItem = document.createElement("div");
    fileItem.className =
      "flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg mb-2";
    fileItem.innerHTML = `
    <div class="flex items-center flex-1 min-w-0">
    <i class="fas fa-file text-gray-400 mr-3 flex-shrink-0"></i>
    <span class="text-sm font-medium truncate">${file.name}</span>
    </div>
    <div class="flex items-center space-x-3 flex-shrink-0">
    <span class="text-xs text-gray-500 dark:text-gray-400">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
    <button type="button" onclick="fileHandler.removeFile('${dropZoneId}', ${index})"
    class="text-red-500 hover:text-red-700 transition-colors">
    <i class="fas fa-times"></i>
    </button>
    </div>
    `;
    return fileItem;
  }

  removeFile(dropZoneId, index) {
    const fileInput = document.querySelector(
      `#${dropZoneId.replace("-drop-zone", "-file-input")}`,
    );
    const dt = new DataTransfer();

    Array.from(fileInput.files).forEach((file, i) => {
      if (i !== index) dt.items.add(file);
    });

    fileInput.files = dt.files;
    this.updateFileList(dropZoneId, fileInput.files);
  }

  setupGlobalFileHandlers() {
    // Add any global file-related event listeners here
  }

  validateFiles(files, allowedTypes = []) {
    if (files.length === 0) return { valid: false, error: "No files selected" };

    if (allowedTypes.length > 0) {
      for (let file of files) {
        const extension = file.name.split(".").pop().toLowerCase();
        if (!allowedTypes.includes(extension)) {
          return {
            valid: false,
            error: `File type .${extension} is not allowed`,
          };
        }
      }
    }

    return { valid: true };
  }
}

// Initialize global file handler
window.fileHandler = new FileHandler();
