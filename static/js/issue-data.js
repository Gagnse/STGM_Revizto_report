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

// Helper function to safely extract and format creation date
function getFormattedCreationDate(item) {
    if (!item.created) return 'N/A';

    let createdDate = '';
    if (typeof item.created === 'string') {
        createdDate = item.created;
    } else if (item.created.value) {
        createdDate = item.created.value;
    }

    // Try to format the date nicely
    if (createdDate) {
        try {
            const date = new Date(createdDate);
            return date.toLocaleString('fr-CA');
        } catch (e) {
            return createdDate;
        }
    }

    return 'N/A';
}

// Helper function to safely extract assignee
function getAssignee(item) {
    if (!item.assignee) return 'Non assignée';

    try {
        if (typeof item.assignee === 'string') {
            return item.assignee;
        } else if (item.assignee.value) {
            return item.assignee.value;
        }
    } catch (e) {
        console.error('[DEBUG] Error extracting assignee:', e);
    }

    return 'Non assignée';
}

// Helper function to safely extract sheet number
function getSheetNumber(item) {
    if (!item.sheet) return 'N/A';

    try {
        if (typeof item.sheet === 'object' && item.sheet.value && item.sheet.value.number) {
            return item.sheet.value.number;
        } else if (typeof item.sheet === 'string') {
            return item.sheet;
        }
    } catch (e) {
        console.error('[DEBUG] Error extracting sheet number:', e);
    }

    return 'N/A';
}

// Helper function to safely extract sheet name
function getSheetName(item) {
    if (!item.sheet) return 'N/A';

    try {
        if (typeof item.sheet === 'object' && item.sheet.value && item.sheet.value.name) {
            return item.sheet.value.name;
        }
    } catch (e) {
        console.error('[DEBUG] Error extracting sheet name:', e);
    }

    return 'N/A';
}

