// Additional utility functions for the new tools
function toggleAdvanced(sectionId) {
  const section = document.getElementById(sectionId);
  section.classList.toggle("hidden");

  const icon = section.previousElementSibling.querySelector("i");
  if (section.classList.contains("hidden")) {
    icon.classList.remove("fa-chevron-up");
    icon.classList.add("fa-chevron-down");
  } else {
    icon.classList.remove("fa-chevron-down");
    icon.classList.add("fa-chevron-up");
  }
}

function browseFolder(type) {
  // This would integrate with a file browser component
  alert(
    "Folder browser would open here. In a real implementation, this would use a file dialog.",
  );
}

function scanFolder() {
  // Simulate folder scanning
  document.getElementById("folder-scan-results").classList.remove("hidden");
  document.getElementById("scan-total").textContent = "156";
  document.getElementById("scan-size").textContent = "245.7 MB";
  document.getElementById("scan-types").textContent = "8";

  // Populate file type breakdown
  const breakdown = document.getElementById("file-type-breakdown");
  breakdown.innerHTML = `
        <div class="flex justify-between text-xs">
            <span>PDF Files</span>
            <span>42 files (67.3 MB)</span>
        </div>
        <div class="flex justify-between text-xs">
            <span>Images</span>
            <span>78 files (112.4 MB)</span>
        </div>
        <div class="flex justify-between text-xs">
            <span>Documents</span>
            <span>36 files (66.0 MB)</span>
        </div>
    `;
}

function previewAnalysis() {
  // Simulate analysis preview
  document.getElementById("analysis-results").classList.remove("hidden");
  document.getElementById("info-duration").textContent = "02:45:18";
  document.getElementById("info-size").textContent = "1.2 GB";
  document.getElementById("info-format").textContent = "MP4";
  document.getElementById("video-resolution").textContent = "1920x1080";
  document.getElementById("video-codec").textContent = "H.264";
  document.getElementById("video-bitrate").textContent = "4.5 Mbps";
  document.getElementById("audio-codec").textContent = "AAC";
  document.getElementById("audio-channels").textContent = "2 (Stereo)";
  document.getElementById("audio-sample-rate").textContent = "44.1 kHz";
}

function previewOCR() {
  // Simulate OCR preview
  document.getElementById("ocr-results").classList.remove("hidden");
  document.getElementById("ocr-filename").textContent = "document.pdf";
  document.getElementById("ocr-text-output").textContent =
    "This is a sample of extracted text from the document.\n\n" +
    "The OCR engine has successfully processed the image and extracted\n" +
    "readable text while preserving the original layout and formatting.\n\n" +
    "Multiple languages are supported, and the accuracy can be adjusted\n" +
    "based on the quality of the input document.";
  document.getElementById("confidence-score").textContent = "92%";
  document.getElementById("word-count").textContent = "45";
  document.getElementById("processing-time").textContent = "2.3s";
}

function copyOCRText() {
  const text = document.getElementById("ocr-text-output").textContent;
  navigator.clipboard.writeText(text).then(() => {
    // Show success message
    alert("Text copied to clipboard!");
  });
}

function downloadOCRText() {
  // Simulate download functionality
  alert("Download functionality would be implemented here");
}

function scanBulkFiles() {
  // Simulate bulk file scanning
  const totalFiles = Math.floor(Math.random() * 100) + 50;
  document.getElementById("bulk-total").textContent = totalFiles;
  document.getElementById("bulk-processed").textContent = "0";
  document.getElementById("bulk-success").textContent = "0";
  document.getElementById("bulk-failed").textContent = "0";
  document.getElementById("bulk-progress").classList.remove("hidden");
}

// Handle separator selection change
document.addEventListener("change", function (e) {
  if (e.target.name === "separator") {
    const customDiv = document.getElementById("custom-separator");
    if (e.target.value === "custom") {
      customDiv.classList.remove("hidden");
    } else {
      customDiv.classList.add("hidden");
    }
  }
});

