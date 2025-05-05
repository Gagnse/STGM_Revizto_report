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

        if (query.length < 2) {
            this.hideDropdown();
            return;
        }

        // In a real application, this would be an API call
        // For now, we'll simulate results
        this.fetchResults(query)
            .then(results => {
                this.results = results;
                this.renderResults();
                this.showDropdown();
            });
    }

    fetchResults(query) {
        // This would be replaced with a real API call in production
        return new Promise(resolve => {
            // Simulate network delay
            setTimeout(() => {
                // Mock results
                const mockResults = [
                    { id: 1, text: `Result for ${query} - Item 1` },
                    { id: 2, text: `Result for ${query} - Item 2` },
                    { id: 3, text: `Result for ${query} - Item 3` }
                ];
                resolve(mockResults);
            }, 200);
        });
    }

    renderResults() {
        // Clear previous results
        this.dropdown.innerHTML = '';

        if (this.results.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'p-4 text-sm text-gray-500';
            noResults.textContent = 'No results found';
            this.dropdown.appendChild(noResults);
            return;
        }

        // Create result list
        const ul = document.createElement('ul');
        ul.className = 'py-2 text-sm text-gray-700';

        this.results.forEach(result => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#'; // Would be a real URL in production
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
        // Handle selection
        this.searchInput.value = result.text;
        this.hideDropdown();

        // You could trigger additional actions here
        console.log('Selected:', result);
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
            new SearchAutocomplete('#search-dropdown', '#autocomplete-dropdown');
            clearInterval(searchInitInterval);
        }
    }, 100);
});