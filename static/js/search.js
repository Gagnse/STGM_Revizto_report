// Search functionality with Django sessions for project data
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Search handler initialized');

    // Check if window.activeProjectId exists
    console.log('[DEBUG] Initial window.activeProjectId in search.js:', window.activeProjectId);

    // Initialize search when elements are available
    initSearchWhenReady();

    // Add a button to the page for debugging
    addDebugButton();
});

// Add a debug button to test active project ID
function addDebugButton() {
    // Create a button element
    const debugBtn = document.createElement('button');
    debugBtn.textContent = 'Debug Project ID';
    debugBtn.className = 'px-4 py-2 mt-4 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300';
    debugBtn.style.position = 'fixed';
    debugBtn.style.bottom = '10px';
    debugBtn.style.right = '10px';
    debugBtn.style.zIndex = '9999';

    // Add click event
    debugBtn.addEventListener('click', function() {
        console.log('[DEBUG] Debug button clicked');
        console.log('[DEBUG] Current window.activeProjectId:', window.activeProjectId);
        console.log('[DEBUG] typeof activeProjectId:', typeof window.activeProjectId);

        // Check if the global variables are shared correctly
        if (window.projectForm) {
            console.log('[DEBUG] window.projectForm exists');
            try {
                // Try to call the debug function if it exists
                if (window.debugProjectId) {
                    const result = window.debugProjectId();
                    console.log('[DEBUG] Result from window.debugProjectId():', result);
                }
            } catch (e) {
                console.error('[DEBUG] Error calling debug function:', e);
            }
        } else {
            console.error('[DEBUG] window.projectForm does not exist!');
        }

        // Check all related global variables
        console.log('[DEBUG] All properties of window related to project:',
            Object.keys(window).filter(key => key.toLowerCase().includes('project')));

        // Show an alert with the current project ID
        alert('Current active project ID: ' + (window.activeProjectId || 'None'));
    });

    // Add to document body
    document.body.appendChild(debugBtn);
    console.log('[DEBUG] Debug button added to page');
}

// Wait for search elements to be available, then initialize
function initSearchWhenReady() {
    const searchInput = document.getElementById('search-dropdown');
    const dropdownElement = document.getElementById('autocomplete-dropdown');

    if (searchInput && dropdownElement) {
        console.log('[DEBUG] Search elements found, initializing search');
        initSearch(searchInput, dropdownElement);
    } else {
        console.log('[DEBUG] Search elements not found, retrying in 100ms');
        // Try again in 100ms
        setTimeout(initSearchWhenReady, 100);
    }
}