// Initialize tool-specific functionality
function initializeTool(toolId) {
  const setupFunctions = {
    batch_doc_convert: () =>
      setupFileDropZone("batch-doc-drop-zone", "batch-doc-file-input", true),
    folder_operations: () => {
      /* Folder operations setup */
    },
    convert_video: () =>
      setupFileDropZone("video-drop-zone", "video-file-input", true),
    analyze_video: () =>
      setupFileDropZone(
        "analyze-video-drop-zone",
        "analyze-video-file-input",
        false,
      ),
    extract_audio: () =>
      setupFileDropZone(
        "extract-video-drop-zone",
        "extract-video-file-input",
        true,
      ),
    ocr: () => setupFileDropZone("ocr-drop-zone", "ocr-file-input", true),
    bulk_ocr: () =>
      setupFileDropZone("bulk-ocr-drop-zone", "bulk-ocr-file-input", true),
  };

  if (setupFunctions[toolId]) {
    setupFunctions[toolId]();
  }
}

// Tool-specific initialization function
function initializeTool(toolId) {
  // Remove hidden class from all tool interfaces first
  document.querySelectorAll(".tool-interface").forEach((interface) => {
    interface.classList.add("hidden");
  });

  // Show the selected tool
  const toolElement = document.getElementById(`tool-${toolId}`);
  if (toolElement) {
    toolElement.classList.remove("hidden");
  }

  // Tool-specific initialization
  const initializationFunctions = {
    // Document Tools
    convert_doc: () => {
      setupFileDropZone("doc-drop-zone", "doc-file-input", true);
      setupFormatOptions("doc-format-select", [
        "pdf",
        "docx",
        "txt",
        "html",
        "image",
      ]);
      setupAdvancedToggle("doc-advanced");
    },
    pdf_join: () => {
      setupFileDropZone("pdf-join-drop-zone", "pdf-join-file-input", true);
      setupOrderOptions();
    },
    scan_pdf: () => {
      setupFileDropZone("scan-pdf-drop-zone", "scan-pdf-file-input", true);
      setupScanOptions();
    },
    doc_long_image: () => {
      setupFileDropZone(
        "doc-longimg-drop-zone",
        "doc-longimg-file-input",
        true,
      );
      setupLongImageOptions();
    },
    extract_pages: () => {
      setupFileDropZone(
        "extract-pages-drop-zone",
        "extract-pages-file-input",
        false,
      );
      setupPageRangeSelector();
    },
    Atext2word: () => {
      setupFileDropZone("atext2word-drop-zone", "atext2word-file-input", true);
      setupFontOptions();
    },
    doc2image: () => {
      setupFileDropZone("doc2image-drop-zone", "doc2image-file-input", true);
      setupImageFormatOptions();
    },

    // Image Tools
    convert_image: () => {
      setupFileDropZone("image-drop-zone", "image-file-input", true);
      setupFormatOptions("image-format-select", [
        "png",
        "jpg",
        "webp",
        "gif",
        "bmp",
      ]);
      setupQualitySlider();
      setupAdvancedToggle("resize-options");
    },
    resize_image: () => {
      setupFileDropZone(
        "resize-image-drop-zone",
        "resize-image-file-input",
        true,
      );
      setupSizeOptions();
      setupDimensionControls();
    },
    image2pdf: () => {
      setupFileDropZone("image2pdf-drop-zone", "image2pdf-file-input", true);
      setupPDFOptions();
    },
    image2word: () => {
      setupFileDropZone("image2word-drop-zone", "image2word-file-input", true);
      setupWordOptions();
    },
    image2gray: () => {
      setupFileDropZone("image2gray-drop-zone", "image2gray-file-input", true);
      setupGrayscaleOptions();
    },
    ocr: () => {
      setupFileDropZone("ocr-drop-zone", "ocr-file-input", true);
      setupOCROptions();
      setupLanguageSelector();
    },

    // Audio Tools
    convert_audio: () => {
      setupFileDropZone("audio-drop-zone", "audio-file-input", true);
      setupFormatOptions("audio-format-select", [
        "mp3",
        "wav",
        "flac",
        "m4a",
        "aac",
      ]);
      setupAudioQualityOptions();
      setupAdvancedToggle("audio-effects");
    },
    audio_join: () => {
      setupFileDropZone("audio-join-drop-zone", "audio-join-file-input", true);
      setupJoinOrder();
    },
    extract_audio: () => {
      setupFileDropZone(
        "extract-audio-drop-zone",
        "extract-audio-file-input",
        true,
      );
      setupExtractionOptions();
    },
    audio_effect: () => {
      setupFileDropZone(
        "audio-effect-drop-zone",
        "audio-effect-file-input",
        true,
      );
      setupAudioEffects();
    },

    // Video Tools
    convert_video: () => {
      setupFileDropZone("video-drop-zone", "video-file-input", true);
      setupFormatOptions("video-format-select", [
        "mp4",
        "mkv",
        "avi",
        "mov",
        "webm",
      ]);
      setupVideoQualityOptions();
      setupAdvancedToggle("video-codec");
      setupAdvancedToggle("video-resolution");
    },
    analyze_video: () => {
      setupFileDropZone(
        "analyze-video-drop-zone",
        "analyze-video-file-input",
        false,
      );
      setupAnalysisOptions();
    },

    // Batch Tools
    batch_dashboard: () => {
      // Dashboard doesn't need file drop zone
      setupBatchDashboard();
    },
    batch_doc_convert: () => {
      setupFileDropZone(
        "batch-doc-drop-zone",
        "batch-doc-file-input",
        true,
        true,
      );
      setupBatchOptions();
      setupAdvancedToggle("batch-advanced");
    },
    folder_operations: () => {
      setupFolderOperations();
    },
    bulk_ocr: () => {
      setupFileDropZone(
        "bulk-ocr-drop-zone",
        "bulk-ocr-file-input",
        true,
        true,
      );
      setupBulkOCROptions();
    },
  };

  // Execute the initialization function for the current tool
  if (initializationFunctions[toolId]) {
    initializationFunctions[toolId]();
  }

  // Initialize form submission for this tool
  initializeFormSubmission(toolId);
}

