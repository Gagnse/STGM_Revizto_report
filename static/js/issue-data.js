// Replace hardcoded status map with dynamic loading from API
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Issue data handler initialized');

    // Initialize global state
    window.issueData = {
        observations: [],
        instructions: [],
        deficiencies: [],
        projectStatuses: {}, // Store project-specific status information
        activeProjectId: null,
        history:{}
    };

    // Create default statusMap as a fallback
    window.statusMap = {
        // Standard statuses as fallback only
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

                        // *** IMPORTANT FIX: Add status to map by UUID ***
                        statusMap[status.uuid] = {
                            name: status.name,
                            displayName: mapStatusNameToFrench(status.name),
                            textColor: status.textColor,
                            backgroundColor: status.backgroundColor,
                            category: status.category
                        };
                    });

                    console.log('[DEBUG] Processed', Object.keys(statusMap).length, 'custom statuses');
                    console.log('[DEBUG] Status map keys:', Object.keys(statusMap));

                    // *** IMPORTANT FIX: Directly assign to window.statusMap ***
                    window.statusMap = statusMap;
                    console.log('[DEBUG] Updated window.statusMap directly with UUIDs');

                    // Also check if "En attente" is in the map
                    const enAttenteUuid = "c70f7d38-1d60-4df3-b85b-14e59174d7ba";
                    if (window.statusMap[enAttenteUuid]) {
                        console.log(`[DEBUG] Verified "En attente" is in statusMap: ${window.statusMap[enAttenteUuid].displayName}`);
                    } else {
                        console.log(`[DEBUG] "En attente" is NOT in statusMap!`);
                    }
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
  console.log(`[DEBUG-STATUS] Getting status display for ID: ${statusId}`);

  // Default status if nothing else matches
  const defaultStatus = {
    name: "Unknown",
    displayName: "Inconnu",
    textColor: "#FFFFFF",
    backgroundColor: "#6F7E93"
  };

  // Check for UUID in custom status value format
  if (typeof statusId === 'object' && statusId !== null) {
    console.log('[DEBUG-STATUS] Status is an object:', statusId);

    // Handle the customStatus.value format seen in logs
    if (statusId.value) {
      console.log(`[DEBUG-STATUS] Using status.value: ${statusId.value}`);
      statusId = statusId.value;
    } else if (statusId.uuid) {
      console.log(`[DEBUG-STATUS] Using status.uuid: ${statusId.uuid}`);
      statusId = statusId.uuid;
    } else {
      console.log('[DEBUG-STATUS] Could not extract status ID from object');
      return defaultStatus;
    }
  }

  // Now statusId should be a string, look it up in our map
   if (typeof statusId === 'string' && statusDirectMap[statusId]) {
    console.log(`[DEBUG-STATUS] Found direct UUID match for ${statusId}: ${statusDirectMap[statusId].displayName}`);
    return statusDirectMap[statusId];
  }

  console.log('[DEBUG-STATUS] Status not found in map, checking for specific IDs');
  // Debug: print all status UUIDs to check
  console.log('[DEBUG-STATUS] All available status UUIDs:', Object.keys(window.statusMap).join(', '));

  // Specific check for the "En attente" UUID
  const enAttenteUuid = "c70f7d38-1d60-4df3-b85b-14e59174d7ba"; // From your data
  if (statusId === enAttenteUuid) {
    console.log('[DEBUG-STATUS] This is the "En attente" status but it was not found in the map');
  }

  // If still not found, try to match by lowercase string
  if (typeof statusId === 'string') {
    const statusLower = statusId.toLowerCase();
    console.log('[DEBUG-STATUS] Trying string match for:', statusLower);

    if (statusLower.includes('open')) {
      return window.statusMap['open'];
    } else if (statusLower.includes('progress')) {
      return window.statusMap['in_progress'];
    } else if (statusLower.includes('solved') || statusLower.includes('fixed')) {
      return window.statusMap['solved'];
    } else if (statusLower.includes('closed')) {
      return window.statusMap['closed'];
    } else if (statusLower.includes('attente')) {
      console.log('[DEBUG-STATUS] Found string match for "attente"');
      // Look for any status with "attente" in name
      for (const [uuid, status] of Object.entries(window.statusMap)) {
        if (status.name.toLowerCase().includes('attente') ||
            status.displayName.toLowerCase().includes('attente')) {
          console.log('[DEBUG-STATUS] Found "attente" status in map:', status);
          return status;
        }
      }
    }
  }

  console.log('[DEBUG-STATUS] No status match found, using default');
  return defaultStatus;
}

