// Form data management - SIMPLIFIED VERSION
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Simple project form handler initialized');

    // Current active project ID
    window.activeProjectId = null;
    console.log('[DEBUG] Initial window.activeProjectId set to:', window.activeProjectId);

    // Initialize form handlers
    initSimpleFormHandlers();

    // Initialize image upload
    initSimpleImageUpload();
});

// Initialize form event handlers - SIMPLIFIED
function initSimpleFormHandlers() {
    // Save button handler
    const saveBtn = document.getElementById('save-project-info');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            console.log('[DEBUG] Save button clicked');

            if (!window.activeProjectId) {
                console.error('[DEBUG] No active project selected');
                if (window.Toast) {
                    Toast.error('Erreur', 'Veuillez sélectionner un projet d\'abord');
                } else {
                    alert('Veuillez sélectionner un projet d\'abord');
                }
                return;
            }

            saveProjectDataSimple(window.activeProjectId);
        });
    } else {
        console.error('[DEBUG] Save button not found in the DOM');
    }

    // Clear button handler - SIMPLIFIED
    const clearBtn = document.getElementById('clear-project-info');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            console.log('[DEBUG] Clear button clicked');

            if (!window.activeProjectId) {
                console.error('[DEBUG] No active project selected');
                if (window.Toast) {
                    Toast.error('Erreur', 'Veuillez sélectionner un projet d\'abord');
                } else {
                    alert('Veuillez sélectionner un projet d\'abord');
                }
                return;
            }

            // Simple browser confirmation
            if (confirm('Êtes-vous sûr de vouloir supprimer toutes les données du formulaire?')) {
                clearFormSimple();
            }
        });
    } else {
        console.error('[DEBUG] Clear button not found in the DOM');
    }
}

// Initialize image upload - SIMPLIFIED
function initSimpleImageUpload() {
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

                // Simple validation
                if (!file.type.startsWith('image/')) {
                    if (window.Toast) {
                        Toast.error('Format invalide', 'Veuillez sélectionner un fichier image valide');
                    } else {
                        alert('Veuillez sélectionner un fichier image valide');
                    }
                    return;
                }

                if (file.size > 5 * 1024 * 1024) { // 5MB limit
                    if (window.Toast) {
                        Toast.error('Fichier trop volumineux', 'La taille de l\'image ne doit pas dépasser 5MB');
                    } else {
                        alert('La taille de l\'image ne doit pas dépasser 5MB');
                    }
                    return;
                }

                let loadingToast = null;
                if (window.Toast) {
                    loadingToast = Toast.loading('Chargement', 'Traitement de l\'image...');
                }

                const reader = new FileReader();
                reader.onload = (e) => {
                    console.log('[DEBUG] File read successfully');

                    // Clear previous content
                    imagePreview.innerHTML = '';

                    // Create and append image
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'w-full h-full object-cover';
                    img.onload = () => {
                        if (loadingToast && window.Toast) {
                            Toast.hide(loadingToast);
                            Toast.success('Image chargée', 'L\'image a été chargée avec succès');
                        }
                    };
                    imagePreview.appendChild(img);

                    console.log('[DEBUG] Image preview updated');
                };

                reader.onerror = (e) => {
                    console.error('[DEBUG] Error reading file:', e);
                    if (loadingToast && window.Toast) {
                        Toast.hide(loadingToast);
                        Toast.error('Erreur de lecture', 'Impossible de lire le fichier image');
                    } else {
                        alert('Impossible de lire le fichier image');
                    }
                };

                reader.readAsDataURL(file);
                console.log('[DEBUG] Started reading file as Data URL');
            }
        });
    } else {
        console.error('[DEBUG] One or more image upload components not found');
    }
}

// Function to save project data - SIMPLIFIED
function saveProjectDataSimple(projectId) {
    console.log('[DEBUG] Saving project data for project ID:', projectId);

    // Show loading toast
    let loadingToast = null;
    if (window.Toast) {
        loadingToast = Toast.loading('Sauvegarde', 'Enregistrement des données du projet...');
    }

    // Collect form data safely
    const formData = getFormDataForSave();
    console.log('[DEBUG] Form data collected:', formData);

    // Check CSRF token
    const csrfToken = getCsrfTokenForSave();
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
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('[DEBUG] Save response data:', data);

        // Hide loading toast
        if (loadingToast && window.Toast) {
            Toast.hide(loadingToast);
        }

        if (data.success) {
            console.log('[DEBUG] Save successful');
            if (window.Toast) {
                Toast.success('Sauvegarde réussie', 'Les données du projet ont été enregistrées avec succès');
            }
            updateLastSavedStatusSimple(new Date());
        } else {
            console.error('[DEBUG] Save failed:', data.error || 'Unknown error');
            if (window.Toast) {
                Toast.error('Erreur de sauvegarde', data.error || 'Une erreur inconnue est survenue');
            } else {
                alert('Erreur de sauvegarde: ' + (data.error || 'Une erreur inconnue est survenue'));
            }
        }
    })
    .catch(error => {
        console.error('[DEBUG] Error saving project data:', error);

        // Hide loading toast
        if (loadingToast && window.Toast) {
            Toast.hide(loadingToast);
        }

        if (window.Toast) {
            Toast.error('Erreur de connexion', 'Impossible d\'enregistrer les données. Vérifiez votre connexion.');
        } else {
            alert('Impossible d\'enregistrer les données. Vérifiez votre connexion.');
        }
    });
}

