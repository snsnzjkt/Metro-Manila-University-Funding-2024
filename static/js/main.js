
/**
 * main.js - JavaScript enhancements for the Metro Manila Research Funding Map
 */

// Executed when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current navigation item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentLocation || 
            (linkPath === '/' && currentLocation === '/')) {
            link.classList.add('active');
        }
    });
    
    // Handle page print styles for map exports
    if (window.location.pathname === '/map') {
        const style = document.createElement('style');
        style.textContent = `
            @media print {
                body {
                    margin: 0;
                    padding: 0;
                }
                
                .leaflet-control-container {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Add a title for the standalone map page
        if (!document.title) {
            document.title = 'Metro Manila Research Funding Map (2024)';
        }
    }
});

/**
 * Format large numbers with commas for readability
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Calculate the percentage change between two values
 * @param {number} oldValue - Original value
 * @param {number} newValue - New value
 * @returns {string} Formatted percentage change
 */
function percentageChange(oldValue, newValue) {
    const change = ((newValue - oldValue) / oldValue) * 100;
    return change.toFixed(1) + '%';
}

/**
 * Handle map error scenarios
 * @param {string} elementId - ID of container element to show error
 * @param {string} message - Error message to display
 */
function handleMapError(elementId, message) {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">Map Loading Error</h4>
                <p>${message}</p>
                <hr>
                <p class="mb-0">Please try refreshing the page or contact support if the problem persists.</p>
            </div>
        `;
    }
}