// Enhanced file drop zone setup
function setupFileDropZone(
  dropZoneId,
  inputId,
  multiple = true,
  allowFolders = false,
) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(inputId);

  if (!dropZone || !fileInput) return;

  // Set multiple attribute
  fileInput.multiple = multiple;

  // Allow folder selection if specified
  if (allowFolders) {
    fileInput.setAttribute("webkitdirectory", "");
    fileInput.setAttribute("directory", "");
  }

  // Click to select files
  dropZone.addEventListener("click", () => fileInput.click());

  // Drag and drop handlers
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
    dropZone.querySelector(".drop-placeholder").style.opacity = "0.5";
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
    dropZone.querySelector(".drop-placeholder").style.opacity = "1";
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    dropZone.querySelector(".drop-placeholder").style.opacity = "1";

    const files = allowFolders ? e.dataTransfer.items : e.dataTransfer.files;
    handleDroppedFiles(files, fileInput, dropZoneId, allowFolders);
  });

  // File input change handler
  fileInput.addEventListener("change", () => {
    updateFileList(dropZoneId, fileInput.files, allowFolders);
  });
}

function handleDroppedFiles(dataTransfer, fileInput, dropZoneId, allowFolders) {
  if (allowFolders && dataTransfer.items) {
    // Handle folder drop
    processDroppedItems(dataTransfer.items, fileInput, dropZoneId);
  } else {
    // Handle file drop
    fileInput.files = dataTransfer.files;
    updateFileList(dropZoneId, dataTransfer.files, allowFolders);
  }
}

async function processDroppedItems(items, fileInput, dropZoneId) {
  const files = [];

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    if (item.kind === "file") {
      const file = item.getAsFile();
      if (file) files.push(file);
    }
  }

  // Create a new FileList-like object
  const dataTransfer = new DataTransfer();
  files.forEach((file) => dataTransfer.items.add(file));
  fileInput.files = dataTransfer.files;

  updateFileList(dropZoneId, dataTransfer.files, true);
}

