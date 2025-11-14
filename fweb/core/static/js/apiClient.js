class APIClient {
  constructor() {
    this.baseURL = "/api";
  }

  async submitToolForm(form, toolId) {
    const formData = new FormData(form);

    try {
      uiManager.setSubmitButtonState(form, true);
      uiManager.updateProgress(10, "Uploading files...");

      const response = await fetch(`${this.baseURL}/process/${toolId}/`, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": this.getCSRFToken(),
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        uiManager.updateProgress(100, "Processing complete!");
        setTimeout(() => {
          uiManager.hideProgressModal();
          this.handleSuccess(data, toolId);
        }, 1000);
      } else {
        throw new Error(data.error || "Processing failed");
      }
    } catch (error) {
      console.error("API Error:", error);
      uiManager.updateProgress(0, `Error: ${error.message}`);
      uiManager.showNotification(error.message, "error");

      setTimeout(() => {
        uiManager.hideProgressModal();
        uiManager.setSubmitButtonState(form, false);
      }, 2000);
    }
  }

  handleSuccess(data, toolId) {
    uiManager.showNotification(
      data.message || "Processing completed successfully",
      "success",
    );

    // Redirect to results page or show results in modal
    if (data.results && data.results.length > 0) {
      this.displayResults(data.results, toolId);
    }
  }

  displayResults(results, toolId) {
    // For now, just show a notification - will implement proper results display later
    uiManager.showNotification(
      `${results.length} files processed successfully`,
      "success",
    );
  }

  getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
  }

  async cancelProcessing(jobId) {
    try {
      const response = await fetch(`${this.baseURL}/cancel/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({ job_id: jobId }),
      });
      return await response.json();
    } catch (error) {
      console.error("Cancel error:", error);
      throw error;
    }
  }
}

window.apiClient = new APIClient();