// Helper function to map status names to French
// Helper function to map status names to French
function mapStatusNameToFrench(statusName) {
    if (!statusName) return 'Inconnu';

    console.log(`[DEBUG-STATUS] Mapping status name to French: "${statusName}"`);
    const statusLower = statusName.toLowerCase();

    // Map by exact case-insensitive matching
    const statusMap = {
        'open': 'Ouvert',
        'opened': 'Ouvert',
        'closed': 'Fermé',
        'solved': 'Résolu',
        'in progress': 'En cours',
        'in_progress': 'En cours',
        'en attente': 'En attente',    // Already French
        'corrigé': 'Corrigé',          // Already French
        'non-problème': 'Non-problème' // Already French
    };

    // Check for direct mapping
    if (statusMap[statusLower]) {
        console.log(`[DEBUG-STATUS] Found direct mapping for "${statusName}": "${statusMap[statusLower]}"`);
        return statusMap[statusLower];
    }

    // If no mapping exists, preserve the original name
    console.log(`[DEBUG-STATUS] No mapping found for "${statusName}", using original`);
    return statusName;
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
    renderItemsWithPrioritizedImages(deficiencies, 'deficiencies-container', 'Déficience');
}

// Render items (observations, instructions) directly
function renderItemsDirectly(items, containerId, itemType) {
    renderItemsWithPrioritizedImages(items, containerId, itemType);
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
    })
};

function fetchIssueHistory(projectId, issueId) {
    console.log(`[DEBUG] Fetching history for issue ID: ${issueId} in project: ${projectId}`);

    const historyPanelId = `history-panel-${issueId}`;
    const historyPanel = document.getElementById(historyPanelId);

    if (!historyPanel) {
        console.error(`[DEBUG] History panel not found with ID: ${historyPanelId}`);
        return;
    }

    // Show loading state
    historyPanel.innerHTML = `
        <div class="p-3">
            <div class="flex items-center">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
                <span class="text-sm text-gray-500">Chargement de l'historique...</span>
            </div>
        </div>
    `;

    fetch(`/api/projects/${projectId}/issues/${issueId}/comments/`)
        .then(response => {
            console.log(`[DEBUG] Comment history response status for issue ${issueId}:`, response.status);
            return response.json();
        })
        .then(data => {
            console.log(`[DEBUG] Comment history data for issue ${issueId}:`, data);

            // Extract comments from the response
            let comments = [];

            // Check for data in the expected structure
            if (data && data.result === 0 && data.data) {
                if (Array.isArray(data.data)) {
                    comments = data.data;
                } else if (data.data.data && Array.isArray(data.data.data)) {
                    comments = data.data.data;
                }
                console.log(`[DEBUG] Found ${comments.length} comments for issue ${issueId}`);
            }

            if (!comments || comments.length === 0) {
                historyPanel.innerHTML = '<div class="p-3 text-sm text-gray-500">Aucun historique disponible.</div>';
                return;
            }

            // Store the comments in the global state for this specific issue
            if (!window.issueData.history) {
                window.issueData.history = {};
            }
            window.issueData.history[issueId] = comments;

            // Render the comments for this specific issue
            const html = renderCommentsHTML(comments);
            historyPanel.innerHTML = html;
        })
        .catch(error => {
            console.error(`[DEBUG] Error fetching comments for issue ${issueId}:`, error);
            historyPanel.innerHTML = '<div class="p-3 text-sm text-red-500">Erreur lors du chargement de l\'historique.</div>';
        });
}

