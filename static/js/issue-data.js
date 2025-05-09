
// Hard-coded status map based on the JSON example
window.statusMap = {
  // Standard statuses
  "2ed005c6-43cd-4907-a4d6-807dbd0197d5": {
    name: "Open",
    displayName: "Ouvert",
    textColor: "#FFFFFF",
    backgroundColor: "#CC2929"
  },
  "cd52ac3e-f345-4f99-870f-5be95dc33245": {
    name: "In progress",
    displayName: "En cours",
    textColor: "#FFFFFF",
    backgroundColor: "#FFAA00"
  },
  "b8504242-3489-43a2-9831-54f64053b226": {
    name: "Solved",
    displayName: "Résolu",
    textColor: "#FFFFFF",
    backgroundColor: "#42BE65"
  },
  "135b58c6-1e14-4716-a134-bbba2bbc90a7": {
    name: "Closed",
    displayName: "Fermé",
    textColor: "#FFFFFF",
    backgroundColor: "#B8B8B8"
  },
  // Custom statuses
  "5947b7d1-70b9-425b-aba6-7187eb0251ff": {
    name: "En attente",
    displayName: "En attente",
    textColor: "#FFFFFF",
    backgroundColor: "#FFD32E"
  },
  "912abbbf-3155-4e3c-b437-5778bdfd73f4": {
    name: "non-problème",
    displayName: "Non-problème",
    textColor: "#FFFFFF",
    backgroundColor: "#2B2B2B"
  },
  "337e2fe6-e2a3-4e3f-b098-30aac68a191c": {
    name: "Corrigé",
    displayName: "Corrigé",
    textColor: "#FFFFFF",
    backgroundColor: "#892EFB"
  },
  // String-based fallbacks
  "open": {
    name: "Open",
    displayName: "Ouvert",
    textColor: "#FFFFFF",
    backgroundColor: "#CC2929"
  },
  "in_progress": {
    name: "In progress",
    displayName: "En cours",
    textColor: "#FFFFFF",
    backgroundColor: "#FFAA00"
  },
  "solved": {
    name: "Solved",
    displayName: "Résolu",
    textColor: "#FFFFFF",
    backgroundColor: "#42BE65"
  },
  "closed": {
    name: "Closed",
    displayName: "Fermé",
    textColor: "#FFFFFF",
    backgroundColor: "#B8B8B8"
  }
};

