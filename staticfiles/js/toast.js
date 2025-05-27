/**
 * Modern Toast Notification System
 * Features: Multiple types, auto-dismiss, progress bars, animations, mobile responsive
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.toasts = new Map();
        this.init();
    }

    init() {
        // Create toast container if it doesn't exist
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    /**
     * Show a toast notification
     * @param {Object} options - Toast configuration
     * @param {string} options.type - Toast type: 'success', 'error', 'warning', 'info', 'loading'
     * @param {string} options.title - Toast title
     * @param {string} options.message - Toast message
     * @param {number} options.duration - Auto-dismiss duration in ms (0 for no auto-dismiss)
     * @param {boolean} options.closable - Whether the toast can be manually closed
     * @param {Function} options.onClose - Callback when toast is closed
     * @returns {string} Toast ID for manual control
     */
    show(options = {}) {
        const {
            type = 'info',
            title = '',
            message = '',
            duration = type === 'loading' ? 0 : 5000,
            closable = true,
            onClose = null
        } = options;

        const id = this.generateId();
        const toast = this.createToastElement(id, type, title, message, closable);

        // Store toast reference
        this.toasts.set(id, {
            element: toast,
            type,
            title,
            message,
            duration,
            onClose,
            timeoutId: null,
            progressInterval: null
        });

        // Add to container
        this.container.appendChild(toast);

        // Trigger animation
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });

        // Set up auto-dismiss if duration > 0
        if (duration > 0) {
            this.setupAutoDismiss(id, duration);
        }

        // Set up close button
        if (closable) {
            this.setupCloseButton(id);
        }

        return id;
    }

    createToastElement(id, type, title, message, closable) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.setAttribute('data-toast-id', id);

        const icon = this.getIcon(type);
        const closeButton = closable ? this.getCloseButton() : '';
        const progressBar = type !== 'loading' ? '<div class="toast-progress"></div>' : '';

        toast.innerHTML = `
            ${icon}
            <div class="toast-content">
                ${title ? `<div class="toast-title">${this.escapeHtml(title)}</div>` : ''}
                ${message ? `<div class="toast-message">${this.escapeHtml(message)}</div>` : ''}
            </div>
            ${closeButton}
            ${progressBar}
        `;

        return toast;
    }

    getIcon(type) {
        const icons = {
            success: `
                <svg class="toast-icon success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            `,
            error: `
                <svg class="toast-icon error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            `,
            warning: `
                <svg class="toast-icon warning" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
            `,
            info: `
                <svg class="toast-icon info" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            `,
            loading: `
                <svg class="toast-icon loading" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
            `
        };

        return icons[type] || icons.info;
    }

    getCloseButton() {
        return `
            <svg class="toast-close" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        `;
    }

    setupAutoDismiss(id, duration) {
        const toast = this.toasts.get(id);
        if (!toast) return;

        const progressBar = toast.element.querySelector('.toast-progress');

        // Animate progress bar
        if (progressBar) {
            progressBar.style.width = '100%';
            progressBar.style.transition = `width ${duration}ms linear`;

            requestAnimationFrame(() => {
                progressBar.style.width = '0%';
            });
        }

        // Set timeout for auto-dismiss
        toast.timeoutId = setTimeout(() => {
            this.hide(id);
        }, duration);
    }

    setupCloseButton(id) {
        const toast = this.toasts.get(id);
        if (!toast) return;

        const closeButton = toast.element.querySelector('.toast-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.hide(id);
            });
        }
    }

    /**
     * Hide a specific toast
     * @param {string} id - Toast ID
     */
    hide(id) {
        const toast = this.toasts.get(id);
        if (!toast) return;

        // Clear any timeouts
        if (toast.timeoutId) {
            clearTimeout(toast.timeoutId);
        }
        if (toast.progressInterval) {
            clearInterval(toast.progressInterval);
        }

        // Animate out
        toast.element.classList.remove('show');
        toast.element.classList.add('hide');

        // Remove from DOM after animation
        setTimeout(() => {
            if (toast.element.parentNode) {
                toast.element.parentNode.removeChild(toast.element);
            }

            // Call onClose callback
            if (toast.onClose) {
                toast.onClose();
            }

            // Remove from tracking
            this.toasts.delete(id);
        }, 300);
    }

    /**
     * Update an existing toast (useful for loading states)
     * @param {string} id - Toast ID
     * @param {Object} options - New toast options
     */
    update(id, options = {}) {
        const toast = this.toasts.get(id);
        if (!toast) return;

        const {
            type = toast.type,
            title = toast.title,
            message = toast.message,
            duration = null
        } = options;

        // Update stored values
        toast.type = type;
        toast.title = title;
        toast.message = message;

        // Update DOM safely
        const element = toast.element;
        if (!element || !element.parentNode) {
            console.warn('[TOAST] Cannot update toast - element not in DOM');
            return;
        }

        try {
            element.className = `toast ${type} show`;

            // Update icon safely
            const iconContainer = element.querySelector('.toast-icon')?.parentNode;
            if (iconContainer) {
                iconContainer.innerHTML = this.getIcon(type);
            }

            // Update title safely
            const titleElement = element.querySelector('.toast-title');
            if (titleElement && title) {
                titleElement.textContent = title;
            } else if (title && !titleElement) {
                const content = element.querySelector('.toast-content');
                if (content) {
                    const titleDiv = document.createElement('div');
                    titleDiv.className = 'toast-title';
                    titleDiv.textContent = title;
                    content.insertBefore(titleDiv, content.firstChild);
                }
            }

            // Update message safely
            const messageElement = element.querySelector('.toast-message');
            if (messageElement && message) {
                messageElement.textContent = message;
            } else if (message && !messageElement) {
                const content = element.querySelector('.toast-content');
                if (content) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'toast-message';
                    messageDiv.textContent = message;
                    content.appendChild(messageDiv);
                }
            }

            // Handle duration change
            if (duration !== null && duration !== toast.duration) {
                // Clear existing timeout
                if (toast.timeoutId) {
                    clearTimeout(toast.timeoutId);
                }

                toast.duration = duration;

                if (duration > 0) {
                    this.setupAutoDismiss(id, duration);
                }
            }
        } catch (error) {
            console.error('[TOAST] Error updating toast:', error);
        }
    }

    /**
     * Hide all toasts
     */
    clear() {
        this.toasts.forEach((_, id) => {
            this.hide(id);
        });
    }

    /**
     * Convenience methods for different toast types
     */
    success(title, message, options = {}) {
        return this.show({ ...options, type: 'success', title, message });
    }

    error(title, message, options = {}) {
        return this.show({ ...options, type: 'error', title, message });
    }

    warning(title, message, options = {}) {
        return this.show({ ...options, type: 'warning', title, message });
    }

    info(title, message, options = {}) {
        return this.show({ ...options, type: 'info', title, message });
    }

    loading(title, message, options = {}) {
        return this.show({ ...options, type: 'loading', title, message, duration: 0 });
    }

    // Utility methods
    generateId() {
        return `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Create global instance
window.Toast = new ToastManager();

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ToastManager;
}