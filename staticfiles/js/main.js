// Modified main.js - removed unnecessary component loading
document.addEventListener('DOMContentLoaded', function() {
    // Initialize search dropdown functionality
    initializeSearchDropdown();
});

// Initialize search dropdown functionality
function initializeSearchDropdown() {
    // Get DOM elements
    const searchInput = document.getElementById('search-dropdown');
    const autocompleteDropdown = document.getElementById('autocomplete-dropdown');

    if (!searchInput || !autocompleteDropdown) return;

    // Show dropdown when input is focused
    searchInput.addEventListener('focus', () => {
        autocompleteDropdown.classList.remove('hidden');
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (event) => {
        if (!searchInput.contains(event.target) && !autocompleteDropdown.contains(event.target)) {
            autocompleteDropdown.classList.add('hidden');
        }
    });

    // Show/hide dropdown based on input
    searchInput.addEventListener('input', () => {
        if (searchInput.value.length > 0) {
            autocompleteDropdown.classList.remove('hidden');
            // Here you would typically filter the dropdown options based on input
            // This would be connected to your backend in a real implementation
        } else {
            autocompleteDropdown.classList.add('hidden');
        }
    });

    // Sample function for keyboard navigation in dropdown
    searchInput.addEventListener('keydown', (event) => {
        if (!autocompleteDropdown.classList.contains('hidden')) {
            const items = autocompleteDropdown.querySelectorAll('a');
            const activeItem = autocompleteDropdown.querySelector('a.active');

            switch(event.key) {
                case 'ArrowDown':
                    event.preventDefault();
                    if (!activeItem) {
                        items[0].classList.add('active');
                    } else {
                        const nextItem = activeItem.parentElement.nextElementSibling;
                        if (nextItem) {
                            activeItem.classList.remove('active');
                            nextItem.querySelector('a').classList.add('active');
                        }
                    }
                    break;
                case 'ArrowUp':
                    event.preventDefault();
                    if (activeItem) {
                        const prevItem = activeItem.parentElement.previousElementSibling;
                        if (prevItem) {
                            activeItem.classList.remove('active');
                            prevItem.querySelector('a').classList.add('active');
                        }
                    }
                    break;
                case 'Enter':
                    if (activeItem) {
                        event.preventDefault();
                        activeItem.click();
                    }
                    break;
                case 'Escape':
                    autocompleteDropdown.classList.add('hidden');
                    break;
            }
        }
    });
}