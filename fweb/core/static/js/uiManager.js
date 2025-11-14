class UIManager {
  constructor() {
    this.progressModal = document.getElementById("progress-modal");
    this.init();
  }

  init() {
    this.setupGlobalUIHandlers();
  }

  setupGlobalUIHandlers() {
    // Escape key to close modals
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        this.closeAllModals();
      }
    });

    // Outside click to close modals
    document.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal-overlay")) {
        this.closeAllModals();
      }
    });

    // Form submissions
    this.setupFormHandlers();
  }

  setupFormHandlers() {
    document.addEventListener("submit", (e) => {
      const form = e.target;
      if (form.classList.contains("tool-form")) {
        e.preventDefault();
        this.handleToolFormSubmit(form);
      }
    });
  }

  handleToolFormSubmit(form) {
    const toolId = form.dataset.toolId;
    if (!toolId) {
      console.error("No tool ID found for form");
      return;
    }

    this.showProgressModal();
    apiClient.submitToolForm(form, toolId);
  }

  showProgressModal() {
    if (this.progressModal) {
      this.progressModal.classList.remove("hidden");
      this.updateProgress(0, "Initializing...");
    }
  }

  hideProgressModal() {
    if (this.progressModal) {
      this.progressModal.classList.add("hidden");
    }
  }

  updateProgress(percent, status) {
    const progressBar = document.getElementById("progress-bar");
    const progressPercent = document.getElementById("progress-percent");
    const progressStatus = document.getElementById("progress-status");

    if (progressBar) progressBar.style.width = percent + "%";
    if (progressPercent) progressPercent.textContent = percent + "%";
    if (progressStatus) progressStatus.textContent = status;
  }

  closeAllModals() {
    this.hideProgressModal();
    // Add other modals here as needed
  }

  showNotification(message, type = "info") {
    // Simple notification system - can be enhanced with Toast library
    const notification = document.createElement("div");
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
      type === "error"
        ? "bg-red-500 text-white"
        : type === "success"
          ? "bg-green-500 text-white"
          : "bg-blue-500 text-white"
    }`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  toggleAdvancedSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.classList.toggle("hidden");

      const svg = section.previousElementSibling?.querySelector("svg");
      if (svg) {
        svg.classList.toggle("rotate-180");
      }
    }
  }

  setSubmitButtonState(form, loading) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
      if (loading) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<span class="h-5 w-5 fill-current fas fa-spinner spin mr-2"><svg><s/vg>Processing...</span';
      } else {
        submitButton.disabled = false;
        submitButton.innerHTML = `<span class="flex-justify-center items-center mr-2">
          <svg class="h-5 w-5 fill-current dark:fill-gray-200 mb-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path d="M176 544C96.5 544 32 479.5 32 400C32 336.6 73 282.8 129.9 263.5C128.6 255.8 128 248 128 240C128 160.5 192.5 96 272 96C327.4 96 375.5 127.3 399.6 173.1C413.8 164.8 430.4 160 448 160C501 160 544 203 544 256C544 271.7 540.2 286.6 533.5 299.7C577.5 320 608 364.4 608 416C608 486.7 550.7 544 480 544L176 544zM337 255C327.6 245.6 312.4 245.6 303.1 255L231.1 327C221.7 336.4 221.7 351.6 231.1 360.9C240.5 370.2 255.7 370.3 265 360.9L296 329.9L296 432C296 445.3 306.7 456 320 456C333.3 456 344 445.3 344 432L344 329.9L375 360.9C384.4 370.3 399.6 370.3 408.9 360.9C418.2 351.5 418.3 336.3 408.9 327L336.9 255z"/></svg>Process Files</span>`;
      }
    }
  }
}

window.uiManager = new UIManager();
