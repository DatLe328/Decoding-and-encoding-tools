const toggleThemeButton = document.getElementById("toggle-theme");
const themeIcon = document.getElementById("theme-icon");

if (localStorage.getItem("darkMode") === "enabled") {
	document.body.classList.add("dark-mode");
	themeIcon.classList.replace("bi-moon-fill", "bi-sun-fill");
}

toggleThemeButton.addEventListener("click", () => {
	document.body.classList.toggle("dark-mode");

	if (document.body.classList.contains("dark-mode")) {
		localStorage.setItem("darkMode", "enabled");
		themeIcon.classList.replace("bi-moon-fill", "bi-sun-fill");
	} else {
		localStorage.removeItem("darkMode");
		themeIcon.classList.replace("bi-sun-fill", "bi-moon-fill");
	}
});