// Helper function to safely extract Revizto links
function getReviztoLinks(item) {
    const links = {
        desktop: null,
        web: null
    };

    if (!item.openLinks) return links;

    try {
        if (typeof item.openLinks === 'object') {
            if (item.openLinks.desktop) {
                links.desktop = item.openLinks.desktop;
            }
            if (item.openLinks.web) {
                links.web = item.openLinks.web;
            }
        }
    } catch (e) {
        console.error('[DEBUG] Error extracting Revizto links:', e);
    }

    return links;
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

        // Get additional information
        const createdDate = getFormattedCreationDate(deficiency);
        const sheetNumber = getSheetNumber(deficiency);
        const sheetName = getSheetName(deficiency);
        const reviztoLinks = getReviztoLinks(deficiency);

        // Build the HTML for this deficiency
         html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
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
                            `<div class="max-w-75 md:w-1/4 mb-4 md:mb-0 md:pr-4">
                                <img src="${imageUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">
                            </div>` : 
                            `<div class="max-w-75 md:w-1/4 mb-4 md:mb-0 md:pr-4">
                                <div class="w-full h-40 bg-gray-100 rounded-md flex items-center justify-center">
                                    <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                            </div>`
                        }
                        <div class="md:w-3/4 flex flex-col md:flex-row">
                            <!-- Left column: Issue information -->
                            <div class="md:w-1/2 pr-4 space-y-3">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                    <p class="text-gray-800">${title}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">État</h4>
                                    <p class="text-gray-800">${statusDisplay.displayName}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Posée le</h4>
                                    <p class="text-gray-800">${createdDate}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Assignée à</h4>
                                    <p class="text-gray-800">${getAssignee(deficiency)}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Numéro de la feuille</h4>
                                    <p class="text-gray-800">${sheetNumber}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Nom de la feuille</h4>
                                    <p class="text-gray-800">${sheetName}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Ouvrir dans Revizto</h4>
                                    <div class="flex gap-2">
                                        ${reviztoLinks.desktop ? 
                                            `<a href="${reviztoLinks.desktop}" class="text-blue-600 hover:underline" target="_blank">Application</a>` : 
                                            ''}
                                        ${reviztoLinks.web ? 
                                            `<a href="${reviztoLinks.web}" class="text-blue-600 hover:underline" target="_blank">Web</a>` : 
                                            ''}
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Right column: Issue history -->
                            <div class="md:w-1/2 mt-4 md:mt-0 border-t md:border-t-0 md:border-l border-gray-200 md:pl-4 pt-4 md:pt-0">
                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Historique</h4>
                                <div class="bg-gray-50 rounded-md p-3">
                                    <p class="text-gray-500 text-sm italic">L'historique des modifications sera affiché ici</p>
                                </div>
                            </div>
                        </div>
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

        // Get additional information
        const createdDate = getFormattedCreationDate(item);
        const sheetNumber = getSheetNumber(item);
        const sheetName = getSheetName(item);
        const reviztoLinks = getReviztoLinks(item);

        // Build the HTML for this item
         html += `
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
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
                            `<div class="max-w-200 md:w-1/4 mb-4 md:mb-0 md:pr-4">
                                <img src="${imageUrl}" alt="Preview" class="w-full h-auto rounded-md border border-gray-200">
                            </div>` : 
                            `<div class="max-w-200 md:w-1/4 mb-4 md:mb-0 md:pr-4">
                                <div class="w-full h-40 bg-gray-100 rounded-md flex items-center justify-center">
                                    <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                            </div>`
                        }
                        <div class="md:w-3/4 flex flex-col md:flex-row">
                            <!-- Left column: Issue information -->
                            <div class="md:w-1/2 pr-4 space-y-3">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Titre</h4>
                                    <p class="text-gray-800">${title}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">État</h4>
                                    <p class="text-gray-800">${statusDisplay.displayName}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Posée le</h4>
                                    <p class="text-gray-800">${createdDate}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Assignée à</h4>
                                    <p class="text-gray-800">${getAssignee(item)}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Numéro de la feuille</h4>
                                    <p class="text-gray-800">${sheetNumber}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Nom de la feuille</h4>
                                    <p class="text-gray-800">${sheetName}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-500">Ouvrir dans Revizto</h4>
                                    <div class="flex gap-2">
                                        ${reviztoLinks.desktop ? 
                                            `<a href="${reviztoLinks.desktop}" class="text-blue-600 hover:underline" target="_blank">Application</a>` : 
                                            ''}
                                        ${reviztoLinks.web ? 
                                            `<a href="${reviztoLinks.web}" class="text-blue-600 hover:underline" target="_blank">Web</a>` : 
                                            ''}
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Right column: Issue history -->
                            <div class="md:w-1/2 mt-4 md:mt-0 border-t md:border-t-0 md:border-l border-gray-200 md:pl-4 pt-4 md:pt-0">
                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Historique</h4>
                                <div class="bg-gray-50 rounded-md p-3">
                                    <p class="text-gray-500 text-sm italic">L'historique des modifications sera affiché ici</p>
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

function fetchIssueHistory(projectId, issueId) {
    console.log(`[DEBUG] Fetching history for issue ID: ${issueId} in project: ${projectId}`);

    // Show loading state in the history panel
    const historyPanel = document.querySelector(`.issue-card[data-issue-id="${issueId}"] .issue-history-panel`);
    if (historyPanel) {
        historyPanel.innerHTML = `
            <div class="flex justify-center items-center p-4">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span class="ml-2 text-gray-600">Chargement de l'historique...</span>
            </div>
        `;
    }

    fetch(`/api/projects/${projectId}/issues/${issueId}/comments/`)
        .then(response => {
            console.log('[DEBUG] Issue history response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('[DEBUG] Issue history response data:', data);

            // Extract comments from the response
            let comments = [];

            // Check if we have a proper response
            if (data && data.result === 0) {
                // The data could be directly in data property or nested
                if (Array.isArray(data.data)) {
                    comments = data.data;
                } else if (data.data && Array.isArray(data.data.items)) {
                    comments = data.data.items;
                }

                console.log(`[DEBUG] Found ${comments.length} comments for issue ${issueId}`);
            }

            // Store in global state
            window.issueData.history[issueId] = comments;

            // Render the history
            renderIssueHistory(issueId, comments);
        })
        .catch(error => {
            console.error(`[DEBUG] Error fetching history for issue ${issueId}:`, error);
            if (historyPanel) {
                historyPanel.innerHTML = `
                    <div class="p-4 text-red-600">
                        <p>Erreur lors du chargement de l'historique.</p>
                    </div>
                `;
            }
        });
}

function renderIssueHistory(issueId, comments) {
    console.log(`[DEBUG] Rendering history for issue ${issueId} with ${comments.length} comments`);

    const historyPanel = document.querySelector(`.issue-card[data-issue-id="${issueId}"] .issue-history-panel`);

    if (!historyPanel) {
        console.error(`[DEBUG] History panel not found for issue ${issueId}`);
        return;
    }

    if (!comments || comments.length === 0) {
        historyPanel.innerHTML = '<p class="p-4 text-gray-500">Aucun historique disponible.</p>';
        return;
    }

    // Sort comments by date (newest first)
    comments.sort((a, b) => {
        const dateA = new Date(a.date || a.created || 0);
        const dateB = new Date(b.date || b.created || 0);
        return dateB - dateA;
    });

    // Create timeline HTML
    let html = '<div class="p-4"><h4 class="text-lg font-medium mb-4">Historique</h4>';
    html += '<ul class="space-y-4">';

    comments.forEach(comment => {
        // Extract data from comment
        const author = comment.author ? comment.author.name || comment.author : 'Unknown';
        const timestamp = comment.date || comment.created || '';
        const formattedDate = formatDate(timestamp);
        let content = comment.text || comment.content || comment.message || 'No content';

        // Get action type if available
        let actionType = comment.type || comment.action || '';

        // Format different types of comments
        let actionClass = 'bg-gray-100';
        let actionIcon = '';

        if (actionType.toLowerCase().includes('status') || content.toLowerCase().includes('status')) {
            actionClass = 'bg-yellow-100';
            actionIcon = '<svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path></svg>';
        } else if (actionType.toLowerCase().includes('create') || content.toLowerCase().includes('created')) {
            actionClass = 'bg-green-100';
            actionIcon = '<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>';
        } else if (actionType.toLowerCase().includes('comment') || content.length > 30) {
            actionClass = 'bg-blue-100';
            actionIcon = '<svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>';
        }

        // Add to timeline
        html += `
            <li class="relative pl-6 border-l-2 border-gray-200">
                <div class="absolute -left-2 mt-1 w-4 h-4 rounded-full ${actionClass} flex items-center justify-center">
                    ${actionIcon}
                </div>
                <div class="bg-white rounded-lg border border-gray-200 p-3 shadow-sm">
                    <div class="flex justify-between items-center mb-1">
                        <span class="font-medium text-gray-900">${author}</span>
                        <span class="text-sm text-gray-500">${formattedDate}</span>
                    </div>
                    <p class="text-gray-700 whitespace-pre-line">${content}</p>
                </div>
            </li>
        `;
    });

    html += '</ul></div>';

    // Set the HTML
    historyPanel.innerHTML = html;
}

function formatDate(dateString) {
    if (!dateString) return '';

    try {
        const date = new Date(dateString);

        // Check if date is valid
        if (isNaN(date.getTime())) {
            return 'Date invalide';
        }

        // Format the date
        return date.toLocaleString('fr-CA', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        console.error('[DEBUG] Error formatting date:', error);
        return dateString;
    }
}