// Enhanced file list update
function updateFileList(dropZoneId, files, showFolderInfo = false) {
  const dropZone = document.getElementById(dropZoneId);
  const fileList = dropZone.querySelector(".file-list");
  const placeholder = dropZone.querySelector(".drop-placeholder");

  if (!fileList) return;

  if (files.length > 0) {
    if (placeholder) placeholder.style.display = "none";
    fileList.innerHTML = "";

    let totalSize = 0;
    let fileCount = 0;
    let folderCount = 0;

    Array.from(files).forEach((file, index) => {
      totalSize += file.size;
      fileCount++;

      // Check if it's a folder (based on webkitRelativePath)
      const isFolder =
        file.webkitRelativePath && file.webkitRelativePath.includes("/");
      if (isFolder) folderCount++;

      const fileItem = document.createElement("div");
      fileItem.className =
        "flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg mb-2";
      fileItem.innerHTML = `
      <div class="flex items-center flex-1 min-w-0">
      <i class="fas ${isFolder ? "fa-folder" : "fa-file"} text-${isFolder ? "yellow" : "gray"}-400 mr-3 flex-shrink-0"></i>
      <div class="min-w-0 flex-1">
      <div class="text-sm font-medium truncate">${file.name}</div>
      ${isFolder ? '<div class="text-xs text-gray-500 truncate">' + file.webkitRelativePath + "</div>" : ""}
      </div>
      </div>
      <div class="flex items-center space-x-3 flex-shrink-0 ml-2">
      <span class="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">${formatFileSize(file.size)}</span>
      <button type="button" onclick="removeFile('${dropZoneId}', ${index})" class="text-red-500 hover:text-red-700 transition-colors">
      <i class="fas fa-times"></i>
      </button>
      </div>
      `;
      fileList.appendChild(fileItem);
    });

    // Add summary for folders
    if (showFolderInfo && folderCount > 0) {
      const summary = document.createElement("div");
      summary.className =
        "mt-3 p-2 bg-blue-50 dark:bg-blue-900 rounded text-xs";
      summary.innerHTML = `
      <div class="flex justify-between">
      <span>Files: ${fileCount}</span>
      <span>Folders: ${folderCount}</span>
      <span>Total: ${formatFileSize(totalSize)}</span>
      </div>
      `;
      fileList.appendChild(summary);
    }
  } else {
    if (placeholder) placeholder.style.display = "block";
    fileList.innerHTML = "";
  }
}

// Format file size
function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Remove file from list
function removeFile(dropZoneId, index) {
  const inputId = dropZoneId.replace("-drop-zone", "-file-input");
  const fileInput = document.getElementById(inputId);
  const dt = new DataTransfer();

  Array.from(fileInput.files).forEach((file, i) => {
    if (i !== index) dt.items.add(file);
  });

  fileInput.files = dt.files;
  updateFileList(dropZoneId, fileInput.files);
}

// Setup functions for different tool options
function setupFormatOptions(selectId, formats) {
  const select = document.getElementById(selectId);
  if (!select) return;

  select.innerHTML = formats
    .map(
      (format) => `<option value="${format}">${format.toUpperCase()}</option>`,
    )
    .join("");
}

function setupAdvancedToggle(sectionId) {
  const toggle = document.querySelector(
    `[onclick="toggleAdvanced('${sectionId}')"]`,
  );
  if (toggle) {
    toggle.addEventListener("click", () => toggleAdvanced(sectionId));
  }
}

function toggleAdvanced(sectionId) {
  const section = document.getElementById(sectionId);
  if (!section) return;

  section.classList.toggle("hidden");

  const icon = section.previousElementSibling?.querySelector("i");
  if (icon) {
    if (section.classList.contains("hidden")) {
      icon.classList.replace("fa-chevron-up", "fa-chevron-down");
    } else {
      icon.classList.replace("fa-chevron-down", "fa-chevron-up");
    }
  }
}

