document.addEventListener("DOMContentLoaded", function () {
  console.log("FileMac UI initialized");

  // Global cancel processing function
  window.cancelProcessing = function () {
    uiManager.hideProgressModal();
    uiManager.showNotification("Processing cancelled", "info");
  };

  // Global advanced section toggle
  window.toggleAdvanced = function (sectionId) {
    uiManager.toggleAdvancedSection(sectionId);
  };

  // Make sure tool interfaces are properly initialized
  const urlParams = new URLSearchParams(window.location.search);
  const toolParam = urlParams.get("tool");

  if (!toolParam) {
    // Ensure default tool is visible
    const firstTool = document.querySelector(".tool-interface");
    if (firstTool) {
      firstTool.classList.remove("hidden");
    }
  }
});
