// Improved issue-data.js focusing only on the essential parts that need fixing

// Fetch deficiencies from the API
function fetchDeficiencies(projectId) {
    console.log('[DEBUG] Fetching deficiencies for project ID:', projectId);

    // Show loading indicators
    showLoadingState('deficiencies');

    fetch(`/api/projects/${projectId}/deficiencies/`)
        .then(response => {
            console.log('[DEBUG] Deficiencies response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('[DEBUG] Received deficiencies data with keys:', Object.keys(data));

            // Find the deficiencies in the response structure
            let deficiencies = [];

            if (data.result === 0 && data.data && data.data.data) {
                deficiencies = data.data.data;
                console.log('[DEBUG] Found', deficiencies.length, 'deficiencies in data.data.data');
            } else if (data.deficiencies && Array.isArray(data.deficiencies)) {
                deficiencies = data.deficiencies;
                console.log('[DEBUG] Found', deficiencies.length, 'deficiencies in data.deficiencies');
            }

            // Log the first deficiency if available
            if (deficiencies.length > 0) {
                console.log('[DEBUG] First deficiency ID:', deficiencies[0].id);
            }

            window.issueData.deficiencies = deficiencies;
            renderDeficiencies(deficiencies);
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching deficiencies:', error);
            showError('deficiencies');
        });
}

// Render deficiencies in the UI
function renderDeficiencies(deficiencies) {
    console.log('[DEBUG] Rendering', deficiencies.length, 'deficiencies');
    const container = document.getElementById('deficiencies-container');

    if (!container) {
        console.error('[DEBUG] Deficiencies container not found in DOM');
        return;
    }

    if (deficiencies.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune déficience trouvée</p>';
        return;
    }

    // Create HTML for deficiencies
    let html = '';
    deficiencies.forEach(deficiency => {
        html += createDeficiencyCard(deficiency);
    });

    container.innerHTML = html;
    console.log('[DEBUG] Deficiency cards rendered successfully');
}

// Create HTML for a deficiency card
function createDeficiencyCard(deficiency) {
    // Extract data with fallbacks
    const id = deficiency.id || '';

    // Get title (could be string or object with value property)
    let title = 'Sans titre';
    if (deficiency.title) {
        if (typeof deficiency.title === 'string') {
            title = deficiency.title;
        } else if (deficiency.title.value) {
            title = deficiency.title.value;
        }
    }

    // Get status (could be string or object with value property)
    let status = 'unknown';
    if (deficiency.status) {
        if (typeof deficiency.status === 'string') {
            status = deficiency.status;
        } else if (deficiency.status.value) {
            status = deficiency.status.value;
        }
    }

    // Get sheet info
    let sheetNumber = '';
    let sheetName = '';
    if (deficiency.sheet) {
        if (typeof deficiency.sheet === 'object' && !Array.isArray(deficiency.sheet)) {
            // Direct sheet object
            sheetNumber = deficiency.sheet.number || '';
            sheetName = deficiency.sheet.name || '';
        } else if (deficiency.sheet.value && typeof deficiency.sheet.value === 'object') {
            // Sheet in value property
            sheetNumber = deficiency.sheet.value.number || '';
            sheetName = deficiency.sheet.value.name || '';
        }
    }

    // Get preview image
    let previewUrl = '';
    if (deficiency.preview && deficiency.preview.small) {
        previewUrl = deficiency.preview.small;
    }

    // Determine status color
    let statusColor = 'bg-gray-100 text-gray-800';
    if (status.toLowerCase() === 'open') {
        statusColor = 'bg-yellow-100 text-yellow-800';
    } else if (status.toLowerCase() === 'closed') {
        statusColor = 'bg-green-100 text-green-800';
    } else if (status.toLowerCase() === 'in_progress') {
        statusColor = 'bg-blue-100 text-blue-800';
    }

    // Create card HTML
    return `
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
            <!-- Card Header -->
            <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-semibold text-gray-800">Déficience #${id}</h3>
                    <span class="px-2 py-1 rounded-full text-xs ${statusColor}">${status}</span>
                </div>
            </div>
            
            <!-- Card Body -->
            <div class="p-4">
                <div class="flex flex-col md:flex-row">
                    <!-- Section 1: Image -->
                    <div class="w-full md:w-1/3 mb-4 md:mb-0 md:pr-4">
                        ${previewUrl ? 
                            `<img src="${previewUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">` : 
                            `<div class="w-full h-40 bg-gray-100 rounded-md flex items-center justify-center">
                                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>`
                        }
                    </div>
                    
                    <!-- Section 2: Details -->
                    <div class="w-full md:w-2/3">
                        <div class="space-y-2">
                            <div>
                                <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                <p class="text-gray-800">${title}</p>
                            </div>
                            
                            ${(sheetNumber || sheetName) ? 
                                `<div>
                                    <h4 class="text-sm font-medium text-gray-500">Feuille</h4>
                                    <p class="text-gray-800">${sheetNumber ? `${sheetNumber} - ` : ''}${sheetName}</p>
                                </div>` : ''
                            }
                            
                            <div>
                                <h4 class="text-sm font-medium text-gray-500">État</h4>
                                <p class="text-gray-800">${status}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Section 3: History -->
            <div class="px-4 py-3 bg-gray-50 border-t border-gray-200">
                <h4 class="text-sm font-medium text-gray-500 mb-2">Historique</h4>
                <p class="text-gray-600 text-sm italic">L'historique sera affiché ici ultérieurement.</p>
            </div>
        </div>
    `;
}

// Show loading state
function showLoadingState(section) {
    const container = document.getElementById(`${section}-container`);
    if (container) {
        container.innerHTML = `
            <div class="flex justify-center items-center p-4">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span class="ml-2 text-gray-600">Chargement en cours...</span>
            </div>
        `;
    }
}

// Show error state
function showError(section) {
    const container = document.getElementById(`${section}-container`);
    if (container) {
        container.innerHTML = `
            <div class="p-4 text-red-600">
                <p>Erreur lors du chargement des données.</p>
            </div>
        `;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Issue data handler initialized');

    // Initialize global state
    window.issueData = {
        observations: [],
        instructions: [],
        deficiencies: []
    };

    // Listen for project selection
    document.addEventListener('projectSelected', function(e) {
        const projectId = e.detail.projectId;
        console.log('[DEBUG] Project selected event received for ID:', projectId);

        if (projectId) {
            // For now, let's focus only on deficiencies
            fetchDeficiencies(projectId);
        }
    });

    // For direct debugging
    window.issueDataHandler = {
        fetchDeficiencies,
        manualFetchDeficiencies: function(projectId) {
            if (!projectId) {
                console.error('[DEBUG] No project ID provided for manual fetch');
                return;
            }
            console.log('[DEBUG] Manual fetch initiated for project ID:', projectId);
            fetchDeficiencies(projectId);
        }
    };
});