// Quality slider setup
function setupQualitySlider() {
  const slider = document.querySelector('input[name="quality"]');
  const valueDisplay = document.getElementById("quality-value");

  if (slider && valueDisplay) {
    slider.addEventListener("input", (e) => {
      valueDisplay.textContent = e.target.value + "%";
    });
  }
}

// Language selector setup
function setupLanguageSelector() {
  const selector = document.querySelector('select[name="language"]');
  if (selector) {
    selector.addEventListener("change", (e) => {
      // You can add language-specific options here
      console.log("Selected language:", e.target.value);
    });
  }
}

// Page range selector
function setupPageRangeSelector() {
  const container = document.getElementById("page-range-container");
  if (!container) return;

  container.innerHTML = `
  <div class="space-y-2">
  <div class="flex items-center space-x-2">
  <input type="number" name="start_page" min="1" value="1"
  class="w-20 p-2 border rounded dark:bg-gray-700 dark:border-gray-600">
  <span>to</span>
  <input type="number" name="end_page" min="1"
  class="w-20 p-2 border rounded dark:bg-gray-700 dark:border-gray-600">
  <span class="text-sm text-gray-500">(leave empty for single page)</span>
  </div>
  <div class="flex space-x-2">
  <button type="button" onclick="addPageRange()" class="text-sm text-blue-600 hover:text-blue-800">
  <i class="fas fa-plus mr-1"></i>Add Range
  </button>
  <button type="button" onclick="clearPageRanges()" class="text-sm text-red-600 hover:text-red-800">
  <i class="fas fa-times mr-1"></i>Clear All
  </button>
  </div>
  </div>
  `;
}

// Font options setup
function setupFontOptions() {
  const fontSelect = document.querySelector('select[name="font_name"]');
  if (fontSelect) {
    const fonts = [
      "Arial",
      "Times New Roman",
      "Helvetica",
      "Courier New",
      "Verdana",
      "Georgia",
      "Palatino",
      "Garamond",
    ];

    fontSelect.innerHTML = fonts
      .map((font) => `<option value="${font}">${font}</option>`)
      .join("");
  }

  const sizeSelect = document.querySelector('select[name="font_size"]');
  if (sizeSelect) {
    const sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32];
    sizeSelect.innerHTML = sizes
      .map((size) => `<option value="${size}">${size}pt</option>`)
      .join("");
  }
}

// Audio effects setup
function setupAudioEffects() {
  const effectsContainer = document.getElementById("audio-effects-container");
  if (!effectsContainer) return;

  const effects = [
    { id: "noise_reduce", name: "Noise Reduction", icon: "volume-mute" },
    { id: "normalize", name: "Normalize", icon: "wave-square" },
    { id: "compressor", name: "Compressor", icon: "compress" },
    { id: "equalizer", name: "Equalizer", icon: "sliders-h" },
    { id: "reverb", name: "Reverb", icon: "expand" },
    { id: "delay", name: "Delay", icon: "clock" },
  ];

  effectsContainer.innerHTML = effects
    .map(
      (effect) => `
  <div class="flex items-center p-2 border rounded dark:border-gray-600">
  <input type="checkbox" id="${effect.id}" name="effects" value="${effect.id}"
  class="mr-2 rounded border-gray-300 text-blue-600">
  <label for="${effect.id}" class="flex items-center cursor-pointer">
  <i class="fas fa-${effect.icon} mr-2 text-gray-500"></i>
  <span class="text-sm">${effect.name}</span>
  </label>
  </div>
  `,
    )
    .join("");
}