function renderCommentsHTML(comments) {
    // Sort comments by date (newest first)
    comments.sort((a, b) => {
        const dateA = new Date(a.created || 0);
        const dateB = new Date(b.created || 0);
        return dateB - dateA;
    });

    let html = '<div class="space-y-3 p-3">';

    if (!comments || comments.length === 0) {
        html += '<div class="text-sm text-gray-500">Aucun historique disponible.</div>';
        html += '</div>';
        return html;
    }

    // Filter comments before displaying
    // Exclude ALL diff comments - this is the important change
    const filteredComments = comments.filter(comment => {
        // Exclude all comments with type 'diff'
        return comment.type !== 'diff';
    });

    // If we have no comments after filtering, show "No history" message
    if (filteredComments.length === 0) {
        html += '<div class="text-sm text-gray-500">Aucun historique disponible.</div>';
        html += '</div>';
        return html;
    }

    filteredComments.forEach(comment => {
        // Add separators between comments
        if (html.indexOf('border-l-2') > -1) {
            // Add a light separator line between comments
            html += `
                <div class="border-l-2 border-gray-200 pl-3">
                    <div class="flex justify-between items-center text-sm mb-1">
            `;
        } else {
            html += `
                <div class="border-l-2 border-gray-200 pl-3">
                    <div class="flex justify-between items-center text-sm mb-1">
            `;
        }

        // Get author info
        let authorName = 'Utilisateur inconnu';
        if (comment.author) {
            if (typeof comment.author === 'string') {
                authorName = comment.author;
            } else if (comment.author.firstname && comment.author.lastname) {
                authorName = `${comment.author.firstname} ${comment.author.lastname}`;
            } else if (comment.author.email) {
                authorName = comment.author.email;
            }
        }

        // Format date
        const created = comment.created ? new Date(comment.created).toLocaleString('fr-CA') : 'Date inconnue';

        // Author and date header
        html += `
                    <span class="font-medium">${authorName}</span>
                    <span class="text-gray-500">${created}</span>
                </div>
        `;

        // Handle different comment types (diff type is already filtered out)
        switch (comment.type) {
            case 'text':
                html += `<p class="text-gray-700 text-sm">${comment.text || ''}</p>`;
                break;
            case 'file':
                html += renderFileComment(comment);
                break;
            case 'markup':
                html += renderMarkupComment(comment);
                break;
            default:
                html += `<p class="text-gray-700 text-sm italic">Activité: ${comment.type || 'Action non spécifiée'}</p>`;
        }

        html += '</div>';
    });

    html += '</div>';
    return html;
}

function renderDiffComment(comment) {
    if (!comment.diff) return '<p class="text-gray-500 text-sm italic">Modification non spécifiée</p>';

    let html = '<div class="bg-gray-50 p-2 rounded-md text-sm">';

    // Only process the comment.diff properties we want to show
    if (comment.diff.customStatus) {
        const change = comment.diff.customStatus;
        const oldValue = change.old || '-';
        const newValue = change.new || '-';

        html += `
            <div class="mb-1">
                <span class="font-medium">État:</span> 
                <span class="text">${formatStatusValue(oldValue)}</span> → 
                <span class="text">${formatStatusValue(newValue)}</span>
            </div>
        `;
    }

    if (comment.diff.assignee) {
        const change = comment.diff.assignee;
        const oldValue = change.old || '-';
        const newValue = change.new || '-';

        html += `
            <div class="mb-1">
                <span class="font-medium">Assigné à:</span> 
                <span class="text">${oldValue}</span> → 
                <span class="text">${newValue}</span>
            </div>
        `;
    }

    html += '</div>';
    return html;
}

function renderFileComment(comment) {
if (!comment.filename) return '<p class="text-gray-500 text-sm italic">Fichier joint</p>';

// Check if it's an image
const isImage = comment.mimetype && comment.mimetype.startsWith('image/');

if (isImage && comment.preview && comment.preview.small) {
    return `
        <div>
            <p class="text-sm text-gray-700 mb-1">Fichier: ${comment.filename}</p>
            <img src="${comment.preview.small}" alt="${comment.filename}" class="border border-gray-200 rounded-md">
        </div>
    `;
} else {
    return `
        <div class="flex items-center">
            <svg class="w-4 h-4 text-gray-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <span class="text-gray-700 text-sm">${comment.filename}</span>
        </div>
    `;
}
}

