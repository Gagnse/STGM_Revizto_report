// Enhanced version of status-map-enhancer.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('[STATUS-FIX] Status mapping fixer initialized');

    // Initialize the UUID-based status map
    window.statusUUIDMap = {};

    // Enhance the getStatusDisplay function first
    const enhanceGetStatusDisplay = function() {
        // Store the original function if it exists
        const originalGetStatusDisplay = window.getStatusDisplay;

        // Create enhanced version
        window.getStatusDisplay = function(statusId) {
            console.log(`[STATUS-FIX] getStatusDisplay called with:`, statusId);

            // Default status as fallback
            const defaultStatus = {
                name: "Unknown",
                displayName: "Inconnu",
                textColor: "#FFFFFF",
                backgroundColor: "#6F7E93"
            };

            // Extract UUID from object if needed
            let statusUuid = null;

            if (typeof statusId === 'object' && statusId !== null) {
                console.log('[STATUS-FIX] Status is an object:', JSON.stringify(statusId));

                // Handle various object structures
                if (statusId.value) {
                    statusUuid = statusId.value;
                    console.log(`[STATUS-FIX] Extracted UUID from status.value: ${statusUuid}`);
                } else if (statusId.uuid) {
                    statusUuid = statusId.uuid;
                    console.log(`[STATUS-FIX] Extracted UUID from status.uuid: ${statusUuid}`);
                } else if (statusId.customStatus) {
                    if (typeof statusId.customStatus === 'string') {
                        statusUuid = statusId.customStatus;
                        console.log(`[STATUS-FIX] Extracted UUID from customStatus string: ${statusUuid}`);
                    } else if (typeof statusId.customStatus === 'object' && statusId.customStatus.value) {
                        statusUuid = statusId.customStatus.value;
                        console.log(`[STATUS-FIX] Extracted UUID from customStatus.value: ${statusUuid}`);
                    }
                } else if (statusId.status) {
                    if (typeof statusId.status === 'string') {
                        statusUuid = statusId.status;
                        console.log(`[STATUS-FIX] Extracted UUID from status string: ${statusUuid}`);
                    } else if (typeof statusId.status === 'object' && statusId.status.value) {
                        statusUuid = statusId.status.value;
                        console.log(`[STATUS-FIX] Extracted UUID from status.value: ${statusUuid}`);
                    }
                }
            } else if (typeof statusId === 'string') {
                // If it's already a string, assume it's a UUID
                statusUuid = statusId;
                console.log(`[STATUS-FIX] Status is already a string UUID: ${statusUuid}`);
            }

            // Look up the status in our UUID map
            if (statusUuid && window.statusUUIDMap && window.statusUUIDMap[statusUuid]) {
                console.log(`[STATUS-FIX] Found status in UUID map: ${window.statusUUIDMap[statusUuid].displayName}`);
                return window.statusUUIDMap[statusUuid];
            }

            // If not found in UUID map, log it
            console.log(`[STATUS-FIX] Status UUID ${statusUuid} not found in map`);

            // Return default
            return defaultStatus;
        };

        console.log('[STATUS-FIX] getStatusDisplay function enhanced');
    };

    // Enhance the fetchProjectStatuses function
    const enhanceFetchProjectStatuses = function() {
        // Store the original function
        const originalFetchProjectStatuses = window.issueDataHandler.fetchProjectStatuses;

        // Create enhanced version
        window.issueDataHandler.fetchProjectStatuses = function(projectId) {
            console.log('[STATUS-FIX] Enhanced fetchProjectStatuses for project ID:', projectId);

            return fetch(`/api/projects/${projectId}/workflow-settings/`)
                .then(response => {
                    console.log('[STATUS-FIX] Workflow settings response status:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('[STATUS-FIX] Received workflow settings with result:', data.result);

                    // Process status information from API
                    if (data && data.result === 0 && data.data) {
                        // Process statuses from the response
                        if (data.data.statuses && Array.isArray(data.data.statuses)) {
                            const statuses = data.data.statuses;
                            console.log(`[STATUS-FIX] Processing ${statuses.length} statuses from API`);

                            // Clear the status UUID map before populating
                            window.statusUUIDMap = {};

                            // Process each status and add it to the status map by UUID
                            statuses.forEach(status => {
                                const uuid = status.uuid;
                                if (!uuid) return;

                                window.statusUUIDMap[uuid] = {
                                    name: status.name,
                                    displayName: mapStatusNameToFrench(status.name), // Will map to French if needed
                                    textColor: status.textColor || "#FFFFFF",
                                    backgroundColor: status.backgroundColor || "#6F7E93",
                                    category: status.category || ""
                                };

                                console.log(`[STATUS-FIX] Added status to UUID map: ${status.name} (${uuid})`);
                            });

                            console.log(`[STATUS-FIX] statusUUIDMap now has ${Object.keys(window.statusUUIDMap).length} entries`);

                            // Also update window.statusMap for compatibility
                            if (window.statusMap) {
                                // Add entries to statusMap by UUID
                                Object.keys(window.statusUUIDMap).forEach(uuid => {
                                    window.statusMap[uuid] = window.statusUUIDMap[uuid];
                                });

                                console.log(`[STATUS-FIX] Updated statusMap with ${Object.keys(window.statusUUIDMap).length} entries`);
                            }

                            // Refresh current issue display to apply new status mappings
                            if (window.issueData) {
                                // Trigger re-rendering to apply new status mappings
                                setTimeout(() => {
                                    tryRefreshDisplays(projectId);
                                }, 500);
                            }
                        }
                    }

                    // Continue with original processing
                    return data;
                })
                .catch(error => {
                    console.error('[STATUS-FIX] Error fetching workflow settings:', error);
                    // Continue with the original function for fallback
                    return originalFetchProjectStatuses(projectId);
                });
        };

        console.log('[STATUS-FIX] fetchProjectStatuses enhanced successfully');
    };

    // Helper function for mapping status names to French
    function mapStatusNameToFrench(statusName) {
        if (!statusName) return 'Inconnu';

        const statusLower = statusName.toLowerCase();

        // Map common English status names to French
        const statusMap = {
            'open': 'Ouvert',
            'opened': 'Ouvert',
            'closed': 'Fermé',
            'solved': 'Résolu',
            'in progress': 'En cours',
            'in_progress': 'En cours'
        };

        // Check for direct mapping
        if (statusMap[statusLower]) {
            return statusMap[statusLower];
        }

        // For statuses already in French, keep them as is
        if (statusLower.includes('attente') ||
            statusLower.includes('corrigé') ||
            statusLower.includes('fermé') ||
            statusLower.includes('ouvert') ||
            statusLower.includes('résolu') ||
            statusLower.includes('cours') ||
            statusLower.includes('problème')) {
            return statusName;
        }

        // If no mapping exists, preserve the original name
        return statusName;
    }

    // Try to refresh current displays if issues are already loaded
    function tryRefreshDisplays(projectId) {
        console.log('[STATUS-FIX] Attempting to refresh displays with new status mappings');

        if (window.issueData) {
            // Access the existing data
            const { observations, instructions, deficiencies } = window.issueData;

            // If there's data and render functions are available, re-render
            if (observations && observations.length > 0 && typeof window.renderItemsDirectly === 'function') {
                console.log('[STATUS-FIX] Re-rendering observations with updated status mappings');
                window.renderItemsDirectly(observations, 'observations-container', 'Observation');
            }

            if (instructions && instructions.length > 0 && typeof window.renderItemsDirectly === 'function') {
                console.log('[STATUS-FIX] Re-rendering instructions with updated status mappings');
                window.renderItemsDirectly(instructions, 'instructions-container', 'Instruction');
            }

            if (deficiencies && deficiencies.length > 0 && typeof window.renderDeficienciesDirectly === 'function') {
                console.log('[STATUS-FIX] Re-rendering deficiencies with updated status mappings');
                window.renderDeficienciesDirectly(deficiencies);
            }
        }
    }

    // Wait a moment to ensure all scripts are loaded
    setTimeout(function() {
        // Apply enhancements
        if (window.issueDataHandler && typeof window.issueDataHandler.fetchProjectStatuses === 'function') {
            enhanceFetchProjectStatuses();
            enhanceGetStatusDisplay();
            console.log('[STATUS-FIX] Status handling enhanced successfully');
        } else {
            console.warn('[STATUS-FIX] issueDataHandler not found, will retry...');

            // Try again in 1 second
            setTimeout(function() {
                if (window.issueDataHandler && typeof window.issueDataHandler.fetchProjectStatuses === 'function') {
                    enhanceFetchProjectStatuses();
                    enhanceGetStatusDisplay();
                    console.log('[STATUS-FIX] Status handling enhanced successfully on retry');
                } else {
                    console.error('[STATUS-FIX] issueDataHandler still not available, could not enhance status handling');
                }
            }, 1000);
        }
    }, 300);
});