// Video analysis options
function setupAnalysisOptions() {
  const optionsContainer = document.getElementById("analysis-options");
  if (!optionsContainer) return;

  optionsContainer.innerHTML = `
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div>
  <label class="flex items-center p-3 border rounded dark:border-gray-600 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
  <input type="checkbox" name="generate_thumbnails" class="mr-2 rounded border-gray-300 text-green-600" checked>
  <span class="text-sm">Generate Thumbnails</span>
  </label>
  </div>
  <div>
  <label class="flex items-center p-3 border rounded dark:border-gray-600 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
  <input type="checkbox" name="extract_audio" class="mr-2 rounded border-gray-300 text-green-600">
  <span class="text-sm">Extract Audio Analysis</span>
  </label>
  </div>
  <div>
  <label class="flex items-center p-3 border rounded dark:border-gray-600 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
  <input type="checkbox" name="detect_scenes" class="mr-2 rounded border-gray-300 text-green-600">
  <span class="text-sm">Detect Scene Changes</span>
  </label>
  </div>
  <div>
  <label class="flex items-center p-3 border rounded dark:border-gray-600 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
  <input type="checkbox" name="analyze_quality" class="mr-2 rounded border-gray-300 text-green-600">
  <span class="text-sm">Quality Analysis</span>
  </label>
  </div>
  </div>
  `;
}

// Batch processing options
function setupBatchOptions() {
  const modeSelect = document.querySelector('select[name="processing_mode"]');
  if (modeSelect) {
    modeSelect.addEventListener("change", (e) => {
      const threadsContainer = document.getElementById("threads-container");
      if (threadsContainer) {
        threadsContainer.style.display =
          e.target.value === "parallel" ? "block" : "none";
      }
    });
  }
}

// Initialize form submission
function initializeFormSubmission(toolId) {
  const form = document.getElementById(`${toolId}-form`);
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    submitToolForm(this, toolId);
  });
}

// Enhanced form submission
async function submitToolForm(form, toolId) {
  const formData = new FormData(form);
  const submitButton = form.querySelector('button[type="submit"]');
  const originalButtonText = submitButton.innerHTML;

  // Show loading state
  submitButton.disabled = true;
  submitButton.innerHTML =
    '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';

  try {
    // Show progress modal
    showProgressModal();
    updateProgress(10, "Validating files...");

    // Add CSRF token
    const csrfToken = getCSRFToken();
    formData.append("csrfmiddlewaretoken", csrfToken);

    const response = await fetch(`/api/process/${toolId}/`, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      updateProgress(100, "Processing complete!");
      setTimeout(() => {
        hideProgressModal();
        showResults(data.results, toolId);
      }, 1000);
    } else {
      throw new Error(data.error || "Processing failed");
    }
  } catch (error) {
    console.error("Error:", error);
    updateProgress(0, `Error: ${error.message}`);
    showError(error.message);

    setTimeout(() => {
      hideProgressModal();
    }, 3000);
  } finally {
    // Restore button state
    submitButton.disabled = false;
    submitButton.innerHTML = originalButtonText;
  }
}

// Progress modal functions
function showProgressModal() {
  const modal = document.getElementById("progress-modal");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
}

