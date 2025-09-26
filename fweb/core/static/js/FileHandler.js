// File Drop Zone Functionality
function setupFileDropZone(dropZoneId, inputId, multiple = true) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(inputId);

  if (multiple) {
    fileInput.multiple = true;
  }

  dropZone.addEventListener("click", () => fileInput.click());

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
    updateFileList(dropZoneId, fileInput.files);
  });

  fileInput.addEventListener("change", () => {
    updateFileList(dropZoneId, fileInput.files);
  });
}

function updateFileList(dropZoneId, files) {
  const dropZone = document.getElementById(dropZoneId);
  const fileList = dropZone.querySelector(".file-list");
  const placeholder = dropZone.querySelector(".drop-placeholder");

  if (files.length > 0) {
    if (placeholder) placeholder.classList.add("hidden");
    fileList.innerHTML = "";

    Array.from(files).forEach((file, index) => {
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
              <button type="button" onclick="removeFile('${dropZoneId}', ${index})" class="text-red-500 hover:text-red-700">
              <i class="fas fa-times"></i>
              </button>
              </div>
              `;
      fileList.appendChild(fileItem);
    });
  } else {
    if (placeholder) placeholder.classList.remove("hidden");
    fileList.innerHTML = "";
  }
}

function removeFile(dropZoneId, index) {
  const fileInput = document.querySelector(
    `#${dropZoneId.replace("-drop-zone", "-file-input")}`,
  );
  const dt = new DataTransfer();

  Array.from(fileInput.files).forEach((file, i) => {
    if (i !== index) dt.items.add(file);
  });

  fileInput.files = dt.files;
  updateFileList(dropZoneId, fileInput.files);
}

// Tool Navigation
function showTool(toolId, category) {
  // Hide all tool interfaces
  document.querySelectorAll(".tool-interface").forEach((interface) => {
    interface.classList.add("hidden");
  });

  // Show selected tool
  const selectedTool = document.getElementById(`tool-${toolId}`);
  if (selectedTool) {
    selectedTool.classList.remove("hidden");
  }

  // Update active nav item
  document.querySelectorAll(".tool-nav").forEach((nav) => {
    nav.classList.remove("tool-active");
  });
  document.querySelector(`.tool-${toolId}`).classList.add("tool-active");

  // Update URL without reload
  history.pushState(null, "", `?tool=${toolId}`);

  // Initialize tool-specific functionality
  initializeTool(toolId);
}

function initializeTool(toolId) {
  // Tool-specific initialization
  const setupFunctions = {
    convert_doc: () =>
      setupFileDropZone("doc-drop-zone", "doc-file-input", true),
    convert_audio: () =>
      setupFileDropZone("audio-drop-zone", "audio-file-input", true),
    convert_video: () =>
      setupFileDropZone("video-drop-zone", "video-file-input", false),
    convert_image: () =>
      setupFileDropZone("image-drop-zone", "image-file-input", true),
    ocr: () => setupFileDropZone("ocr-drop-zone", "ocr-file-input", true),
    // Add more tool initializations
  };

  if (setupFunctions[toolId]) {
    setupFunctions[toolId]();
  }
}

// Load tool from URL parameter
document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const toolParam = urlParams.get("tool");
  if (toolParam) {
    showTool(toolParam, "{{ category }}");
  }
});
