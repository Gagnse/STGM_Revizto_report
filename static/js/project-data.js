// Project data management using localStorage - Fixed version
class ProjectDataManager {
    constructor() {
        // Initialize the storage key
        this.STORAGE_KEY_PREFIX = 'stgm_project_';
        console.log('ProjectDataManager initialized');
    }

    /**
     * Save project data to localStorage
     * @param {string} projectId - The project ID
     * @param {object} projectData - The project data to save
     */
    saveProjectData(projectId, projectData) {
        if (!projectId) {
            console.error('No project ID provided for saving data');
            return false;
        }

        try {
            // Create a storage key specific to this project
            const storageKey = this.STORAGE_KEY_PREFIX + projectId;

            // Add timestamp for tracking when the data was last saved
            projectData.lastSaved = new Date().toISOString();

            // Save to localStorage
            localStorage.setItem(storageKey, JSON.stringify(projectData));

            console.log(`Project data saved for project ID: ${projectId}`);
            console.log('Saved data:', projectData);
            return true;
        } catch (error) {
            console.error('Error saving project data:', error);
            return false;
        }
    }

    /**
     * Load project data from localStorage
     * @param {string} projectId - The project ID
     * @returns {object|null} - The project data or null if not found
     */
    loadProjectData(projectId) {
        if (!projectId) {
            console.error('No project ID provided for loading data');
            return null;
        }

        try {
            // Create storage key for this project
            const storageKey = this.STORAGE_KEY_PREFIX + projectId;
            console.log(`Attempting to load data for project ID: ${projectId}`);
            console.log(`Storage key: ${storageKey}`);

            // Get data from localStorage
            const savedData = localStorage.getItem(storageKey);

            if (!savedData) {
                console.log(`No saved data found for project ID: ${projectId}`);
                return null;
            }

            // Parse the JSON data
            const projectData = JSON.parse(savedData);
            console.log(`Loaded project data for project ID: ${projectId}`);
            console.log('Loaded data:', projectData);

            return projectData;
        } catch (error) {
            console.error('Error loading project data:', error);
            console.error(error.stack);
            return null;
        }
    }

    /**
     * Check if there is saved data for a project
     * @param {string} projectId - The project ID
     * @returns {boolean} - True if there is saved data, false otherwise
     */
    hasProjectData(projectId) {
        if (!projectId) return false;

        const storageKey = this.STORAGE_KEY_PREFIX + projectId;
        const hasData = localStorage.getItem(storageKey) !== null;
        console.log(`Checking if project ${projectId} has data: ${hasData}`);
        return hasData;
    }

    /**
     * Delete project data from localStorage
     * @param {string} projectId - The project ID
     */
    deleteProjectData(projectId) {
        if (!projectId) return;

        const storageKey = this.STORAGE_KEY_PREFIX + projectId;
        localStorage.removeItem(storageKey);
        console.log(`Deleted project data for project ID: ${projectId}`);
    }

    /**
     * Get a list of all projects with saved data
     * @returns {Array} - Array of project IDs with saved data
     */
    getProjectsWithSavedData() {
        const projects = [];

        // Loop through all localStorage items
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);

            // Check if this is a project data key
            if (key && key.startsWith(this.STORAGE_KEY_PREFIX)) {
                // Extract the project ID from the key
                const projectId = key.replace(this.STORAGE_KEY_PREFIX, '');
                projects.push(projectId);
            }
        }

        console.log(`Found ${projects.length} projects with saved data:`, projects);
        return projects;
    }
}

// Initialize the project data manager as a global variable
window.projectDataManager = new ProjectDataManager();