// Enhanced issue data handler with custom status support
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Issue data handler initialized');

    // Initialize global state
    window.issueData = {
        observations: [],
        instructions: [],
        deficiencies: [],
        projectStatuses: {}, // Store project-specific status information
        activeProjectId: null
    };

    // Listen for project selection
    document.addEventListener('projectSelected', function(e) {
        const projectId = e.detail.projectId;
        console.log('[DEBUG] Project selected event received for ID:', projectId);

        if (projectId) {
            window.issueData.activeProjectId = projectId;

            // First fetch custom statuses, then fetch issues
            fetchProjectStatuses(projectId).then(() => {
                // After statuses are loaded, fetch issues
                console.log('[DEBUG] Fetching all issue data for project ID:', projectId);
                fetchObservations(projectId);
                fetchInstructions(projectId);
                fetchDeficiencies(projectId);
            }).catch(error => {
                console.error('[DEBUG] Error fetching project statuses:', error);
                // Still try to fetch issues even if statuses fail
                fetchObservations(projectId);
                fetchInstructions(projectId);
                fetchDeficiencies(projectId);
            });
        }
    });

    // For direct debugging
    window.issueDataHandler = {
        fetchObservations,
        fetchInstructions,
        fetchDeficiencies,
        fetchProjectStatuses,
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

// Fetch project workflow settings including custom statuses
function fetchProjectStatuses(projectId) {
    console.log('[DEBUG] Fetching workflow settings for project ID:', projectId);

    return fetch(`/api/projects/${projectId}/workflow-settings/`)
        .then(response => {
            console.log('[DEBUG] Workflow settings response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('[DEBUG] Received workflow settings with result:', data.result);
            console.log('[DEBUG] Workflow data keys:', data.data ? Object.keys(data.data) : 'No data property');

            // Process and store status information
            if (data && data.result === 0 && data.data) {
                // Store all statuses in a map for easy lookup
                const statusMap = {};

                // Process statuses from the response
                if (data.data.statuses && Array.isArray(data.data.statuses)) {
                    console.log('[DEBUG] Found', data.data.statuses.length, 'statuses in response');

                    data.data.statuses.forEach(status => {
                        console.log(`[DEBUG] Processing status: ${status.name} (UUID: ${status.uuid})`);

                        statusMap[status.uuid] = {
                            name: status.name,
                            textColor: status.textColor,
                            backgroundColor: status.backgroundColor,
                            category: status.category
                        };
                    });

                    console.log('[DEBUG] Processed', Object.keys(statusMap).length, 'custom statuses');
                    console.log('[DEBUG] Status map keys:', Object.keys(statusMap));
                } else {
                    console.warn('[DEBUG] No statuses array found in data or it is not an array');
                    console.log('[DEBUG] Data structure:', JSON.stringify(data.data).substring(0, 200) + '...');
                }

                // Store in global state
                window.issueData.projectStatuses = statusMap;
                return statusMap;
            } else {
                console.warn('[DEBUG] Invalid workflow settings data format:', data);
                return {};
            }
        })
        .catch(error => {
            console.error('[DEBUG] Error fetching workflow settings:', error);
            return {};
        });
}

// Get status display information based on status UUID
function getStatusDisplay(statusId) {
  console.log(`[DEBUG] Getting status display for ID: ${statusId}`);

  // Default status if nothing else matches
  const defaultStatus = {
    name: "Unknown",
    displayName: "Inconnu",
    textColor: "#FFFFFF",
    backgroundColor: "#6F7E93"
  };

  // Check for UUID in custom status value format
  if (typeof statusId === 'object' && statusId !== null) {
    console.log('[DEBUG] Status is an object:', statusId);

    // Handle the customStatus.value format seen in logs
    if (statusId.value) {
      console.log(`[DEBUG] Using status.value: ${statusId.value}`);
      statusId = statusId.value;
    } else if (statusId.uuid) {
      console.log(`[DEBUG] Using status.uuid: ${statusId.uuid}`);
      statusId = statusId.uuid;
    } else {
      console.log('[DEBUG] Could not extract status ID from object');
      return defaultStatus;
    }
  }

  // Now statusId should be a string, look it up in our map
  if (statusId && window.statusMap[statusId]) {
    console.log(`[DEBUG] Found status in map: ${window.statusMap[statusId].displayName}`);
    return window.statusMap[statusId];
  }

  // If still not found, try to match by lowercase string
  if (typeof statusId === 'string') {
    const statusLower = statusId.toLowerCase();

    if (statusLower.includes('open')) {
      return window.statusMap['open'];
    } else if (statusLower.includes('progress')) {
      return window.statusMap['in_progress'];
    } else if (statusLower.includes('solved') || statusLower.includes('fixed')) {
      return window.statusMap['solved'];
    } else if (statusLower.includes('closed')) {
      return window.statusMap['closed'];
    }
  }

  console.log('[DEBUG] No status match found, using default');
  return defaultStatus;
}

// Helper function to map status names to French
function mapStatusNameToFrench(statusName) {
    if (!statusName) return 'Inconnu';

    const statusLower = statusName.toLowerCase();

    if (statusLower === 'open' || statusLower === 'opened') {
        return 'Ouvert';
    } else if (statusLower === 'closed') {
        return 'Fermé';
    } else if (statusLower === 'solved') {
        return 'Résolu';
    } else if (statusLower === 'in progress' || statusLower === 'in_progress') {
        return 'En cours';
    } else if (statusLower === 'en attente') {
        return 'En attente';
    } else if (statusLower === 'corrigé') {
        return 'Corrigé';
    } else if (statusLower === 'non-problème') {
        return 'Non-problème';
    } else {
        // If no mapping exists, use the original name
        return statusName;
    }
}

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
    // Filter out closed issues
    const filteredDeficiencies = filterOutClosedIssues(deficiencies);
    console.log('[DEBUG] After filtering closed issues:', filteredDeficiencies.length, 'deficiencies remain');

    const container = document.getElementById('deficiencies-container');

    if (!container) {
        console.error('[DEBUG] Deficiencies container not found');
        return;
    }

    if (!filteredDeficiencies || filteredDeficiencies.length === 0) {
        container.innerHTML = '<p class="text-yellow-700">Aucune déficience trouvée</p>';
        return;
    }

    // Create HTML for all deficiencies
    let html = '';

    filteredDeficiencies.forEach(deficiency => {
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

        // Get status - check for both status and customStatus
        let statusId = null;
        if (deficiency.customStatus) {
            statusId = deficiency.customStatus;
        } else if (deficiency.status) {
            statusId = deficiency.status;
        }

        // Get status display information
        const statusDisplay = getStatusDisplay(statusId);

        // Get preview image URL if exists
        let imageUrl = '';
        if (deficiency.preview) {
            if (typeof deficiency.preview === 'string') {
                imageUrl = deficiency.preview;
            } else if (deficiency.preview.original) {
                imageUrl = deficiency.preview.original;
            }
        }

        // Build the HTML for this deficiency
        html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-2 overflow-hidden">
                <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-800">#${id}</h3>
                        <span class="px-5 py-1.5 rounded-full font-bold text-sm" 
                            style="background-color: ${statusDisplay.backgroundColor}; color: ${statusDisplay.textColor}">
                            ${statusDisplay.displayName}
                        </span>
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
                                    <p class="text-gray-800">${statusDisplay.displayName}</p>
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
    console.log('[DEBUG] Rendered', filteredDeficiencies.length, 'deficiency cards');
}

// Render items (observations, instructions) directly
function renderItemsDirectly(items, containerId, itemType) {
    console.log(`[DEBUG] Direct rendering of ${items.length} ${itemType.toLowerCase()}s`);
    // Filter out closed issues
    const filteredItems = filterOutClosedIssues(items);
    console.log(`[DEBUG] After filtering closed issues: ${filteredItems.length} ${itemType.toLowerCase()}s remain`);

    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`[DEBUG] ${itemType} container not found`);
        return;
    }

    if (!filteredItems || filteredItems.length === 0) {
        container.innerHTML = `<p class="text-yellow-700">Aucun(e) ${itemType.toLowerCase()} trouvé(e)</p>`;
        return;
    }

    // Create HTML for all items
    let html = '';

    filteredItems.forEach(item => {
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

        // Get status - check for both status and customStatus
        let statusId = null;
        if (item.customStatus) {
            statusId = item.customStatus;
        } else if (item.status) {
            statusId = item.status;
        }

        // Get status display information
        const statusDisplay = getStatusDisplay(statusId);

        // Get preview image URL if exists
        let imageUrl = '';
        if (item.preview) {
            if (typeof item.preview === 'string') {
                imageUrl = item.preview;
            } else if (item.preview.original) {
                imageUrl = item.preview.original;
            }
        }

        // Build the HTML for this item
        html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-1 overflow-hidden">
                <div class="bg-gray-50 px-4 py-2 border-b border-gray-200">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-800">#${id}</h3>
                        <span class="px-5 py-1.5 rounded-full font-bold text-sm" 
                            style="background-color: ${statusDisplay.backgroundColor}; color: ${statusDisplay.textColor}">
                            ${statusDisplay.displayName}
                        </span>
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
                                    <p class="text-gray-800">${statusDisplay.displayName}</p>
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
    console.log(`[DEBUG] Rendered ${filteredItems.length} ${itemType.toLowerCase()} cards`);
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
    projectId = projectId || window.activeProjectId || window.issueData.activeProjectId;
    if (!projectId) {
        console.error('[DEBUG] No project ID available for manual fetch');
        return;
    }

    console.log('[DEBUG] Forcing deficiency load for project:', projectId);
    fetchDeficiencies(projectId);
};

// Helper function to filter out closed issues
function filterOutClosedIssues(issues) {
    return issues.filter(issue => {
        // Get status - could be string, object with value property, or UUID
        let status = '';

        // First check for customStatus
        if (issue.customStatus) {
            if (typeof issue.customStatus === 'string') {
                status = issue.customStatus;
            } else if (issue.customStatus.value) {
                status = issue.customStatus.value;
            }
        }
        // If no customStatus or couldn't extract it, check regular status
        else if (issue.status) {
            if (typeof issue.status === 'string') {
                status = issue.status;
            } else if (issue.status.value) {
                status = issue.status.value;
            } else if (issue.status.uuid) {
                status = issue.status.uuid;
            }
        }

        // Check if this is a "closed" status
        // 1. Direct match with closed UUID
        if (status === "135b58c6-1e14-4716-a134-bbba2bbc90a7") {
            return false;
        }

        // 2. String comparison for status name
        if (typeof status === 'string' && status.toLowerCase().includes('closed')) {
            return false;
        }

        // 3. Check in statusMap if available
        if (window.statusMap && window.statusMap[status]) {
            const statusInfo = window.statusMap[status];
            if (statusInfo.name && statusInfo.name.toLowerCase() === 'closed') {
                return false;
            }
        }

        // Include issue if not closed
        return true;
    });
}