function hideProgressModal() {
  const modal = document.getElementById("progress-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

function updateProgress(percent, status) {
  const progressBar = document.getElementById("progress-bar");
  const progressPercent = document.getElementById("progress-percent");
  const progressStatus = document.getElementById("progress-status");

  if (progressBar) progressBar.style.width = percent + "%";
  if (progressPercent) progressPercent.textContent = percent + "%";
  if (progressStatus) progressStatus.textContent = status;
}

// Results display
function showResults(results, toolId) {
  // Create results container or redirect to results page
  const resultsContainer = document.getElementById("results-container");

  if (resultsContainer) {
    resultsContainer.classList.remove("hidden");
    resultsContainer.innerHTML = generateResultsHTML(results, toolId);
  } else {
    // Redirect to results page or show modal
    window.location.href = `/results/?tool=${toolId}&results=${encodeURIComponent(JSON.stringify(results))}`;
  }
}

function generateResultsHTML(results, toolId) {
  return `
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
  <div class="flex items-center justify-between mb-6">
  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
  <i class="fas fa-check-circle text-green-500 mr-2"></i>
  Processing Complete
  </h3>
  <span class="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm">
  ${results.length} files processed
  </span>
  </div>
  <div class="space-y-4">
  ${results
    .map(
      (result, index) => `
    <div class="flex items-center justify-between p-4 border rounded-lg dark:border-gray-600">
    <div class="flex items-center space-x-4">
    <i class="fas fa-file text-gray-400 text-xl"></i>
    <div>
    <div class="font-medium text-gray-900 dark:text-white">${result.original_name}</div>
    <div class="text-sm text-gray-500">${result.converted_name}</div>
    </div>
    </div>
    <div class="flex items-center space-x-2">
    <span class="text-sm text-gray-500">${result.size}</span>
    <button onclick="downloadFile('${result.download_url}')"
    class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors">
    <i class="fas fa-download mr-1"></i>Download
    </button>
    </div>
    </div>
    `,
    )
    .join("")}
    </div>
    <div class="mt-6 flex justify-end space-x-3">
    <button onclick="downloadAllFiles(${JSON.stringify(results)})"
    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition-colors">
    <i class="fas fa-download mr-2"></i>Download All
    </button>
    <button onclick="processNew()"
    class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded transition-colors">
    <i class="fas fa-plus mr-2"></i>New Conversion
    </button>
    </div>
    </div>
    `;
}

// Utility functions
function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
}

function showError(message) {
  // Create or show error notification
  const errorDiv =
    document.getElementById("error-notification") || createErrorNotification();
  errorDiv.querySelector(".error-message").textContent = message;
  errorDiv.classList.remove("hidden");

  setTimeout(() => {
    errorDiv.classList.add("hidden");
  }, 5000);
}

function createErrorNotification() {
  const div = document.createElement("div");
  div.id = "error-notification";
  div.className =
    "fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-lg z-50 hidden";
  div.innerHTML = `
  <div class="flex items-center">
  <i class="fas fa-exclamation-triangle mr-2"></i>
  <span class="error-message"></span>
  <button onclick="this.parentElement.parentElement.classList.add('hidden')"
  class="ml-4 text-red-700 hover:text-red-900">
  <i class="fas fa-times"></i>
  </button>
  </div>
  `;
  document.body.appendChild(div);
  return div;
}

// Additional utility functions for specific tools
function addPageRange() {
  // Implementation for adding page ranges
  console.log("Add page range functionality");
}

function clearPageRanges() {
  // Implementation for clearing page ranges
  console.log("Clear page ranges functionality");
}

function downloadFile(url) {
  window.open(url, "_blank");
}

function downloadAllFiles(results) {
  // Implementation for downloading all files
  results.forEach((result) => {
    downloadFile(result.download_url);
  });
}

function processNew() {
  // Reset form and UI for new processing
  document.querySelectorAll("form").forEach((form) => form.reset());
  document
    .querySelectorAll(".file-list")
    .forEach((list) => (list.innerHTML = ""));
  document.querySelectorAll(".drop-placeholder").forEach((placeholder) => {
    placeholder.style.display = "block";
  });

  const resultsContainer = document.getElementById("results-container");
  if (resultsContainer) {
    resultsContainer.classList.add("hidden");
  }
}

// Cancel processing
function cancelProcessing() {
  // Send cancel request to server
  fetch("/api/cancel/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
      "Content-Type": "application/json",
    },
  }).then(() => {
    hideProgressModal();
    showError("Processing cancelled");
  });
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize tool based on URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const toolParam = urlParams.get("tool");

  if (toolParam) {
    initializeTool(toolParam);
  }

  // Add global event listeners
  setupGlobalEventListeners();
});

function setupGlobalEventListeners() {
  // Escape key to close modals
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      hideProgressModal();
      const errorNotification = document.getElementById("error-notification");
      if (errorNotification) errorNotification.classList.add("hidden");
    }
  });

  // Click outside to close modals
  document.addEventListener("click", function (e) {
    const progressModal = document.getElementById("progress-modal");
    if (progressModal && e.target === progressModal) {
      hideProgressModal();
    }
  });
}

// Export functions for global access
window.initializeTool = initializeTool;
window.removeFile = removeFile;
window.toggleAdvanced = toggleAdvanced;
window.cancelProcessing = cancelProcessing;
window.downloadFile = downloadFile;
window.processNew = processNew;
