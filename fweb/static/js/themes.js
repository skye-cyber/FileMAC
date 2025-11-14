document.addEventListener("DOMContentLoaded", () => {
  const themeSwitch = document.getElementById("theme-toggle");
  const rootElement = document.documentElement;

  // Initialize theme based on user's previous preference or system preference
  const userTheme = localStorage.getItem("theme");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
  const currentTheme = userTheme || systemTheme;

  // Set the initial theme
  setTheme(currentTheme);

  // Function to set the theme
  function setTheme(theme) {
    if (theme === "dark") {
      rootElement.classList.add("dark");
      themeSwitch.checked = true;
    } else {
      rootElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }

  // Toggle theme on switch click
  themeSwitch.addEventListener("click", () => {
    const newTheme = rootElement.classList.contains("dark") ? "light" : "dark";
    setTheme(newTheme);
  });
});
