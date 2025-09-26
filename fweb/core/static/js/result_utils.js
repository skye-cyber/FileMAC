function downloadAll() {
  // Create a zip of all files and download
  alert("Batch download functionality would be implemented here");
}

function previewFile(url) {
  // Load and display file preview
  document.getElementById("preview-modal").classList.remove("hidden");
  // Implementation would load the file content based on type
}

function closePreview() {
  document.getElementById("preview-modal").classList.add("hidden");
}

// Keyboard shortcut to close preview
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closePreview();
  }
});
