/**
 * API wrapper for SceneValidator web UI.
 * This module provides client-side functions to interact with the SceneValidator API.
 */

class SceneValidatorAPI {
    /**
     * Initialize the API wrapper.
     * @param {string} baseUrl - Base URL for the API
     */
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }

    /**
     * Validate a single scene.
     * @param {Object} sceneData - Scene data to validate
     * @returns {Promise<Object>} - Validation results
     */
    async validateScene(sceneData) {
        try {
            const response = await fetch(`${this.baseUrl}/validate/scene`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(sceneData)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error validating scene:', error);
            throw error;
        }
    }

    /**
     * Validate a scene file by uploading it.
     * @param {File} file - Scene file to validate
     * @returns {Promise<Object>} - Validation results
     */
    async validateSceneFile(file) {
        try {
            // First check if the file is JSON or XML
            if (!file.name.endsWith('.json') && !file.name.endsWith('.xml')) {
                throw new Error('Unsupported file format. Only JSON and XML are supported.');
            }

            // For JSON files, parse and send directly
            if (file.name.endsWith('.json')) {
                const fileContent = await this.readFileAsText(file);
                const sceneData = JSON.parse(fileContent);
                return await this.validateScene(sceneData);
            }

            // For XML files, we need to upload the file
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseUrl}/validate/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error validating file:', error);
            throw error;
        }
    }

    /**
     * Validate multiple scenes.
     * @param {Array<Object>} scenes - Array of scene data objects
     * @returns {Promise<Object>} - Validation results
     */
    async validateProject(scenes) {
        try {
            const response = await fetch(`${this.baseUrl}/validate/project`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(scenes)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error validating project:', error);
            throw error;
        }
    }

    /**
     * Get recent validation reports.
     * @param {number} limit - Maximum number of reports to return
     * @returns {Promise<Array>} - Array of report summaries
     */
    async getRecentReports(limit = 10) {
        try {
            const response = await fetch(`${this.baseUrl}/reports/recent?limit=${limit}`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching recent reports:', error);
            throw error;
        }
    }

    /**
     * Get a specific validation report.
     * @param {string} reportId - ID of the report to retrieve
     * @returns {Promise<Object>} - Report data
     */
    async getReport(reportId) {
        try {
            const response = await fetch(`${this.baseUrl}/reports/${reportId}`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching report:', error);
            throw error;
        }
    }

    /**
     * Get current configuration.
     * @returns {Promise<Object>} - Current configuration
     */
    async getConfig() {
        try {
            const response = await fetch(`${this.baseUrl}/config`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching configuration:', error);
            throw error;
        }
    }

    /**
     * Update configuration.
     * @param {Object} config - Updated configuration
     * @returns {Promise<Object>} - Updated configuration
     */
    async updateConfig(config) {
        try {
            const response = await fetch(`${this.baseUrl}/config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error updating configuration:', error);
            throw error;
        }
    }

    /**
     * Get validation rules.
     * @returns {Promise<Object>} - Current validation rules
     */
    async getValidationRules() {
        try {
            const response = await fetch(`${this.baseUrl}/validation-rules`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching validation rules:', error);
            throw error;
        }
    }

    /**
     * Update validation rules.
     * @param {Object} rules - Updated validation rules
     * @returns {Promise<Object>} - Updated validation rules
     */
    async updateValidationRules(rules) {
        try {
            const response = await fetch(`${this.baseUrl}/validation-rules`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(rules)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error updating validation rules:', error);
            throw error;
        }
    }

    /**
     * Helper method to read file as text.
     * @param {File} file - File to read
     * @returns {Promise<string>} - File contents as text
     * @private
     */
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = event => resolve(event.target.result);
            reader.onerror = error => reject(error);
            reader.readAsText(file);
        });
    }

    /**
     * Health check for the API.
     * @returns {Promise<Object>} - Health status
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error during health check:', error);
            throw error;
        }
    }
}

// Create global instance for easy access
const sceneValidatorAPI = new SceneValidatorAPI();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SceneValidatorAPI };
}