// Simple and direct solution for deficiencies display

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
            // Extract observations from the response structure
            let observations = [];

            if (data && data.result === 0 && data.data && data.data.data) {
                observations = data.data.data;
            }

            window.issueData.observations = observations;
            console.log('[DEBUG] Received observations data:', observations.length, 'items');
            renderObservations(observations);
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
            // Extract instructions from the response structure
            let instructions = [];

            if (data && data.result === 0 && data.data && data.data.data) {
                instructions = data.data.data;
            }

            window.issueData.instructions = instructions;
            console.log('[DEBUG] Received instructions data:', instructions.length, 'items');
            renderInstructions(instructions);
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching instructions:', error);
            showError('instructions');
        });
}

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

            // Find the deficiencies in the nested structure
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

// Force render deficiencies with a simpler approach
function forceRenderDeficiencies(deficiencies) {
    console.log('[DEBUG] Force rendering', deficiencies.length, 'deficiencies');
    const container = document.getElementById('deficiencies-container');

    if (!container) {
        console.error('[DEBUG] Deficiencies container not found in DOM');
        return;
    }

    if (!deficiencies || deficiencies.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune déficience trouvée</p>';
        return;
    }

    // Create HTML for deficiencies - SIMPLE VERSION
    let html = '';

    deficiencies.forEach(deficiency => {
        // Extract basic info safely
        const id = deficiency.id || 'N/A';

        // Get title - handle both string and object with value
        let title = 'Sans titre';
        if (deficiency.title) {
            if (typeof deficiency.title === 'string') {
                title = deficiency.title;
            } else if (deficiency.title.value) {
                title = deficiency.title.value;
            }
        }

        // Get status - handle both string and object with value
        let status = 'Unknown';
        if (deficiency.status) {
            if (typeof deficiency.status === 'string') {
                status = deficiency.status;
            } else if (deficiency.status.value) {
                status = deficiency.status.value;
            }
        }

        // Get image URL if exists
        let imageUrl = '';
        if (deficiency.preview) {
            if (typeof deficiency.preview === 'string') {
                imageUrl = deficiency.preview;
            } else if (deficiency.preview.small) {
                imageUrl = deficiency.preview.small;
            }
        }

        // Determine status color
        let statusColor = 'bg-gray-100 text-gray-800';
        const statusLower = String(status).toLowerCase();
        if (statusLower === 'open' || statusLower === 'opened') {
            statusColor = 'bg-yellow-100 text-yellow-800';
        } else if (statusLower === 'closed' || statusLower === 'solved') {
            statusColor = 'bg-green-100 text-green-800';
        } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
            statusColor = 'bg-blue-100 text-blue-800';
        }

        // Create a simple card
        html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
                <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-800">Déficience #${id}</h3>
                        <span class="px-2 py-1 rounded-full text-xs ${statusColor}">${status}</span>
                    </div>
                </div>
                <div class="p-4">
                    <div class="flex flex-col md:flex-row">
                        ${imageUrl ? 
                            `<div class="w-full md:w-1/3 mb-4 md:mb-0 md:pr-4">
                                <img src="${imageUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">
                            </div>` : ''
                        }
                        <div class="w-full ${imageUrl ? 'md:w-2/3' : ''}">
                            <div class="space-y-2">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                    <p class="text-gray-800">${title}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
    console.log('[DEBUG] Force-rendered', deficiencies.length, 'deficiency cards');
}

// Render observations in the UI
function renderObservations(observations) {
    console.log('[DEBUG] Rendering', observations.length, 'observations');
    const container = document.getElementById('observations-container');

    if (!container) {
        console.error('[DEBUG] Observations container not found in DOM');
        return;
    }

    if (!observations || observations.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune observation trouvée</p>';
        return;
    }

    // Create HTML for observations
    let html = '';
    observations.forEach(observation => {
        html += createIssueCard(observation, 'observation');
    });

    container.innerHTML = html;
    console.log('[DEBUG] Observation cards rendered successfully');
}

// Render instructions in the UI
function renderInstructions(instructions) {
    console.log('[DEBUG] Rendering', instructions.length, 'instructions');
    const container = document.getElementById('instructions-container');

    if (!container) {
        console.error('[DEBUG] Instructions container not found in DOM');
        return;
    }

    if (!instructions || instructions.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune instruction trouvée</p>';
        return;
    }

    // Create HTML for instructions
    let html = '';
    instructions.forEach(instruction => {
        html += createIssueCard(instruction, 'instruction');
    });

    container.innerHTML = html;
    console.log('[DEBUG] Instruction cards rendered successfully');
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

    // Create card HTML
    return `
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
            <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-semibold text-gray-800">Déficience #${id}</h3>
                    <span class="px-2 py-1 rounded-full text-xs bg-yellow-100 text-yellow-800">${status}</span>
                </div>
            </div>
            <div class="p-4">
                <div class="flex flex-col md:flex-row">
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
        </div>
    `;
}

// Create HTML for an issue card (observation, instruction, or deficiency)
function createIssueCard(issue, type) {
    // Extract ID
    const id = extractValue(issue, 'id', 'N/A');

    // Extract title
    let title = 'Sans titre';
    if (issue.title) {
        if (typeof issue.title === 'string') {
            title = issue.title;
        } else if (issue.title.value) {
            title = issue.title.value;
        }
    }

    // Extract status
    let status = 'Unknown';
    if (issue.status) {
        if (typeof issue.status === 'string') {
            status = issue.status;
        } else if (issue.status.value) {
            status = issue.status.value;
        }
    }

    // Extract sheet info
    let sheetNumber = '';
    let sheetName = '';
    if (issue.sheet) {
        if (typeof issue.sheet === 'object' && !Array.isArray(issue.sheet)) {
            if (issue.sheet.number) sheetNumber = issue.sheet.number;
            if (issue.sheet.name) sheetName = issue.sheet.name;
        } else if (issue.sheet.value && typeof issue.sheet.value === 'object') {
            if (issue.sheet.value.number) sheetNumber = issue.sheet.value.number;
            if (issue.sheet.value.name) sheetName = issue.sheet.value.name;
        }
    }

    // Extract preview image
    let previewUrl = '';
    if (issue.preview) {
        if (typeof issue.preview === 'string') {
            previewUrl = issue.preview;
        } else if (issue.preview.small) {
            previewUrl = issue.preview.small;
        } else if (issue.preview.value && issue.preview.value.small) {
            previewUrl = issue.preview.value.small;
        }
    }

    // Determine status color
    let statusColor = 'bg-gray-100 text-gray-800';
    const statusLower = String(status).toLowerCase();
    if (statusLower === 'open' || statusLower === 'opened') {
        statusColor = 'bg-yellow-100 text-yellow-800';
    } else if (statusLower === 'closed' || statusLower === 'solved') {
        statusColor = 'bg-green-100 text-green-800';
    } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
        statusColor = 'bg-blue-100 text-blue-800';
    }

    // Get type label in French
    let typeLabel = 'Item';
    if (type === 'observation') typeLabel = 'Observation';
    if (type === 'instruction') typeLabel = 'Instruction';
    if (type === 'deficiency') typeLabel = 'Déficience';

    // Create card HTML
    return `
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
            <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-semibold text-gray-800">${typeLabel} #${id}</h3>
                    <span class="px-2 py-1 rounded-full text-xs ${statusColor}">${status}</span>
                </div>
            </div>
            <div class="p-4">
                <div class="flex flex-col md:flex-row">
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
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Helper function to extract values safely
function extractValue(obj, key, defaultValue = '') {
    if (!obj) return defaultValue;

    if (obj[key] !== undefined) {
        if (typeof obj[key] === 'string' || typeof obj[key] === 'number') {
            return obj[key];
        } else if (obj[key] && obj[key].value !== undefined) {
            return obj[key].value;
        }
    }

    return defaultValue;
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

// Add this debugging function
window.forceLoadDeficiencies = function(projectId) {
    projectId = projectId || window.activeProjectId || 712062;

    console.log('[DEBUG] Forcing deficiency load for project:', projectId);

    fetch(`/api/projects/${projectId}/deficiencies/`)
        .then(response => response.text())
        .then(text => {
            try {
                const data = JSON.parse(text);
                console.log('[DEBUG] Raw response data:', data);

                if (data.result === 0 && data.data && data.data.data) {
                    const deficiencies = data.data.data;
                    console.log('[DEBUG] Found', deficiencies.length, 'deficiencies');

                    if (deficiencies.length > 0) {
                        forceRenderDeficiencies(deficiencies);
                        return 'Successfully rendered deficiencies';
                    }
                }

                return 'No deficiencies found in data';
            } catch (e) {
                console.error('[DEBUG] JSON parse error:', e);
                return 'Error parsing JSON';
            }
        })
        .catch(error => {
            console.error('[DEBUG] Fetch error:', error);
            return 'Fetch error';
        });
};