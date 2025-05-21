// status-fix.js
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[DEBUG-FIX] Pure dynamic status fix script loaded');

        // Wait a moment for issue-data.js to initialize first
        setTimeout(function() {
            // Keep track of loaded statuses
            window.loadedStatusUUIDs = [];

            // Enhance fetchProjectStatuses to properly build the status map
            const enhanceFetchProjectStatuses = function() {
                // Store the original function
                const originalFetchProjectStatuses = window.issueDataHandler.fetchProjectStatuses;

                // Create our enhanced version
                window.issueDataHandler.fetchProjectStatuses = function(projectId) {
                    console.log('[DEBUG-FIX] Enhanced fetchProjectStatuses for project ID:', projectId);

                    return fetch(`/api/projects/${projectId}/workflow-settings/`)
                        .then(response => response.json())
                        .then(data => {
                            if (data && data.result === 0 && data.data && data.data.statuses) {
                                // Create status map from the API response
                                const statuses = data.data.statuses;
                                console.log(`[DEBUG-FIX] Processing ${statuses.length} statuses from API`);

                                // Create an empty object if statusMap doesn't exist
                                if (!window.statusMap) {
                                    window.statusMap = {};
                                }

                                // Process each status and add it to the status map directly by UUID
                                statuses.forEach(status => {
                                    const uuid = status.uuid;
                                    if (!uuid) return;

                                    // Track this UUID as loaded
                                    window.loadedStatusUUIDs.push(uuid);

                                    // Add to the status map
                                    window.statusMap[uuid] = {
                                        name: status.name,
                                        displayName: status.name, // Will map to French if needed
                                        textColor: status.textColor || "#FFFFFF",
                                        backgroundColor: status.backgroundColor || "#6F7E93",
                                        category: status.category || ""
                                    };

                                    // Check if this is "En attente" status
                                    if (status.name === "En attente") {
                                        console.log(`[DEBUG-FIX] Found En attente status with UUID ${uuid} and color ${status.backgroundColor}`);
                                    }

                                    // Translate standard English status names to French display names
                                    if (status.name === "Open") {
                                        window.statusMap[uuid].displayName = "Ouvert";
                                    } else if (status.name === "In progress") {
                                        window.statusMap[uuid].displayName = "En cours";
                                    } else if (status.name === "Solved") {
                                        window.statusMap[uuid].displayName = "Résolu";
                                    } else if (status.name === "Closed") {
                                        window.statusMap[uuid].displayName = "Fermé";
                                    }
                                    // Other statuses like "En attente" keep their French names
                                });

                                console.log(`[DEBUG-FIX] statusMap now has ${Object.keys(window.statusMap).length} entries`);
                                console.log('[DEBUG-FIX] Status UUIDs loaded:', window.loadedStatusUUIDs);

                                // Also store in project statuses for reference
                                window.issueData.projectStatuses = window.statusMap;

                                // Return the data for continuation of the promise chain
                                return data;
                            }

                            return data;
                        })
                        .catch(error => {
                            console.error('[DEBUG-FIX] Error in enhanced fetchProjectStatuses:', error);
                            // Still call the original to maintain compatibility
                            return originalFetchProjectStatuses(projectId);
                        });
                };

                console.log('[DEBUG-FIX] fetchProjectStatuses enhanced successfully');
            };

            // Enhance getStatusDisplay to properly extract and use UUIDs
            const enhanceGetStatusDisplay = function() {
                // Replace the original function
                window.getStatusDisplay = function(statusId) {
                    console.log(`[DEBUG-FIX] Enhanced getStatusDisplay called for:`, statusId);

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
                        console.log('[DEBUG-FIX] Status is an object:', JSON.stringify(statusId));

                        // Handle various object structures we've seen
                        if (statusId.value) {
                            statusUuid = statusId.value;
                            console.log(`[DEBUG-FIX] Extracted UUID from status.value: ${statusUuid}`);
                        } else if (statusId.uuid) {
                            statusUuid = statusId.uuid;
                            console.log(`[DEBUG-FIX] Extracted UUID from status.uuid: ${statusUuid}`);
                        } else if (statusId.customStatus && typeof statusId.customStatus === 'object') {
                            // Try to extract from nested customStatus
                            if (statusId.customStatus.value) {
                                statusUuid = statusId.customStatus.value;
                                console.log(`[DEBUG-FIX] Extracted UUID from customStatus.value: ${statusUuid}`);
                            } else if (statusId.customStatus.uuid) {
                                statusUuid = statusId.customStatus.uuid;
                                console.log(`[DEBUG-FIX] Extracted UUID from customStatus.uuid: ${statusUuid}`);
                            }
                        }
                    } else if (typeof statusId === 'string') {
                        // If it's already a string, assume it's a UUID
                        statusUuid = statusId;
                        console.log(`[DEBUG-FIX] Status is already a string UUID: ${statusUuid}`);
                    }

                    // Now look up the status in our map
                    if (statusUuid && window.statusMap && window.statusMap[statusUuid]) {
                        console.log(`[DEBUG-FIX] Found status in map for UUID ${statusUuid}:`, window.statusMap[statusUuid]);
                        return window.statusMap[statusUuid];
                    }

                    // If we have loaded statuses but this one isn't in the map, log details
                    if (statusUuid && window.loadedStatusUUIDs && window.loadedStatusUUIDs.length > 0) {
                        console.log(`[DEBUG-FIX] Status UUID ${statusUuid} not found in loaded UUIDs:`, window.loadedStatusUUIDs);
                    }

                    // If we couldn't find by UUID, try name matching as fallback
                    if (window.statusMap && Object.keys(window.statusMap).length > 0) {
                        // Try to match by status name if we still have a string
                        if (typeof statusId === 'string') {
                            // Search through statusMap for a status with this name
                            for (const [uuid, status] of Object.entries(window.statusMap)) {
                                if (status.name === statusId || status.displayName === statusId) {
                                    console.log(`[DEBUG-FIX] Found status by name match: ${status.displayName}`);
                                    return status;
                                }
                            }

                            // Try partial matching in lowercase
                            const lowercaseQuery = statusId.toLowerCase();
                            for (const [uuid, status] of Object.entries(window.statusMap)) {
                                const name = status.name.toLowerCase();
                                const displayName = status.displayName.toLowerCase();

                                if (name.includes(lowercaseQuery) || displayName.includes(lowercaseQuery)) {
                                    console.log(`[DEBUG-FIX] Found status by partial name match: ${status.displayName}`);
                                    return status;
                                }

                                // Additional matching for keywords
                                if (lowercaseQuery.includes('attend') && name.includes('atten')) {
                                    console.log(`[DEBUG-FIX] Found status by 'attente' keyword match: ${status.displayName}`);
                                    return status;
                                }
                            }
                        }
                    }

                    console.log('[DEBUG-FIX] No status match found, returning default');
                    return defaultStatus;
                };

                console.log('[DEBUG-FIX] getStatusDisplay function enhanced successfully');
            };

            // Apply the enhancements
            if (window.issueDataHandler && typeof window.issueDataHandler.fetchProjectStatuses === 'function') {
                enhanceFetchProjectStatuses();
                enhanceGetStatusDisplay();
                console.log('[DEBUG-FIX] Status handling has been fully enhanced');

                // If there's already an active project, trigger a refresh
                if (window.issueData && window.issueData.activeProjectId) {
                    console.log('[DEBUG-FIX] Active project detected, refreshing status data');
                    window.issueDataHandler.fetchProjectStatuses(window.issueData.activeProjectId);
                }
            } else {
                console.error('[DEBUG-FIX] Could not enhance status handling - issueDataHandler not available');
            }
        }, 500); // Wait 500ms to ensure issue-data.js is loaded and initialized
    });
})();