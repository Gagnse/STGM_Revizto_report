// Search functionality
class SearchAutocomplete {
    constructor(inputSelector, dropdownSelector) {
        this.searchInput = document.querySelector(inputSelector);
        this.dropdown = document.querySelector(dropdownSelector);
        this.results = [];
        this.debounceTimer = null;

        this.init();
    }

    init() {
        if (!this.searchInput || !this.dropdown) return;

        // Add event listeners
        this.searchInput.addEventListener('input', () => this.debounceSearch());
        this.searchInput.addEventListener('focus', () => this.showDropdown());
    }

    debounceSearch() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.performSearch();
        }, 300); // Wait 300ms after typing stops
    }

    performSearch() {
        const query = this.searchInput.value.trim();
        console.log("Searching for:", query);

        if (query.length < 2) {
            this.hideDropdown();
            return;
        }

        // Call the real API endpoint
        fetch(`/api/search/?query=${encodeURIComponent(query)}`)
            .then(response => {
                console.log("Search response status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Search results:", data);
                this.results = data.results || [];
                this.renderResults();
                this.showDropdown();
            })
            .catch(error => {
                console.error('Search error:', error);
                this.results = [];
                this.renderResults();
                this.showDropdown();
            });
    }

    renderResults() {
        // Clear previous results
        this.dropdown.innerHTML = '';

        if (this.results.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'p-4 text-sm text-gray-500';
            noResults.textContent = 'No projects found';
            this.dropdown.appendChild(noResults);
            return;
        }

        // Create result list
        const ul = document.createElement('ul');
        ul.className = 'py-2 text-sm text-gray-700';

        this.results.forEach(result => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#'; // We'll handle navigation via JavaScript
            a.className = 'block px-4 py-2 hover:bg-gray-100';
            a.textContent = result.text;
            a.dataset.id = result.id;

            a.addEventListener('click', (e) => {
                e.preventDefault();
                this.selectResult(result);
            });

            li.appendChild(a);
            ul.appendChild(li);
        });

        this.dropdown.appendChild(ul);
    }

    selectResult(result) {
        // Handle selection - load issues for the selected project
        this.searchInput.value = result.text;
        this.hideDropdown();

        // Update active project name in the header
        this.updateActiveProject(result.text, result.id);

        // Load issues for the selected project
        loadIssues(result.id);
    }

    // New method to update active project information
    updateActiveProject(projectName, projectId) {
        // Update the active project title
        const projectTitle = document.getElementById('active-project-title');
        if (projectTitle) {
            projectTitle.textContent = projectName || 'ACTIVE PROJECT NAME';
        }

        // Store the current project ID
        window.currentProjectId = projectId;

        // Don't pre-fill the project name field since it's manually input
        // and different from the API title

        console.log(`Active project updated: ${projectName} (ID: ${projectId})`);
    }

    showDropdown() {
        if (this.results.length > 0 || this.searchInput.value.trim().length >= 2) {
            this.dropdown.classList.remove('hidden');
        }
    }

    hideDropdown() {
        this.dropdown.classList.add('hidden');
    }
}

// Initialize when the navbar is loaded
document.addEventListener('DOMContentLoaded', function() {
    // We'll check periodically if the search input exists
    // (since it's loaded dynamically)
    const searchInitInterval = setInterval(() => {
        if (document.getElementById('search-dropdown')) {
            const searchAutoComplete = new SearchAutocomplete('#search-dropdown', '#autocomplete-dropdown');
            window.searchAutoComplete = searchAutoComplete; // Make it globally accessible
            clearInterval(searchInitInterval);
        }
    }, 100);
});