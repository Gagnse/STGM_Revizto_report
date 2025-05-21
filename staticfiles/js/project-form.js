// Form data management using Django's session storage with enhanced debugging
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Project form handler initialized');

    // Current active project ID
    window.activeProjectId = null;
    console.log('[DEBUG] Initial window.activeProjectId set to:', window.activeProjectId);

    // Initialize form handlers
    initFormHandlers();

    // Initialize image upload
    initImageUpload();
});

// Initialize form event handlers
function initFormHandlers() {
    // Save button handler
    const saveBtn = document.getElementById('save-project-info');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            console.log('[DEBUG] Save button clicked');

            if (!window.activeProjectId) {
                console.error('[DEBUG] No active project selected');
                showMessage('Please select a project first', 'error');
                return;
            }

            saveProjectData(window.activeProjectId);
        });
    } else {
        console.error('[DEBUG] Save button not found in the DOM');
    }

    // Clear button handler
    const clearBtn = document.getElementById('clear-project-info');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            console.log('[DEBUG] Clear button clicked');

            if (!window.activeProjectId) {
                console.error('[DEBUG] No active project selected');
                showMessage('Please select a project first', 'error');
                return;
            }

            clearForm();
        });
    } else {
        console.error('[DEBUG] Clear button not found in the DOM');
    }
}

// Initialize image upload functionality
function initImageUpload() {
    const uploadBtn = document.getElementById('upload-image-btn');
    const fileInput = document.getElementById('project-image-upload');
    const imagePreview = document.getElementById('project-image-preview');

    if (uploadBtn && fileInput && imagePreview) {
        console.log('[DEBUG] Image upload components found');

        uploadBtn.addEventListener('click', () => {
            console.log('[DEBUG] Upload button clicked');
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                console.log('[DEBUG] File selected:', file.name, 'Size:', file.size, 'Type:', file.type);

                const reader = new FileReader();
                reader.onload = (e) => {
                    console.log('[DEBUG] File read successfully');

                    // Clear previous content
                    imagePreview.innerHTML = '';

                    // Create and append image
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'w-full h-full object-cover';
                    imagePreview.appendChild(img);

                    console.log('[DEBUG] Image preview updated');
                };

                reader.onerror = (e) => {
                    console.error('[DEBUG] Error reading file:', e);
                };

                reader.readAsDataURL(file);
                console.log('[DEBUG] Started reading file as Data URL');
            }
        });
    } else {
        console.error('[DEBUG] One or more image upload components not found');
    }
}

