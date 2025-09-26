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

      const icon = section.previousElementSibling?.querySelector("i");
      if (icon) {
        icon.classList.toggle("fa-chevron-up");
        icon.classList.toggle("fa-chevron-down");
      }
    }
  }

  setSubmitButtonState(form, loading) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
      if (loading) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
      } else {
        submitButton.disabled = false;
        submitButton.innerHTML = '<i class="fas fa-cog mr-2"></i>Process Files';
      }
    }
  }
}

window.uiManager = new UIManager();
