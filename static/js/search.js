// Search functionality with Django sessions for project data
document.addEventListener('DOMContentLoaded', function() {
    console.log('Search handler initialized');

    // Initialize search when elements are available
    initSearchWhenReady();
});

// Wait for search elements to be available, then initialize
function initSearchWhenReady() {
    const searchInput = document.getElementById('search-dropdown');
    const dropdownElement = document.getElementById('autocomplete-dropdown');

    if (searchInput && dropdownElement) {
        initSearch(searchInput, dropdownElement);
    } else {
        // Try again in 100ms
        setTimeout(initSearchWhenReady, 100);
    }
}

// Initialize search functionality
function initSearch(searchInput, dropdownElement) {
    let results = [];
    let debounceTimer = null;

    // Add event listeners
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            performSearch(searchInput.value.trim());
        }, 300);
    });

    searchInput.addEventListener('focus', function() {
        if (results.length > 0) {
            showDropdown();
        }
    });

    // Add click outside listener to close dropdown
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !dropdownElement.contains(event.target)) {
            hideDropdown();
        }
    });

    // Perform search
    function performSearch(query) {
        if (query.length < 2) {
            hideDropdown();
            return;
        }

        fetch(`/api/search/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                results = data.results || [];
                renderResults();
                showDropdown();
            })
            .catch(error => {
                console.error('Search error:', error);
                results = [];
                renderResults();
            });
    }

    // Render search results
    function renderResults() {
        // Clear previous results
        dropdownElement.innerHTML = '';

        if (results.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'p-4 text-sm text-gray-500';
            noResults.textContent = 'No projects found';
            dropdownElement.appendChild(noResults);
            return;
        }

        // Create result list
        const ul = document.createElement('ul');
        ul.className = 'py-2 text-sm text-gray-700';

        results.forEach(result => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.className = 'block px-4 py-2 hover:bg-gray-100 flex justify-between items-center';

            // Add project name
            const nameSpan = document.createElement('span');
            nameSpan.textContent = result.text;
            a.appendChild(nameSpan);

            // Add saved indicator if applicable
            if (result.hasSavedData) {
                const savedIcon = document.createElement('span');
                savedIcon.className = 'ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800';
                savedIcon.textContent = 'Saved';
                a.appendChild(savedIcon);
            }

            // Add click handler
            a.addEventListener('click', function(e) {
                e.preventDefault();
                selectProject(result);
            });

            li.appendChild(a);
            ul.appendChild(li);
        });

        dropdownElement.appendChild(ul);
    }

    // Select a project from search results
    function selectProject(project) {
        console.log(`Project selected: ${project.text} (ID: ${project.id})`);

        // Update search input
        searchInput.value = project.text;

        // Hide dropdown
        hideDropdown();

        // Update project title
        const projectTitle = document.getElementById('active-project-title');
        if (projectTitle) {
            projectTitle.textContent = project.text;
        }

        // Load project data using the project form handler
        if (window.projectForm && window.projectForm.loadProjectData) {
            window.projectForm.loadProjectData(project.id);
        } else {
            console.error('Project form handler not available');
        }

        // Load issues if function exists
        if (typeof loadIssues === 'function') {
            loadIssues(project.id);
        }
    }

    // Show dropdown
    function showDropdown() {
        dropdownElement.classList.remove('hidden');
    }

    // Hide dropdown
    function hideDropdown() {
        dropdownElement.classList.add('hidden');
    }

    console.log('Search functionality initialized');
}