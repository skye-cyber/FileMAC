// AJAX file processing
function submitToolForm(formId, toolId) {
  const form = document.getElementById(formId);
  const formData = new FormData(form);

  // Show progress modal
  showProgressModal();
  updateProgress(10, "Starting processing...");

  // Add CSRF token
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`/api/process/${toolId}/`, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        updateProgress(100, "Processing complete!");
        setTimeout(() => {
          hideProgressModal();
          showResults(data.results);
        }, 1000);
      } else {
        updateProgress(0, `Error: ${data.error}`);
        setTimeout(hideProgressModal, 2000);
      }
    })
    .catch((error) => {
      updateProgress(0, `Network error: ${error}`);
      setTimeout(hideProgressModal, 2000);
    });
}

// Update your form submission handlers
document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners to all tool forms
  const forms = document.querySelectorAll('form[id$="-form"]');
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const toolId = form.id.replace("-form", "");
      submitToolForm(form.id, toolId);
    });
  });
});
