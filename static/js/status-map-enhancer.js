// status-map-enhancer.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('[STATUS-ENHANCER] Status map enhancer initialized');

    // Hard-coded direct mapping of status UUIDs to display info
    // This serves as a reliable fallback for known status UUIDs
    window.statusDirectMap = {
        // Open status
        "2ed005c6-43cd-4907-a4d6-807dbd0197d5": {
            name: "Open",
            displayName: "Ouvert",
            textColor: "#FFFFFF",
            backgroundColor: "#CC2929"
        },
        // In progress status
        "cd52ac3e-f345-4f99-870f-5be95dc33245": {
            name: "In progress",
            displayName: "En cours",
            textColor: "#FFFFFF",
            backgroundColor: "#FFAA00"
        },
        // Solved status
        "b8504242-3489-43a2-9831-54f64053b226": {
            name: "Solved",
            displayName: "Résolu",
            textColor: "#FFFFFF",
            backgroundColor: "#42BE65"
        },
        // Closed status
        "135b58c6-1e14-4716-a134-bbba2bbc90a7": {
            name: "Closed",
            displayName: "Fermé",
            textColor: "#FFFFFF",
            backgroundColor: "#B8B8B8"
        },
        // En attente status (from paste.txt)
        "c70f7d38-1d60-4df3-b85b-14e59174d7ba": {
            name: "En attente",
            displayName: "En attente",
            textColor: "#FFFFFF",
            backgroundColor: "#FFD32E"
        },
        // non-problème status (from paste.txt)
        "fc0cfae9-b820-47cc-9f43-eb06fb69dcfc": {
            name: "non-problème",
            displayName: "Non-problème",
            textColor: "#FFFFFF",
            backgroundColor: "#2B2B2B"
        },
        // Corrigé status (from paste.txt)
        "877b09d5-ccc4-4ba5-8f8b-e5f0b8f80f6a": {
            name: "Corrigé",
            displayName: "Corrigé",
            textColor: "#FFFFFF",
            backgroundColor: "#892EFB"
        }
    };

    // Wait until issue-data.js has loaded
    setTimeout(function() {
        // Create original getStatusDisplay reference if it exists
        let originalGetStatusDisplay = null;
        if (typeof window.getStatusDisplay === 'function') {
            originalGetStatusDisplay = window.getStatusDisplay;
        }

        // Enhanced version of getStatusDisplay
        window.getStatusDisplay = function(statusId) {
            console.log('[STATUS-ENHANCER] Enhanced getStatusDisplay called with:', statusId);

            // Default status if nothing else matches
            const defaultStatus = {
                name: "Unknown",
                displayName: "Inconnu",
                textColor: "#FFFFFF",
                backgroundColor: "#6F7E93"
            };

            // Extract the status UUID or identifier from different formats
            let statusValue = null;

            if (typeof statusId === 'object' && statusId !== null) {
                console.log('[STATUS-ENHANCER] Status is an object:', statusId);

                // Handle customStatus from deficiencies
                if (statusId.customStatus) {
                    if (typeof statusId.customStatus === 'string') {
                        statusValue = statusId.customStatus;
                    } else if (typeof statusId.customStatus === 'object' && statusId.customStatus.value) {
                        statusValue = statusId.customStatus.value;
                    }
                }
                // Handle standard status property
                else if (statusId.status) {
                    if (typeof statusId.status === 'string') {
                        statusValue = statusId.status;
                    } else if (typeof statusId.status === 'object' && statusId.status.value) {
                        statusValue = statusId.status.value;
                    }
                }
                // Handle direct value or uuid property
                else if (statusId.value) {
                    statusValue = statusId.value;
                } else if (statusId.uuid) {
                    statusValue = statusId.uuid;
                }

                if (statusValue) {
                    console.log('[STATUS-ENHANCER] Extracted status value:', statusValue);
                }
            } else if (typeof statusId === 'string') {
                // If it's already a string, use it directly
                statusValue = statusId;
                console.log('[STATUS-ENHANCER] Status is already a string:', statusValue);
            }

            // If we've extracted a status value, try to look it up
            if (statusValue) {
                // First check our direct map for standard UUIDs
                if (window.statusDirectMap && window.statusDirectMap[statusValue]) {
                    console.log('[STATUS-ENHANCER] Found in direct map:', window.statusDirectMap[statusValue].displayName);
                    return window.statusDirectMap[statusValue];
                }

                // Then check window.statusMap
                if (window.statusMap && window.statusMap[statusValue]) {
                    console.log('[STATUS-ENHANCER] Found in window.statusMap:', window.statusMap[statusValue].displayName);
                    return window.statusMap[statusValue];
                }

                // If it's a string but not a UUID, try name matching
                if (typeof statusValue === 'string' && statusValue.length < 36) {
                    const lowerValue = statusValue.toLowerCase();

                    // Keyword matching for standard statuses
                    if (lowerValue.includes('open')) {
                        console.log('[STATUS-ENHANCER] Matched by "open" keyword');
                        return window.statusDirectMap["2ed005c6-43cd-4907-a4d6-807dbd0197d5"];
                    } else if (lowerValue.includes('progress')) {
                        console.log('[STATUS-ENHANCER] Matched by "progress" keyword');
                        return window.statusDirectMap["cd52ac3e-f345-4f99-870f-5be95dc33245"];
                    } else if (lowerValue.includes('solv')) {
                        console.log('[STATUS-ENHANCER] Matched by "solved" keyword');
                        return window.statusDirectMap["b8504242-3489-43a2-9831-54f64053b226"];
                    } else if (lowerValue.includes('closed')) {
                        console.log('[STATUS-ENHANCER] Matched by "closed" keyword');
                        return window.statusDirectMap["135b58c6-1e14-4716-a134-bbba2bbc90a7"];
                    } else if (lowerValue.includes('attente')) {
                        console.log('[STATUS-ENHANCER] Matched by "attente" keyword');
                        return window.statusDirectMap["c70f7d38-1d60-4df3-b85b-14e59174d7ba"];
                    } else if (lowerValue.includes('corrigé')) {
                        console.log('[STATUS-ENHANCER] Matched by "corrigé" keyword');
                        return window.statusDirectMap["877b09d5-ccc4-4ba5-8f8b-e5f0b8f80f6a"];
                    } else if (lowerValue.includes('problème') || lowerValue.includes('probleme')) {
                        console.log('[STATUS-ENHANCER] Matched by "problème" keyword');
                        return window.statusDirectMap["fc0cfae9-b820-47cc-9f43-eb06fb69dcfc"];
                    }
                }
            }

            // If we still have no match but the original function exists, try it as fallback
            if (originalGetStatusDisplay) {
                const result = originalGetStatusDisplay(statusId);
                if (result && result.displayName !== "Inconnu") {
                    return result;
                }
            }

            // No match found, return default
            console.log('[STATUS-ENHANCER] No match found, returning default status');
            return defaultStatus;
        };

        console.log('[STATUS-ENHANCER] Successfully enhanced getStatusDisplay function');
    }, 1000); // Wait for issue-data.js to initialize
});