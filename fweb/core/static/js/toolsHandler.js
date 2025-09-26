// Initialize first tool if specified in URL
document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const toolParam = urlParams.get("tool");
  if (toolParam) {
    showTool(toolParam, "{{ category }}");
  } else {
    // Show first tool by default
    const firstTool = document.querySelector(".tool-nav");
    if (firstTool) {
      const toolId = firstTool.classList[1].replace("tool-", "");
      showTool(toolId, "{{ category }}");
    }
  }
});

function showProgressModal() {
  document.getElementById("progress-modal").classList.remove("hidden");
}

function hideProgressModal() {
  document.getElementById("progress-modal").classList.add("hidden");
}

function updateProgress(percent, status) {
  document.getElementById("progress-bar").style.width = percent + "%";
  document.getElementById("progress-percent").textContent = percent + "%";
  document.getElementById("progress-status").textContent = status;
}

function cancelProcessing() {
  // Implement cancellation logic
  hideProgressModal();
}

// Form submission handler
function handleToolSubmit(formId, endpoint) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    showProgressModal();
    updateProgress(10, "Uploading files...");

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        updateProgress(100, "Processing complete!");
        setTimeout(() => {
          hideProgressModal();
          // Handle success
        }, 1000);
      } else {
        throw new Error("Processing failed");
      }
    } catch (error) {
      updateProgress(0, "Error occurred");
      setTimeout(hideProgressModal, 2000);
    }
  });
}