function renderMarkupComment(comment) {
if (!comment.preview || !comment.preview.small) return '<p class="text-gray-500 text-sm italic">Markup ajouté</p>';

return `
    <div>
        <p class="text-sm text-gray-700 mb-1">Markup ajouté</p>
        <img src="${comment.preview.small}" alt="Markup" class="border border-gray-200 rounded-md">
    </div>
`;
}

function formatStatusValue(value) {
// Try to map status UUIDs to display names if available
if (window.statusMap && window.statusMap[value]) {
    return window.statusMap[value].displayName || window.statusMap[value].name;
}

// Basic status translations
if (typeof value === 'string') {
    if (value.toLowerCase() === 'open') return 'Ouvert';
    if (value.toLowerCase() === 'solved') return 'Résolu';
    if (value.toLowerCase() === 'closed') return 'Fermé';
    if (value.toLowerCase() === 'in_progress') return 'En cours';
}

return value;
}

/**
 * Gets the best available image for an issue based on priority:
 * 1. Last uploaded image from comments
 * 2. Last markup image
 * 3. Default image from issue data
 *
 * @param {Object} item - The issue object
 * @param {Array} comments - Comments for this issue
 * @returns {string} - URL of the best available image or empty string if none found
 */
function getBestImageForIssue(item, comments) {
    console.log(`[DEBUG] Finding best image for issue ${item.id}`);

    // First check if we have comments
    if (comments && Array.isArray(comments) && comments.length > 0) {
        console.log(`[DEBUG] Checking ${comments.length} comments for images`);

        // First priority: Find the most recent file comment with an image
        // Sort comments newest first
        const sortedComments = [...comments].sort((a, b) => {
            const dateA = new Date(a.created || 0);
            const dateB = new Date(b.created || 0);
            return dateB - dateA;
        });

        // Look for a file comment with an image preview
        const fileComment = sortedComments.find(comment =>
            comment.type === 'file' &&
            comment.mimetype &&
            comment.mimetype.startsWith('image/') &&
            comment.preview &&
            (comment.preview.original || comment.preview.middle)
        );

        if (fileComment) {
            const imageUrl = fileComment.preview.original || fileComment.preview.middle;
            console.log(`[DEBUG] Found image in file comment: ${imageUrl}`);
            return imageUrl;
        }

        // Second priority: Find the most recent markup with a preview
        const markupComment = sortedComments.find(comment =>
            comment.type === 'markup' &&
            comment.preview &&
            (comment.preview.original || comment.preview.middle)
        );

        if (markupComment) {
            const imageUrl = markupComment.preview.original || markupComment.preview.middle;
            console.log(`[DEBUG] Found image in markup comment: ${imageUrl}`);
            return imageUrl;
        }
    }

    // Third priority: Use the default issue preview image
    if (item.preview) {
        if (typeof item.preview === 'string') {
            console.log(`[DEBUG] Using issue's string preview: ${item.preview}`);
            return item.preview;
        } else if (item.preview.original) {
            console.log(`[DEBUG] Using issue's preview.original: ${item.preview.original}`);
            return item.preview.original;
        } else if (item.preview.middle) {
            console.log(`[DEBUG] Using issue's preview.middle: ${item.preview.middle}`);
            return item.preview.middle;
        }
    }

    // No image found
    console.log(`[DEBUG] No image found for issue ${item.id}`);
    return '';
}