// Function to clear form - SIMPLIFIED
function clearFormSimple() {
    console.log('[DEBUG] Clearing form data');

    let loadingToast = null;
    if (window.Toast) {
        loadingToast = Toast.loading('Suppression', 'Suppression des données...');
    }

    const formFields = [
        'report-date', 'project-name', 'project-owner', 'contractor',
        'visit-by', 'in-presence-of', 'visit-date', 'visit-number',
        'architect-file', 'distribution', 'project-description'
    ];

    // Clear all form fields safely
    formFields.forEach(fieldId => {
        try {
            const element = document.getElementById(fieldId);
            if (element) {
                element.value = '';
                console.log(`[DEBUG] Cleared field: ${fieldId}`);
            } else {
                console.error(`[DEBUG] Field not found: ${fieldId}`);
            }
        } catch (error) {
            console.error(`[DEBUG] Error clearing field ${fieldId}:`, error);
        }
    });

    // Reset image preview safely
    try {
        const imagePreview = document.getElementById('project-image-preview');
        if (imagePreview) {
            imagePreview.innerHTML = `
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
            `;
            console.log('[DEBUG] Image preview reset');
        }
    } catch (error) {
        console.error('[DEBUG] Error resetting image preview:', error);
    }

    // Hide data status safely
    try {
        const dataStatus = document.getElementById('data-status');
        if (dataStatus) {
            dataStatus.classList.add('hidden');
            console.log('[DEBUG] Data status hidden');
        }
    } catch (error) {
        console.error('[DEBUG] Error hiding data status:', error);
    }

    // Hide loading toast and show success
    setTimeout(() => {
        if (loadingToast && window.Toast) {
            Toast.hide(loadingToast);
            Toast.success('Données supprimées', 'Toutes les données du formulaire ont été supprimées');
        }
    }, 500);
}

// Helper function to get all form data safely
function getFormDataForSave() {
    console.log('[DEBUG] Collecting form data safely');

    const formData = {
        reportDate: getElementValueSafe('report-date'),
        projectName: getElementValueSafe('project-name'),
        projectOwner: getElementValueSafe('project-owner'),
        contractor: getElementValueSafe('contractor'),
        visitBy: getElementValueSafe('visit-by'),
        inPresenceOf: getElementValueSafe('in-presence-of'),
        visitDate: getElementValueSafe('visit-date'),
        visitNumber: getElementValueSafe('visit-number'),
        architectFile: getElementValueSafe('architect-file'),
        distribution: getElementValueSafe('distribution'),
        description: getElementValueSafe('project-description'),
        lastSaved: new Date().toISOString()
    };

    // Get image if exists - safely
    try {
        const imagePreview = document.getElementById('project-image-preview');
        if (imagePreview) {
            const img = imagePreview.querySelector('img');
            if (img && img.src) {
                formData.imageUrl = img.src;
                console.log('[DEBUG] Image URL included in form data');
            }
        }
    } catch (error) {
        console.error('[DEBUG] Error getting image URL:', error);
    }

    return formData;
}

// Helper function to get element value safely
function getElementValueSafe(elementId) {
    try {
        const element = document.getElementById(elementId);
        return element ? (element.value || '') : '';
    } catch (error) {
        console.error(`[DEBUG] Error getting value for ${elementId}:`, error);
        return '';
    }
}

// Helper function to update last saved status safely
function updateLastSavedStatusSimple(saveDate) {
    console.log('[DEBUG] Updating last saved status:', saveDate);

    try {
        const lastSavedText = document.getElementById('last-saved-text');
        if (lastSavedText) {
            const formattedDate = saveDate.toLocaleString();
            lastSavedText.textContent = `Dernière sauvegarde: ${formattedDate}`;
            console.log('[DEBUG] Last saved text updated to:', formattedDate);
        }

        // Show the data status container
        const dataStatus = document.getElementById('data-status');
        if (dataStatus) {
            dataStatus.classList.remove('hidden');
            console.log('[DEBUG] Data status shown');
        }
    } catch (error) {
        console.error('[DEBUG] Error updating last saved status:', error);
    }
}

// Helper function to get CSRF token safely
function getCsrfTokenForSave() {
    try {
        return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
            document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1] || '';
    } catch (error) {
        console.error('[DEBUG] Error getting CSRF token:', error);
        return '';
    }
}

// Make functions available globally - SIMPLIFIED
window.projectForm = {
    saveProjectData: saveProjectDataSimple,
    clearForm: clearFormSimple
};