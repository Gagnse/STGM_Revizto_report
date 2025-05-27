// PDF generation functionality - SIMPLIFIED VERSION
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] Simple PDF generation handler initialized');

    // Add event listener for the PDF generation button
    const generatePdfBtn = document.getElementById('generate-pdf');

    if (generatePdfBtn) {
        generatePdfBtn.addEventListener('click', function() {
            console.log('[DEBUG] Generate PDF button clicked');
            generateProjectPDFSimple();
        });
    } else {
        console.error('[DEBUG] Generate PDF button not found in DOM');
    }

    // Make function available globally
    window.pdfGenerator = {
        generateProjectPDF: generateProjectPDFSimple
    };
});

/**
 * Simple PDF generation without complex DOM manipulation
 */
function generateProjectPDFSimple() {
    // Check if a project is selected
    if (!window.activeProjectId) {
        console.error('[DEBUG] No active project selected');
        if (window.Toast) {
            Toast.error('Projet manquant', 'Veuillez sélectionner un projet d\'abord');
        } else {
            alert('Veuillez sélectionner un projet d\'abord');
        }
        return;
    }

    console.log('[DEBUG] Generating PDF for project ID:', window.activeProjectId);

    // Show simple loading toast
    let processingToastId = null;
    if (window.Toast) {
        processingToastId = Toast.loading('Génération PDF', 'Préparation en cours...');
    }

    // Show loading state on button
    showPdfGenerationLoadingSimple(true);

    // Simple auto-save before PDF generation
    saveProjectDataSimple()
        .then(() => {
            console.log('[DEBUG] Data saved, generating PDF...');

            if (processingToastId && window.Toast) {
                // Simple update without complex DOM manipulation
                Toast.hide(processingToastId);
                processingToastId = Toast.loading('Génération PDF', 'Création du document...');
            }

            // Generate PDF URL and open in new tab
            const pdfUrl = `/api/projects/${window.activeProjectId}/generate-pdf/`;
            console.log('[DEBUG] Opening PDF URL:', pdfUrl);

            // Simple window.open approach
            const newWindow = window.open(pdfUrl, '_blank');

            // Hide loading after short delay
            setTimeout(() => {
                if (processingToastId && window.Toast) {
                    Toast.hide(processingToastId);
                }

                showPdfGenerationLoadingSimple(false);

                if (window.Toast) {
                    if (newWindow) {
                        Toast.success('PDF généré', 'Le PDF s\'ouvre dans un nouvel onglet');
                    } else {
                        Toast.warning('Popup bloqué', 'Veuillez autoriser les popups pour télécharger le PDF');
                    }
                } else {
                    if (!newWindow) {
                        alert('Le PDF a été généré mais les popups sont bloquées. Veuillez les autoriser.');
                    }
                }
            }, 1500);

        })
        .catch(error => {
            console.error('[DEBUG] Error in PDF generation:', error);

            if (processingToastId && window.Toast) {
                Toast.hide(processingToastId);
                Toast.error('Erreur PDF', 'Impossible de générer le PDF: ' + error.message);
            } else {
                alert('Erreur lors de la génération du PDF: ' + error.message);
            }

            showPdfGenerationLoadingSimple(false);
        });
}

/**
 * Simple data saving before PDF generation
 */
function saveProjectDataSimple() {
    return new Promise((resolve, reject) => {
        try {
            console.log('[DEBUG] Simple auto-save before PDF');

            const projectId = window.activeProjectId;
            const formData = getFormDataSimple();
            const csrfToken = getCsrfTokenSimple();

            if (!projectId || !formData || !csrfToken) {
                console.warn('[DEBUG] Missing data for auto-save, proceeding anyway');
                resolve();
                return;
            }

            fetch(`/api/projects/${projectId}/data/save/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('[DEBUG] Auto-save completed:', data.success);
                resolve();
            })
            .catch(error => {
                console.warn('[DEBUG] Auto-save failed, continuing with PDF:', error);
                resolve(); // Don't block PDF generation
            });

        } catch (error) {
            console.warn('[DEBUG] Auto-save exception, continuing:', error);
            resolve(); // Don't block PDF generation
        }
    });
}

/**
 * Simple button loading state
 */
function showPdfGenerationLoadingSimple(isLoading) {
    const generatePdfBtn = document.getElementById('generate-pdf');
    if (!generatePdfBtn) return;

    if (isLoading) {
        generatePdfBtn.setAttribute('data-original-text', generatePdfBtn.textContent);
        generatePdfBtn.textContent = 'Génération...';
        generatePdfBtn.disabled = true;
        generatePdfBtn.style.opacity = '0.6';
    } else {
        const originalText = generatePdfBtn.getAttribute('data-original-text') || 'Générer PDF';
        generatePdfBtn.textContent = originalText;
        generatePdfBtn.disabled = false;
        generatePdfBtn.style.opacity = '1';
    }
}

/**
 * Simple form data collection
 */
function getFormDataSimple() {
    try {
        const formData = {
            reportDate: getElementValueSimple('report-date'),
            projectName: getElementValueSimple('project-name'),
            projectOwner: getElementValueSimple('project-owner'),
            contractor: getElementValueSimple('contractor'),
            visitBy: getElementValueSimple('visit-by'),
            inPresenceOf: getElementValueSimple('in-presence-of'),
            visitDate: getElementValueSimple('visit-date'),
            visitNumber: getElementValueSimple('visit-number'),
            architectFile: getElementValueSimple('architect-file'),
            distribution: getElementValueSimple('distribution'),
            description: getElementValueSimple('project-description'),
            lastSaved: new Date().toISOString()
        };

        // Get image if exists
        const imagePreview = document.getElementById('project-image-preview');
        if (imagePreview) {
            const img = imagePreview.querySelector('img');
            if (img && img.src) {
                formData.imageUrl = img.src;
            }
        }

        return formData;
    } catch (error) {
        console.error('[DEBUG] Error collecting form data:', error);
        return {};
    }
}

function getElementValueSimple(elementId) {
    try {
        const element = document.getElementById(elementId);
        return element ? element.value || '' : '';
    } catch (error) {
        console.error(`[DEBUG] Error getting value for ${elementId}:`, error);
        return '';
    }
}

function getCsrfTokenSimple() {
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