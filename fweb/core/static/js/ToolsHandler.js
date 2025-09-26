class ToolHandler {
  constructor() {
    this.currentTool = null;
    this.category = document.body.dataset.category || "document";
    this.init();
  }

  init() {
    this.setupToolNavigation();
    this.initializeFromURL();
  }

  setupToolNavigation() {
    // Add click handlers to all tool navigation items
    document.addEventListener("click", (e) => {
      const toolNav = e.target.closest(".tool-nav");
      if (toolNav) {
        const toolId = this.getToolIdFromElement(toolNav);
        if (toolId) {
          this.showTool(toolId);
          e.preventDefault();
        }
      }
    });
  }

  getToolIdFromElement(element) {
    // Find the tool ID from element's classes (class="tool-nav tool-{id}")
    for (let className of element.classList) {
      if (className.startsWith("tool-") && className !== "tool-nav") {
        return className.replace("tool-", "");
      }
    }
    return null;
  }

  showTool(toolId, category) {
    this.category = category;
    // Hide all tool interfaces
    this.hideAllToolInterfaces();

    // Show selected tool
    const selectedTool = document.getElementById(`tool-${toolId}`);
    if (selectedTool) {
      selectedTool.classList.remove("hidden");
      this.currentTool = toolId;
    }

    // Update active navigation
    this.updateActiveNav(toolId);

    // Update URL
    this.updateURL(toolId);

    // Initialize tool-specific functionality
    this.initializeTool(toolId);
  }

  hideAllToolInterfaces() {
    document.querySelectorAll(".tool-interface").forEach((_interface) => {
      _interface.classList.add("hidden");
    });
  }

  updateActiveNav(toolId) {
    document.querySelectorAll(".tool-nav").forEach((nav) => {
      nav.classList.remove("tool-active");
    });

    const activeNav = document.querySelector(`.tool-${toolId}`);
    if (activeNav) {
      activeNav.classList.add("tool-active");
    }
  }

  updateURL(toolId) {
    const newUrl = `${window.location.pathname}?tool=${toolId}`;
    window.history.replaceState({ tool: toolId }, "", newUrl);
  }

  initializeTool(toolId) {
    const toolConfigs = {
      // Document Tools
      convert_doc: () => this.initDocumentConversion(),
      pdf_join: () => this.initPDFJoining(),
      scan_pdf: () => this.initPDFScanning(),
      doc_long_image: () => this.initLongImageConversion(),
      extract_pages: () => this.initPageExtraction(),
      Atext2word: () => this.initTextToWord(),
      doc2image: () => this.initDocToImage(),

      // Image Tools
      convert_image: () => this.initImageConversion(),
      resize_image: () => this.initImageResize(),
      image2pdf: () => this.initImageToPDF(),
      image2word: () => this.initImageToWord(),
      image2gray: () => this.initGrayscaleConversion(),
      ocr: () => this.initOCR(),

      // Audio Tools
      convert_audio: () => this.initAudioConversion(),
      audio_join: () => this.initAudioJoining(),
      extract_audio: () => this.initAudioExtraction(),
      audio_effect: () => this.initAudioEffects(),

      // Video Tools
      convert_video: () => this.initVideoConversion(),
      analyze_video: () => this.initVideoAnalysis(),

      // Batch Tools
      batch_dashboard: () => this.initBatchDashboard(),
      batch_doc_convert: () => this.initBatchDocConversion(),
      folder_operations: () => this.initFolderOperations(),
      bulk_ocr: () => this.initBulkOCR(),
    };

    if (toolConfigs[toolId]) {
      toolConfigs[toolId]();
    } else {
      console.warn(`No initialization found for tool: ${toolId}`);
    }
  }

  // Tool-specific initialization methods
  initDocumentConversion() {
    fileHandler.setupFileDropZone("doc-drop-zone", "doc-file-input", true);
    this.setupFormatSelector("doc-target-format", [
      "pdf",
      "docx",
      "txt",
      "html",
    ]);
  }

  initImageConversion() {
    fileHandler.setupFileDropZone("image-drop-zone", "image-file-input", true);
    this.setupFormatSelector("image-target-format", [
      "png",
      "jpg",
      "jpeg",
      "webp",
      "gif",
    ]);
    this.setupQualitySlider();
  }

  initAudioConversion() {
    fileHandler.setupFileDropZone("audio-drop-zone", "audio-file-input", true);
    this.setupFormatSelector("audio-target-format", [
      "mp3",
      "wav",
      "flac",
      "m4a",
    ]);
  }

  initVideoConversion() {
    fileHandler.setupFileDropZone("video-drop-zone", "video-file-input", false);
    this.setupFormatSelector("video-target-format", [
      "mp4",
      "mkv",
      "avi",
      "mov",
    ]);
  }

  initOCR() {
    fileHandler.setupFileDropZone("ocr-drop-zone", "ocr-file-input", true);
    this.setupLanguageSelector();
  }

  // Add more tool initialization methods as needed...

  // Utility methods for tool setup
  setupFormatSelector(selectId, formats) {
    const select = document.getElementById(selectId);
    if (select) {
      select.innerHTML = formats
        .map(
          (format) =>
            `<option value="${format}">${format.toUpperCase()}</option>`,
        )
        .join("");
    }
  }

  setupQualitySlider() {
    const slider = document.querySelector('input[name="quality"]');
    const valueDisplay = document.getElementById("quality-value");

    if (slider && valueDisplay) {
      slider.addEventListener("input", (e) => {
        valueDisplay.textContent = `${e.target.value}%`;
      });
    }
  }

  setupLanguageSelector() {
    const languages = {
      eng: "English",
      spa: "Spanish",
      fra: "French",
      deu: "German",
      chi_sim: "Chinese Simplified",
    };

    const selector = document.querySelector('select[name="language"]');
    if (selector) {
      selector.innerHTML = Object.entries(languages)
        .map(([code, name]) => `<option value="${code}">${name}</option>`)
        .join("");
    }
  }

  initializeFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const toolParam = urlParams.get("tool");

    if (toolParam) {
      this.showTool(toolParam);
    } else {
      // Show first tool by default
      this.showDefaultTool();
    }
  }

  showDefaultTool() {
    const firstToolNav = document.querySelector(".tool-nav");
    if (firstToolNav) {
      const toolId = this.getToolIdFromElement(firstToolNav);
      if (toolId) {
        this.showTool(toolId);
      }
    }
  }

  getCurrentTool() {
    return this.currentTool;
  }
}

window.toolHandler = new ToolHandler();
