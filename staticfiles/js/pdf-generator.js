// PDF generation functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] PDF generation handler initialized');

    // Add event listener for the PDF generation button
    const generatePdfBtn = document.getElementById('generate-pdf');

    if (generatePdfBtn) {
        generatePdfBtn.addEventListener('click', function() {
            console.log('[DEBUG] Generate PDF button clicked');
            generateProjectPDF();
        });
    } else {
        console.error('[DEBUG] Generate PDF button not found in DOM');
    }

    // Make function available globally
    window.pdfGenerator = {
        generateProjectPDF
    };
});

/**
 * Generate PDF for the current project
 */
function generateProjectPDF() {
    // Check if a project is selected
    if (!window.activeProjectId) {
        console.error('[DEBUG] No active project selected');
        showMessage('Veuillez sélectionner un projet d\'abord', 'error');
        return;
    }

    console.log('[DEBUG] Generating PDF for project ID:', window.activeProjectId);

    // Show loading state
    showPdfGenerationLoading(true);

    // Save current project data before generating PDF to ensure all changes are included
    saveProjectDataBeforePdfGeneration()
        .then(() => {
            // Generate PDF by redirecting to the PDF endpoint
            const pdfUrl = `/api/projects/${window.activeProjectId}/generate-pdf/`;
            console.log('[DEBUG] Redirecting to PDF URL:', pdfUrl);

            // Open PDF in a new tab/window
            window.open(pdfUrl, '_blank');

            // Hide loading state
            showPdfGenerationLoading(false);
        })
        .catch(error => {
            console.error('[DEBUG] Error generating PDF:', error);
            showMessage('Erreur lors de la génération du PDF: ' + error.message, 'error');
            showPdfGenerationLoading(false);
        });
}

/**
 * Save project data before generating PDF
 * @returns {Promise} Promise that resolves when data is saved
 */
function saveProjectDataBeforePdfGeneration() {
    return new Promise((resolve, reject) => {
        console.log('[DEBUG] Saving project data before PDF generation');

        // Check if save function exists
        if (window.projectForm && typeof window.projectForm.saveProjectData === 'function') {
            try {
                // Save project data
                const projectId = window.activeProjectId;

                // Call the saveProjectData function and handle its response
                window.projectForm.saveProjectData(projectId);

                // Since saveProjectData might not return a Promise, we'll just wait a bit
                setTimeout(() => {
                    console.log('[DEBUG] Project data saved (or timeout) before PDF generation');
                    resolve();
                }, 1000);
            } catch (error) {
                console.error('[DEBUG] Exception saving project data before PDF generation:', error);
                // Continue with PDF generation even if save fails
                resolve();
            }
        } else {
            console.warn('[DEBUG] projectForm.saveProjectData function not available, skipping save before PDF generation');
            // Continue with PDF generation without saving
            resolve();
        }
    });
}

/**
 * Show or hide PDF generation loading state
 * @param {boolean} isLoading - True to show loading, false to hide
 */
function showPdfGenerationLoading(isLoading) {
    const generatePdfBtn = document.getElementById('generate-pdf');

    if (!generatePdfBtn) {
        return;
    }

    if (isLoading) {
        // Save original text and disable button
        generatePdfBtn.setAttribute('data-original-text', generatePdfBtn.innerText);
        generatePdfBtn.innerText = 'Génération en cours...';
        generatePdfBtn.disabled = true;
        generatePdfBtn.classList.add('opacity-75', 'cursor-not-allowed');
    } else {
        // Restore original text and enable button
        const originalText = generatePdfBtn.getAttribute('data-original-text') || 'Générer PDF';
        generatePdfBtn.innerText = originalText;
        generatePdfBtn.disabled = false;
        generatePdfBtn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
}

/**
 * Show message to user
 * @param {string} message - Message to display
 * @param {string} type - Message type (info, success, warning, error)
 */
function showMessage(message, type = 'info') {
    console.log(`[DEBUG] [${type.toUpperCase()}] ${message}`);

    if (type === 'error') {
        alert(message);
    } else if (window.projectForm && typeof window.projectForm.showMessage === 'function') {
        // Use projectForm's showMessage function if available
        window.projectForm.showMessage(message, type);
    }
}