// Initialize search functionality
function initSearch(searchInput, dropdownElement) {
    let results = [];
    let debounceTimer = null;

    console.log('[DEBUG] Initializing search with elements:',
                searchInput ? 'Search input found' : 'Search input missing',
                dropdownElement ? 'Dropdown found' : 'Dropdown missing');

    // Add event listeners
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            performSearch(searchInput.value.trim());
        }, 300);
    });

    searchInput.addEventListener('focus', function() {
        console.log('[DEBUG] Search input focused');
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
        console.log('[DEBUG] Performing search with query:', query);

        if (query.length < 2) {
            console.log('[DEBUG] Query too short, hiding dropdown');
            hideDropdown();
            return;
        }

        console.log('[DEBUG] Fetching search results for query:', query);
        fetch(`/api/search/?query=${encodeURIComponent(query)}`)
            .then(response => {
                console.log('[DEBUG] Search response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('[DEBUG] Search results received:', data.results ? data.results.length : 0, 'results');
                results = data.results || [];
                renderResults();
                showDropdown();
            })
            .catch(error => {
                console.error('[DEBUG] Search error:', error);
                results = [];
                renderResults();
            });
    }

    // Render search results
    function renderResults() {
        // Clear previous results
        dropdownElement.innerHTML = '';
        console.log('[DEBUG] Rendering', results.length, 'search results');

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
        console.log('[DEBUG] Project selected:', project);
        console.log(`[DEBUG] Project details - ID: ${project.id}, Name: ${project.text}`);

        // Update search input
        searchInput.value = project.text;
        console.log('[DEBUG] Updated search input value to:', project.text);

        // Hide dropdown
        hideDropdown();
        console.log('[DEBUG] Dropdown hidden');

        // Update project title
        const projectTitle = document.getElementById('active-project-title');
        if (projectTitle) {
            projectTitle.textContent = project.text;
            console.log('[DEBUG] Project title updated to:', project.text);
        } else {
            console.error('[DEBUG] Project title element not found');
        }

        // Explicitly set the active project ID on the window object
        console.log('[DEBUG] Before setting: window.activeProjectId =', window.activeProjectId);
        window.activeProjectId = project.id;
        console.log('[DEBUG] After setting: window.activeProjectId =', window.activeProjectId);

        // Create a global variable with a different name as a backup
        window.selectedProjectId = project.id;
        console.log('[DEBUG] Created backup global: window.selectedProjectId =', window.selectedProjectId);

        // Set as global variable with fully qualified name
        console.log('[DEBUG] Setting window.activeProjectId directly');
        try {
            // Try to forcefully set using window object
            Object.defineProperty(window, 'activeProjectId', {
                value: project.id,
                writable: true,
                configurable: true
            });
            console.log('[DEBUG] Forcefully set window.activeProjectId to:', project.id);
        } catch (e) {
            console.error('[DEBUG] Error forcefully setting activeProjectId:', e);
        }

        // Double-check that it was set
        console.log('[DEBUG] Double checking activeProjectId value:', window.activeProjectId);

        // Try to create a closure with the project ID
        (function(projectId) {
            console.log('[DEBUG] Inside closure, projectId =', projectId);
            window.latestProjectId = projectId;
            console.log('[DEBUG] From closure, set window.latestProjectId =', window.latestProjectId);
        })(project.id);

        // Load project data using the project form handler
        if (window.projectForm && typeof window.projectForm.loadProjectData === 'function') {
            console.log('[DEBUG] Calling window.projectForm.loadProjectData with ID:', project.id);

            // Pass both the parameter and set the global variable
            window.projectForm.loadProjectData(project.id);

            // Check after loading
            setTimeout(function() {
                console.log('[DEBUG] After loadProjectData, activeProjectId =', window.activeProjectId);
            }, 500);
        } else {
            console.error('[DEBUG] Project form handler not available or loadProjectData is not a function');
            console.error('[DEBUG] window.projectForm exists:', !!window.projectForm);
            if (window.projectForm) {
                console.error('[DEBUG] loadProjectData exists:', !!window.projectForm.loadProjectData);
                console.error('[DEBUG] loadProjectData type:', typeof window.projectForm.loadProjectData);
            }
        }

        // Load issues if function exists
        if (typeof loadIssues === 'function') {
            console.log('[DEBUG] Calling loadIssues with ID:', project.id);
            loadIssues(project.id);
        } else {
            console.log('[DEBUG] loadIssues function not found, skipping');
        }

        // Alert the user for debugging
        console.log('[DEBUG] Project selection complete');
        console.log('[DEBUG] Final activeProjectId =', window.activeProjectId);

        // Create a visible indicator
        const indicator = document.createElement('div');
        indicator.style.position = 'fixed';
        indicator.style.top = '10px';
        indicator.style.right = '10px';
        indicator.style.padding = '8px 12px';
        indicator.style.background = '#e0f7fa';
        indicator.style.border = '1px solid #4fc3f7';
        indicator.style.borderRadius = '4px';
        indicator.style.zIndex = '9999';
        indicator.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        indicator.textContent = `Active Project: ${project.text} (ID: ${project.id})`;

        // Remove any existing indicators
        const existingIndicator = document.getElementById('project-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }

        // Add ID to new indicator
        indicator.id = 'project-indicator';

        // Add to document
        document.body.appendChild(indicator);

        // Remove after 5 seconds
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.remove();
            }
        }, 5000);
    }

    // Show dropdown
    function showDropdown() {
        dropdownElement.classList.remove('hidden');
        console.log('[DEBUG] Dropdown shown');
    }

    // Hide dropdown
    function hideDropdown() {
        dropdownElement.classList.add('hidden');
        console.log('[DEBUG] Dropdown hidden');
    }

    console.log('[DEBUG] Search functionality fully initialized');
}