// Function to save project data to Django session
function saveProjectData(projectId) {
    console.log('[DEBUG] Saving project data for project ID:', projectId);

    // Show loading state
    showMessage('Saving project data...', 'info');

    // Collect form data
    const formData = getFormData();
    console.log('[DEBUG] Form data collected:', formData);

    // Check CSRF token
    const csrfToken = getCsrfToken();
    console.log('[DEBUG] CSRF Token:', csrfToken ? 'Found' : 'Not found');

    // Send data to server
    console.log('[DEBUG] Sending data to server...');
    fetch(`/api/projects/${projectId}/data/save/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        console.log('[DEBUG] Server response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('[DEBUG] Save response data:', data);

        if (data.success) {
            console.log('[DEBUG] Save successful');
            showMessage('Project data saved successfully', 'success');
            updateLastSavedStatus(new Date());
        } else {
            console.error('[DEBUG] Save failed:', data.error || 'Unknown error');
            showMessage('Error saving project data: ' + (data.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('[DEBUG] Error saving project data:', error);
        showMessage('Error saving project data: ' + error.message, 'error');
    });
}

// Function to load project data from Django session
function loadProjectData(projectId) {
    console.log('[DEBUG] Loading project data for project ID:', projectId);

    // Always clear form first to prevent mixing data
    clearForm();

    // Set the active project ID
    window.activeProjectId = projectId;
    console.log('[DEBUG] Active project ID set to:', window.activeProjectId);

    // Show loading state
    const dataStatus = document.getElementById('data-status');
    if (dataStatus) {
        dataStatus.classList.remove('hidden');
        document.getElementById('last-saved-text').textContent = 'Loading project data...';
        console.log('[DEBUG] Loading indicator shown');
    }

    // Load data from server
    console.log('[DEBUG] Requesting project data from server...');
    fetch(`/api/projects/${projectId}/data/load/`)
    .then(response => {
        console.log('[DEBUG] Load response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('[DEBUG] Load response data:', data);

        if (data.success) {
            if (data.has_data) {
                console.log('[DEBUG] Data found for project');

                // Populate form with data
                populateForm(data.data);

                // Show last saved time if available
                if (data.data.lastSaved) {
                    updateLastSavedStatus(new Date(data.data.lastSaved));
                    console.log('[DEBUG] Last saved timestamp updated');
                }
            } else {
                console.log('[DEBUG] No data found for project - creating new entry');

                // Create a new entry for this project
                createNewProjectEntry(projectId);
            }
        } else {
            console.error('[DEBUG] Load failed:', data.error || 'Unknown error');

            // Hide data status on error
            if (dataStatus) {
                dataStatus.classList.add('hidden');
            }
        }
    })
    .catch(error => {
        console.error('[DEBUG] Error loading project data:', error);
        showMessage('Error loading project data: ' + error.message, 'error');

        // Hide data status on error
        if (dataStatus) {
            dataStatus.classList.add('hidden');
        }
    });
}


// Function to load project data from database
function loadProjectData(projectId) {
    console.log('[DEBUG] Loading project data for project ID:', projectId);

    // STEP 1: Set the active project ID
    window.activeProjectId = projectId;
    console.log('[DEBUG] Active project ID set to:', window.activeProjectId);

    // STEP 2: Always clear form first to prevent mixing data
    console.log('[DEBUG] Clearing form before loading data');
    clearForm();

    // Show loading state
    const dataStatus = document.getElementById('data-status');
    if (dataStatus) {
        dataStatus.classList.remove('hidden');
        document.getElementById('last-saved-text').textContent = 'Loading project data...';
        console.log('[DEBUG] Loading indicator shown');
    }

    // STEP 3: Load data from server
    console.log('[DEBUG] Requesting project data from server...');
    fetch(`/api/projects/${projectId}/data/load/`)
    .then(response => {
        console.log('[DEBUG] Load response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('[DEBUG] Load response data:', data);

        if (data.success) {
            if (data.has_data) {
                console.log('[DEBUG] Data found for project');

                // Populate form with data
                populateForm(data.data);

                // Show last saved time if available
                if (data.data.lastSaved) {
                    updateLastSavedStatus(new Date(data.data.lastSaved));
                    console.log('[DEBUG] Last saved timestamp updated');
                }
            } else {
                console.log('[DEBUG] No data found for project - creating new entry');

                // Create a new entry for this project
                createNewProjectEntry(projectId);
            }
        } else {
            console.error('[DEBUG] Load failed:', data.error || 'Unknown error');

            // Hide data status on error
            if (dataStatus) {
                dataStatus.classList.add('hidden');
            }
        }
    })
    .catch(error => {
        console.error('[DEBUG] Error loading project data:', error);
        showMessage('Error loading project data: ' + error.message, 'error');

        // Hide data status on error
        if (dataStatus) {
            dataStatus.classList.add('hidden');
        }
    });
}

// Function to clear form data
function clearForm() {
    console.log('[DEBUG] Clearing form data');

    const formFields = [
        'report-date', 'project-name', 'project-owner', 'contractor',
        'visit-by', 'in-presence-of', 'visit-date', 'visit-number',
        'architect-file', 'distribution', 'project-description'
    ];

    // Clear all form fields
    formFields.forEach(fieldId => {
        const element = document.getElementById(fieldId);
        if (element) {
            element.value = '';
            console.log(`[DEBUG] Cleared field: ${fieldId}`);
        } else {
            console.error(`[DEBUG] Field not found: ${fieldId}`);
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
        console.log('[DEBUG] Image preview reset');
    }

    // Hide data status
    const dataStatus = document.getElementById('data-status');
    if (dataStatus) {
        dataStatus.classList.add('hidden');
        console.log('[DEBUG] Data status hidden');
    }
}

// Helper function to get all form data
function getFormData() {
    console.log('[DEBUG] Collecting form data');

    const formData = {
        reportDate: getElementValue('report-date'),
        projectName: getElementValue('project-name'),
        projectOwner: getElementValue('project-owner'),
        contractor: getElementValue('contractor'),
        visitBy: getElementValue('visit-by'),
        inPresenceOf: getElementValue('in-presence-of'),
        visitDate: getElementValue('visit-date'),
        visitNumber: getElementValue('visit-number'),
        architectFile: getElementValue('architect-file'),
        distribution: getElementValue('distribution'),
        description: getElementValue('project-description'),
        lastSaved: new Date().toISOString()
    };

    // Get image if exists
    const imagePreview = document.getElementById('project-image-preview');
    if (imagePreview) {
        const img = imagePreview.querySelector('img');
        if (img) {
            formData.imageUrl = img.src;
            console.log('[DEBUG] Image URL included in form data');
        }
    }

    return formData;
}

// Helper function to get element value with error checking
function getElementValue(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        return element.value;
    } else {
        console.error(`[DEBUG] Element not found: ${elementId}`);
        return '';
    }
}

// Helper function to populate form with data
function populateForm(data) {
    console.log('[DEBUG] Populating form with data:', Object.keys(data));

    // Set form field values if they exist in the data
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

    // Load image if saved
    if (data.imageUrl) {
        console.log('[DEBUG] Loading image from URL');
        const imagePreview = document.getElementById('project-image-preview');
        if (imagePreview) {
            // Clear previous content
            imagePreview.innerHTML = '';

            // Create and append image
            const img = document.createElement('img');
            img.src = data.imageUrl;
            img.className = 'w-full h-full object-cover';
            imagePreview.appendChild(img);
            console.log('[DEBUG] Image loaded into preview');
        }
    }

    // Show data status
    const dataStatus = document.getElementById('data-status');
    if (dataStatus) {
        dataStatus.classList.remove('hidden');
        console.log('[DEBUG] Data status shown');
    }
}

// Helper function to safely set form value
function trySetFormValue(elementId, value) {
    if (value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.value = value;
            console.log(`[DEBUG] Set ${elementId} to value of length ${value.length}`);
        } else {
            console.error(`[DEBUG] Element not found when setting value: ${elementId}`);
        }
    }
}

// Helper function to update last saved status
function updateLastSavedStatus(saveDate) {
    console.log('[DEBUG] Updating last saved status:', saveDate);

    const lastSavedText = document.getElementById('last-saved-text');
    if (lastSavedText) {
        const formattedDate = saveDate.toLocaleString();
        lastSavedText.textContent = `Last saved: ${formattedDate}`;
        console.log('[DEBUG] Last saved text updated to:', formattedDate);
    }

    // Show the data status container
    const dataStatus = document.getElementById('data-status');
    if (dataStatus) {
        dataStatus.classList.remove('hidden');
        console.log('[DEBUG] Data status shown');
    }
}

// Helper function to show messages
function showMessage(message, type = 'info') {
    console.log(`[DEBUG] [${type.toUpperCase()}] ${message}`);

    if (type === 'error') {
        alert(message);
    }
    // You could implement a more sophisticated message display system here
}

// Helper function to get CSRF token
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
        document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1] || '';
}

// Make functions available globally
window.projectForm = {
    loadProjectData,
    saveProjectData,
    clearForm,
    populateForm,
    createNewProjectEntry
};