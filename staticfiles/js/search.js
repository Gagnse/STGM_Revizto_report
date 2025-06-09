// Search functionality with Django sessions for project data
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Search handler initialized');

    // Set up global active project ID if it doesn't exist
    if (window.activeProjectId === undefined) {
        window.activeProjectId = null;
        console.log('[DEBUG] Initialized window.activeProjectId:', window.activeProjectId);
    }

    // Initialize search when elements are available
    initSearchWhenReady();
});

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
                savedIcon.textContent = 'Enregistré';
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

    // Set the active project ID globally
    window.activeProjectId = project.id;
    console.log('[DEBUG] Set window.activeProjectId to:', window.activeProjectId);

    // STEP 1: Clear the form before loading or creating project data
    console.log('[DEBUG] Clearing form before loading project data');
    if (window.projectForm && typeof window.projectForm.clearForm === 'function') {
        window.projectForm.clearForm();
    } else {
        console.error('[DEBUG] projectForm.clearForm function not available');
        // Fallback to basic form clearing
        clearFormFields();
    }

    // STEP 2: Load or create project data
    loadOrCreateProjectData(project.id);

    // STEP 3: Trigger event to notify issue data handler
    console.log('[DEBUG] Dispatching projectSelected event');
    const event = new CustomEvent('projectSelected', {
        detail: {
            projectId: project.id,
            projectName: project.text
        }
    });
    document.dispatchEvent(event);
}

    // Basic form clearing function as fallback
    function clearFormFields() {
        console.log('[DEBUG] Using fallback form clearing function');
        const formFields = [
            'report-date', 'project-name', 'project-owner', 'contractor',
            'visit-by', 'in-presence-of', 'visit-date', 'visit-number',
            'architect-file', 'distribution', 'project-description'
        ];

        formFields.forEach(fieldId => {
            const element = document.getElementById(fieldId);
            if (element) {
                element.value = '';
            }
        });

        // Reset image preview
        const imagePreview = document.getElementById('project-image-preview');
        if (imagePreview) {
            imagePreview.innerHTML = `
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
            `;
        }
    }

    // Load or create project data
    function loadOrCreateProjectData(projectId) {
        console.log('[DEBUG] Loading or creating project data for ID:', projectId);

        // Load existing data
        fetch(`/api/projects/${projectId}/data/load/`)
            .then(response => response.json())
            .then(data => {
                console.log('[DEBUG] Load response:', data);

                if (data.success) {
                    if (data.has_data) {
                        // Existing data found, populate form
                        console.log('[DEBUG] Existing data found, populating form');

                        // Use the project form handler if available
                        if (window.projectForm && typeof window.projectForm.populateForm === 'function') {
                            window.projectForm.populateForm(data.data);
                        } else {
                            // Fallback to our own implementation if projectForm not available
                            populateFormFields(data.data);
                        }

                        // Show last saved time if available
                        updateLastSavedStatus(data.data.lastSaved ? new Date(data.data.lastSaved) : new Date());
                    } else {
                        // No data found, create a new entry
                        console.log('[DEBUG] No data found, creating new entry');
                        createNewProjectEntry(projectId);
                    }
                } else {
                    console.error('[DEBUG] Error loading project data:', data.error);
                }
            })
            .catch(error => {
                console.error('[DEBUG] Error in load/create process:', error);
            });
    }

    // Create a new project entry
    function createNewProjectEntry(projectId) {
        console.log('[DEBUG] Creating new project entry for ID:', projectId);

        // Prepare empty data
        const emptyData = {
            projectId: projectId,
            lastSaved: new Date().toISOString()
            // other fields will be empty
        };

        // Save this empty data to create the entry
        fetch(`/api/projects/${projectId}/data/save/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(emptyData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('[DEBUG] New project entry created:', data);

            // Update status
            updateLastSavedStatus(new Date());
        })
        .catch(error => {
            console.error('[DEBUG] Error creating new project entry:', error);
        });
    }

    // Helper function to populate form with data (if projectForm is not available)
    function populateFormFields(data) {
        console.log('[DEBUG] Populating form fields with data');

        // Map data fields to form fields
        trySetFormValue('report-date', data.reportDate);
        trySetFormValue('project-name', data.projectName);
        trySetFormValue('project-owner', data.projectOwner);
        trySetFormValue('contractor', data.contractor);
        trySetFormValue('visit-by', data.visitBy);
        trySetFormValue('in-presence-of', data.inPresenceOf);
        trySetFormValue('visit-date', data.visitDate);
        trySetFormValue('visit-number', data.visitNumber);
        trySetFormValue('architect-file', data.architectFile);
        trySetFormValue('distribution', data.distribution);
        trySetFormValue('project-description', data.description);

        // Load image if available
        if (data.imageUrl) {
            const imagePreview = document.getElementById('project-image-preview');
            if (imagePreview) {
                // Clear previous content
                imagePreview.innerHTML = '';

                // Create and append image
                const img = document.createElement('img');
                img.src = data.imageUrl;
                img.className = 'w-full h-full object-cover';
                imagePreview.appendChild(img);
            }
        }
    }

    // Helper function to set form field value
    function trySetFormValue(elementId, value) {
        if (value) {
            const element = document.getElementById(elementId);
            if (element) {
                element.value = value;
            }
        }
    }

    // Helper function to update last saved status
    function updateLastSavedStatus(saveDate) {
        const lastSavedText = document.getElementById('last-saved-text');
        const dataStatus = document.getElementById('data-status');

        if (lastSavedText) {
            const formattedDate = saveDate.toLocaleString();
            lastSavedText.textContent = `Dernière sauvegarde: ${formattedDate}`;
        }

        if (dataStatus) {
            dataStatus.classList.remove('hidden');
        }
    }

    // Helper function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
            document.cookie.split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1] || '';
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

// Make functions available globally
window.searchFunctions = {
    loadOrCreateProjectData: function(projectId) {
        console.log('[DEBUG] Global function loadOrCreateProjectData called with ID:', projectId);
        // This function would need to be implemented here if needed globally
    }
};