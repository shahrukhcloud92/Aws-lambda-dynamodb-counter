// Configuration Constants
const API_ENDPOINT = 'https://0shend8f85.execute-api.us-east-1.amazonaws.com/count';

/**
 * Asynchronously fetches the live visitor count from the API Gateway endpoint
 * and safely updates the DOM.
 */
async function getVisitorCount() {
    const countElement = document.getElementById('count');
    
    try {
        const response = await fetch(API_ENDPOINT);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        // Update the UI with the counter value returned from the backend
        countElement.innerText = data.count;
        
    } catch (error) {
        console.error('Failed to retrieve visitor count:', error);
        countElement.innerText = 'Unavailable';
    }
}

// Execute logic when DOM content is fully parsed
document.addEventListener('DOMContentLoaded', getVisitorCount);