// Modified function to render items with enhanced image prioritization
function renderItemsWithPrioritizedImages(items, containerId, itemType) {
    console.log(`[DEBUG] Rendering ${items.length} ${itemType.toLowerCase()}s with prioritized images`);

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

    // First pass to generate the basic structure without images
    // This allows us to start fetching histories immediately
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

        // Get additional information
        const createdDate = getFormattedCreationDate(item);
        const sheetNumber = getSheetNumber(item);
        const sheetName = getSheetName(item);
        const reviztoLinks = getReviztoLinks(item);

        // Build the HTML for this item - initially with placeholder for image
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
                <div class="pt-4 pb-4 pl-4">
                    <div class="flex flex-col md:flex-row">
                        <div class="max-w-75 md:w-1/4 mb-4 md:mb-0 md:pr-4">
                            <div id="image-container-${id}" class="w-full bg-gray-100 rounded-md flex items-center justify-center overflow-hidden" style="min-height: 150px; max-height: 280px;">
                                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="w-full flex flex-col md:flex-row">
                            <!-- Left column: Issue information -->
                            <div class="w-full md:w-1/2 pr-4 space-y-3">
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
                            <div class="w-full md:w-1/2 mt-4 md:mt-0 border-t md:border-t-0 md:border-l border-gray-200 md:pl-4 md:pr-4 pt-4 md:pt-0">
                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Historique</h4>
                                <div id="history-panel-${id}" class="bg-gray-50 rounded-md">
                                    <div class="p-3 text-sm text-gray-500">Chargement de l'historique...</div>
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
    console.log(`[DEBUG] Rendered ${filteredItems.length} ${itemType.toLowerCase()} cards with placeholders`);

    // Fetch history for each issue and update images once history is loaded
    filteredItems.forEach(item => {
        fetchIssueHistoryAndUpdateImage(window.issueData.activeProjectId, item);
    });
}

/**
 * Fetch issue history and update the image when history is available
 */
function fetchIssueHistoryAndUpdateImage(projectId, issue) {
    console.log(`[DEBUG] Fetching history for issue ID: ${issue.id} in project: ${projectId}`);

    const historyPanelId = `history-panel-${issue.id}`;
    const historyPanel = document.getElementById(historyPanelId);
    const imageContainerId = `image-container-${issue.id}`;
    const imageContainer = document.getElementById(imageContainerId);

    if (!historyPanel) {
        console.error(`[DEBUG] History panel not found with ID: ${historyPanelId}`);
        return;
    }

    if (!imageContainer) {
        console.error(`[DEBUG] Image container not found with ID: ${imageContainerId}`);
        return;
    }

    // Show loading state
    historyPanel.innerHTML = `
        <div class="p-3">
            <div class="flex items-center">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
                <span class="text-sm text-gray-500">Chargement de l'historique...</span>
            </div>
        </div>
    `;

    fetch(`/api/projects/${projectId}/issues/${issue.id}/comments/`)
        .then(response => {
            console.log(`[DEBUG] Comment history response status for issue ${issue.id}:`, response.status);
            return response.json();
        })
        .then(data => {
            console.log(`[DEBUG] Comment history data for issue ${issue.id}:`, data);

            // Extract comments from the response
            let comments = [];

            // Check for data in the expected structure
            if (data && data.result === 0 && data.data) {
                if (Array.isArray(data.data)) {
                    comments = data.data;
                } else if (data.data.data && Array.isArray(data.data.data)) {
                    comments = data.data.data;
                }
                console.log(`[DEBUG] Found ${comments.length} comments for issue ${issue.id}`);
            }

            // Store the comments in the global state for this specific issue
            if (!window.issueData.history) {
                window.issueData.history = {};
            }
            window.issueData.history[issue.id] = comments;

            // Find the best image based on priority
            const bestImageUrl = getBestImageForIssue(issue, comments);

            // Update the image in the container
            if (bestImageUrl) {
                imageContainer.innerHTML = `
                    <img src="${bestImageUrl}" alt="Issue preview" class="w-full h-auto object-contain">
                `;
            }

            // Render the comments for this specific issue
            const html = renderCommentsHTML(comments);
            historyPanel.innerHTML = html;
        })
        .catch(error => {
            console.error(`[DEBUG] Error fetching comments for issue ${issue.id}:`, error);
            historyPanel.innerHTML = '<div class="p-3 text-sm text-red-500">Erreur lors du chargement de l\'historique.</div>';

            // Even if history fetch fails, we still try to set default image
            const defaultImageUrl = getDefaultImageUrl(issue);
            if (defaultImageUrl) {
                imageContainer.innerHTML = `
                    <img src="${defaultImageUrl}" alt="Issue preview" class="w-full h-auto object-contain">
                `;
            }
        });
}

/**
 * Get default image URL from issue object
 */
function getDefaultImageUrl(item) {
    if (item.preview) {
        if (typeof item.preview === 'string') {
            return item.preview;
        } else if (item.preview.original) {
            return item.preview.original;
        } else if (item.preview.middle) {
            return item.preview.middle;
        }
    }
    return '';
}

