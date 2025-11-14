// File Drop Zone Functionality
function setupFileDropZone(dropZoneId, inputId) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(inputId);

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
    fileInput.files = e.dataTransfer.files;
    updateFileList(dropZoneId, fileInput.files);
  });

  fileInput.addEventListener("change", () => {
    updateFileList(dropZoneId, fileInput.files);
  });
}

function updateFileList(dropZoneId, files) {
  const dropZone = document.getElementById(dropZoneId);
  const fileList = dropZone.querySelector(".file-list");
  fileList.innerHTML = "";

  if (files.length > 0) {
    Array.from(files).forEach((file) => {
      const fileItem = document.createElement("div");
      fileItem.className =
        "flex items-center justify-between p-2 bg-gray-50 rounded";
      fileItem.innerHTML = `
                        <div class="flex items-center">
                            <i class="fas fa-file text-gray-400 mr-2"></i>
                            <span class="text-sm truncate">${file.name}</span>
                        </div>
                        <span class="text-xs text-gray-500">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
                    `;
      fileList.appendChild(fileItem);
    });
  }
}
