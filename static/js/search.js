// Search functionality - Fixed version
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

        // Add click outside listener to close dropdown
        document.addEventListener('click', (event) => {
            if (!this.searchInput.contains(event.target) && !this.dropdown.contains(event.target)) {
                this.hideDropdown();
            }
        });

        console.log('Search autocomplete initialized');
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

                // Enhancement: Add a visual indicator for projects that have saved data
                if (window.projectDataManager) {
                    console.log('Adding saved data indicators to search results');
                    this.results = this.results.map(result => {
                        // Check if there's saved data for this project
                        const hasSavedData = window.projectDataManager.hasProjectData(result.id);
                        return {
                            ...result,
                            hasSavedData
                        };
                    });
                } else {
                    console.warn('ProjectDataManager not found, cannot check for saved data');
                }

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
            a.className = 'block px-4 py-2 hover:bg-gray-100 flex justify-between items-center';

            // Add project name
            const nameSpan = document.createElement('span');
            nameSpan.textContent = result.text;
            a.appendChild(nameSpan);

            // Add indicator if there's saved data
            if (result.hasSavedData) {
                const savedIcon = document.createElement('span');
                savedIcon.className = 'ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800';
                savedIcon.textContent = 'Saved';
                a.appendChild(savedIcon);
            }

            a.dataset.id = result.id;
            a.dataset.text = result.text;

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
        console.log(`Project selected: ID=${result.id}, Name=${result.text}`);

        // Update the search input value
        this.searchInput.value = result.text;
        this.hideDropdown();

        // Update active project name in the header
        this.updateActiveProject(result.text, result.id);

        // Load project data from localStorage FIRST before loading issues
        // This ensures the form is populated with the correct data for this project
        if (window.loadProjectData) {
            console.log(`Calling loadProjectData for project ID: ${result.id}`);
            window.loadProjectData(result.id);
        } else {
            console.error('loadProjectData function not found');
        }

        // Load issues for the selected project
        if (typeof loadIssues === 'function') {
            loadIssues(result.id);
        }
    }

    // Update active project information
    updateActiveProject(projectName, projectId) {
        console.log(`Updating active project: ID=${projectId}, Name=${projectName}`);

        // Update the active project title
        const projectTitle = document.getElementById('active-project-title');
        if (projectTitle) {
            projectTitle.textContent = projectName || 'ACTIVE PROJECT NAME';
        }

        // Store the current project ID globally
        window.currentProjectId = projectId;

        // Also update the main script's currentProjectId
        if (typeof currentProjectId !== 'undefined') {
            currentProjectId = projectId;
        }

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

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - search.js running');

    // We'll check periodically if the search input exists
    // (since it may be loaded dynamically)
    const searchInitInterval = setInterval(() => {
        const searchInput = document.getElementById('search-dropdown');
        const dropdownElement = document.getElementById('autocomplete-dropdown');

        if (searchInput && dropdownElement) {
            console.log('Search elements found, initializing SearchAutocomplete');
            const searchAutoComplete = new SearchAutocomplete('#search-dropdown', '#autocomplete-dropdown');
            window.searchAutoComplete = searchAutoComplete; // Make it globally accessible
            clearInterval(searchInitInterval);
        }
    }, 100);
});