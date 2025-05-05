// Custom date picker enhancements
document.addEventListener('DOMContentLoaded', () => {
    // We'll check periodically if the date inputs exist
    // (since they're loaded dynamically)
    const dateInitInterval = setInterval(() => {
        const dateFrom = document.getElementById('date-from');
        const dateTo = document.getElementById('date-to');

        if (dateFrom && dateTo) {
            enhanceDatePickers(dateFrom, dateTo);
            clearInterval(dateInitInterval);
        }
    }, 100);
});

function enhanceDatePickers(dateFromInput, dateToInput) {
    // Ensure "to" date is never before "from" date
    dateFromInput.addEventListener('change', function() {
        const fromDate = parseDate(this.value);
        const toDate = parseDate(dateToInput.value);

        if (fromDate && toDate && fromDate > toDate) {
            dateToInput.value = this.value;
        }
    });

    dateToInput.addEventListener('change', function() {
        const fromDate = parseDate(dateFromInput.value);
        const toDate = parseDate(this.value);

        if (fromDate && toDate && toDate < fromDate) {
            dateFromInput.value = this.value;
        }
    });

    // Set default dates if empty
    if (!dateFromInput.value) {
        const today = new Date();
        const oneMonthAgo = new Date();
        oneMonthAgo.setMonth(today.getMonth() - 1);

        dateFromInput.value = formatDate(oneMonthAgo);
    }

    if (!dateToInput.value) {
        const today = new Date();
        dateToInput.value = formatDate(today);
    }
}

// Helper function to parse date in DD/MM/YYYY format
function parseDate(dateString) {
    if (!dateString) return null;

    const parts = dateString.split('/');
    if (parts.length !== 3) return null;

    // Note: months are 0-based in JavaScript Date
    return new Date(parts[2], parts[1] - 1, parts[0]);
}

// Helper function to format date as DD/MM/YYYY
function formatDate(date) {
    if (!date) return '';

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    return `${day}/${month}/${year}`;
}