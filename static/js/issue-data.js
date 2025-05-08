// Optimized issue data handler for observations, instructions, and deficiencies

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
            console.log('[DEBUG] Fetching all issue data for project ID:', projectId);
            fetchObservations(projectId);
            fetchInstructions(projectId);
            fetchDeficiencies(projectId);
        }
    });

    // For direct debugging
    window.issueDataHandler = {
        fetchObservations,
        fetchInstructions,
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

// Fetch observations from the API
function fetchObservations(projectId) {
    console.log('[DEBUG] Fetching observations for project ID:', projectId);
    showLoadingState('observations');

    fetch(`/api/projects/${projectId}/observations/`)
        .then(response => {
            console.log('[DEBUG] Observations response status:', response.status);
            return response.json();
        })
        .then(data => {
            // Extract observations from the correct nested structure
            let observations = [];
            if (data && data.result === 0 && data.data && data.data.data) {
                observations = data.data.data;
                console.log('[DEBUG] Found', observations.length, 'observations in data.data.data');
            }

            window.issueData.observations = observations;
            renderItemsDirectly(observations, 'observations-container', 'Observation');
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching observations:', error);
            showError('observations');
        });
}

// Fetch instructions from the API
function fetchInstructions(projectId) {
    console.log('[DEBUG] Fetching instructions for project ID:', projectId);
    showLoadingState('instructions');

    fetch(`/api/projects/${projectId}/instructions/`)
        .then(response => {
            console.log('[DEBUG] Instructions response status:', response.status);
            return response.json();
        })
        .then(data => {
            // Extract instructions from the correct nested structure
            let instructions = [];
            if (data && data.result === 0 && data.data && data.data.data) {
                instructions = data.data.data;
                console.log('[DEBUG] Found', instructions.length, 'instructions in data.data.data');
            }

            window.issueData.instructions = instructions;
            renderItemsDirectly(instructions, 'instructions-container', 'Instruction');
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching instructions:', error);
            showError('instructions');
        });
}

// Fetch deficiencies from the API
function fetchDeficiencies(projectId) {
    console.log('[DEBUG] Fetching deficiencies for project ID:', projectId);
    showLoadingState('deficiencies');

    fetch(`/api/projects/${projectId}/deficiencies/`)
        .then(response => {
            console.log('[DEBUG] Deficiencies response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('[DEBUG] Received deficiencies data with keys:', Object.keys(data));

            // Extract deficiencies from the nested data structure
            let deficiencies = [];
            if (data && data.result === 0 && data.data && data.data.data) {
                deficiencies = data.data.data;
                console.log('[DEBUG] Found', deficiencies.length, 'deficiencies in data.data.data');
            }

            // Store in global state
            window.issueData.deficiencies = deficiencies;

            // Render deficiencies
            renderDeficienciesDirectly(deficiencies);
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching deficiencies:', error);
            showError('deficiencies');
        });
}

// Render deficiencies directly
function renderDeficienciesDirectly(deficiencies) {
    console.log('[DEBUG] Direct rendering of', deficiencies.length, 'deficiencies');
    const container = document.getElementById('deficiencies-container');

    if (!container) {
        console.error('[DEBUG] Deficiencies container not found');
        return;
    }

    if (!deficiencies || deficiencies.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune déficience trouvée</p>';
        return;
    }

    // Create HTML for all deficiencies
    let html = '';

    deficiencies.forEach(deficiency => {
        // Extract basic properties safely
        const id = deficiency.id || 'N/A';

        // Get title - could be string or object with value property
        let title = 'Sans titre';
        if (deficiency.title) {
            if (typeof deficiency.title === 'string') {
                title = deficiency.title;
            } else if (deficiency.title.value) {
                title = deficiency.title.value;
            }
        }

        // Get status - could be string or object with value property
        let status = 'Unknown';
        if (deficiency.status) {
            if (typeof deficiency.status === 'string') {
                status = deficiency.status;
            } else if (deficiency.status.value) {
                status = deficiency.status.value;
            }
        }

        // Get preview image URL if exists
        let imageUrl = '';
        if (deficiency.preview) {
            if (typeof deficiency.preview === 'string') {
                imageUrl = deficiency.preview;
            } else if (deficiency.preview.original) {
                imageUrl = deficiency.preview.original;
            }
        }

        // Translate status to French and determine status color
        let statusColor = 'bg-gray-100 text-gray-800';
        let frenchStatus = 'Inconnu';
        const statusLower = String(status).toLowerCase();

        if (statusLower === 'open' || statusLower === 'opened') {
            statusColor = 'bg-red-100 text-red-800'; // Changed from yellow to red
            frenchStatus = 'Ouvert';
        } else if (statusLower === 'closed' || statusLower === 'solved') {
            statusColor = 'bg-green-100 text-green-800'; // Kept green for solved
            frenchStatus = 'Résolu';
        } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
            statusColor = 'bg-orange-100 text-orange-800'; // Changed from blue to orange
            frenchStatus = 'En cours';
        }

        // Build the HTML for this deficiency
        html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-2 overflow-hidden">
                <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-800">#${id}</h3>
                        <span class="px-2 py-1 rounded-full text-xs ${statusColor}">${frenchStatus}</span>
                    </div>
                </div>
                <div class="p-4">
                    <div class="flex flex-col md:flex-row">
                        ${imageUrl ? 
                            `<div class="max-w-200 md:w-1/3 mb-4 md:mb-0 md:pr-4">
                                <img src="${imageUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">
                            </div>` : 
                            `<div class="w-full md:w-1/3 mb-4 md:mb-0 md:pr-4">
                                <div class="w-full h-40 bg-gray-100 rounded-md flex items-center justify-center">
                                    <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                            </div>`
                        }
                        <div class="w-full ${imageUrl ? 'md:w-2/3' : ''}">
                            <div class="space-y-2">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                    <p class="text-gray-800">${title}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">État</h4>
                                    <p class="text-gray-800">${frenchStatus}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    // Set the HTML to the container
    container.innerHTML = html;
    console.log('[DEBUG] Rendered', deficiencies.length, 'deficiency cards');
}

// Render items (observations, instructions) directly
function renderItemsDirectly(items, containerId, itemType) {
    console.log(`[DEBUG] Direct rendering of ${items.length} ${itemType.toLowerCase()}s`);
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`[DEBUG] ${itemType} container not found`);
        return;
    }

    if (!items || items.length === 0) {
        container.innerHTML = `<p class="text-yellow-700">Aucun(e) ${itemType.toLowerCase()} trouvé(e)</p>`;
        return;
    }

    // Create HTML for all items
    let html = '';

    items.forEach(item => {
        // Extract basic properties safely
        const id = item.id || 'N/A';

        // Get title - could be string or object with value property
        let title = 'Sans titre';
        if (item.title) {
            if (typeof item.title === 'string') {
                title = item.title;
            } else if (item.title.value) {
                title = item.title.value;
            }
        }

        // Get status - could be string or object with value property
        let status = 'Unknown';
        if (item.status) {
            if (typeof item.status === 'string') {
                status = item.status;
            } else if (item.status.value) {
                status = item.status.value;
            }
        }

        // Get preview image URL if exists
        let imageUrl = '';
        if (item.preview) {
            if (typeof item.preview === 'string') {
                imageUrl = item.preview;
            } else if (item.preview.original) {
                imageUrl = item.preview.original;
            }
        }

        // Translate status to French and determine status color
        let statusColor = 'bg-gray-100 text-gray-800';
        let frenchStatus = 'Inconnu';
        const statusLower = String(status).toLowerCase();

        if (statusLower === 'open' || statusLower === 'opened') {
            statusColor = 'bg-red-100 text-red-800'; // Changed from yellow to red
            frenchStatus = 'Ouvert';
        } else if (statusLower === 'closed' || statusLower === 'solved') {
            statusColor = 'bg-green-100 text-green-800'; // Kept green for solved
            frenchStatus = 'Résolu';
        } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
            statusColor = 'bg-orange-100 text-orange-800'; // Changed from blue to orange
            frenchStatus = 'En cours';
        }

        // Build the HTML for this item
        html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-1 overflow-hidden">
                <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-800">#${id}</h3>
                        <span class="px-2 py-1 rounded-full text-xs ${statusColor}">${frenchStatus}</span>
                    </div>
                </div>
                <div class="p-4">
                    <div class="flex flex-col md:flex-row">
                        ${imageUrl ? 
                            `<div class="max-w-200 md:w-1/3 mb-4 md:mb-0 md:pr-4">
                                <img src="${imageUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">
                            </div>` : 
                            `<div class="w-full md:w-1/3 mb-4 md:mb-0 md:pr-4">
                                <div class="w-full h-40 bg-gray-100 rounded-md flex items-center justify-center">
                                    <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                            </div>`
                        }
                        <div class="w-full ${imageUrl ? 'md:w-2/3' : ''}">
                            <div class="space-y-2">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                    <p class="text-gray-800">${title}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">État</h4>
                                    <p class="text-gray-800">${frenchStatus}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    // Set the HTML to the container
    container.innerHTML = html;
    console.log(`[DEBUG] Rendered ${items.length} ${itemType.toLowerCase()} cards`);
}

// Show loading state
function showLoadingState(section) {
    console.log('[DEBUG] Showing loading state for', section);
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
    console.log('[DEBUG] Showing error state for', section);
    const container = document.getElementById(`${section}-container`);
    if (container) {
        container.innerHTML = `
            <div class="p-4 text-red-600">
                <p>Erreur lors du chargement des données.</p>
            </div>
        `;
    }
}

// Manual testing function
window.forceLoadDeficiencies = function(projectId) {
    projectId = projectId || window.activeProjectId;
    if (!projectId) {
        console.error('[DEBUG] No project ID available for manual fetch');
        return;
    }

    console.log('[DEBUG] Forcing deficiency load for project:', projectId);
    fetchDeficiencies(projectId);
};