// Theme toggle functionality
const THEME_STORAGE_KEY = '_remdingo_theme';
const DARK_THEME_CLASS = 'dark-theme';
const LIGHT_ICON_CLASS = 'fa-sun';
const DARK_ICON_CLASS = 'fa-moon';

function getStoredTheme() {
    return localStorage.getItem(THEME_STORAGE_KEY);
}

function setStoredTheme(theme) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
}

function applyTheme(theme) {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');

    if (theme === 'dark') {
        body.classList.add(DARK_THEME_CLASS);
        if (themeIcon) {
            themeIcon.classList.remove(DARK_ICON_CLASS);
            themeIcon.classList.add(LIGHT_ICON_CLASS);
        }
    } else {
        body.classList.remove(DARK_THEME_CLASS);
        if (themeIcon) {
            themeIcon.classList.remove(LIGHT_ICON_CLASS);
            themeIcon.classList.add(DARK_ICON_CLASS);
        }
    }
}

function toggleTheme() {
    const currentTheme = document.body.classList.contains(DARK_THEME_CLASS) ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    applyTheme(newTheme);
    setStoredTheme(newTheme);
}

// Initialize theme on page load
function initTheme() {
    const storedTheme = getStoredTheme();
    
    if (storedTheme) {
        applyTheme(storedTheme);
    }
    
    // Set up click handler for theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

// Run when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}

