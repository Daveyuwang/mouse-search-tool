// Function to handle mouse search
function searchMice() {
    // Show loading message
    const loadingMessage = document.createElement('div');
    loadingMessage.id = 'loading-message';
    loadingMessage.textContent = 'Searching...';
    document.body.appendChild(loadingMessage);
    const handLength = document.getElementById("hand-length").value;
    const handWidth = document.getElementById("hand-width").value;
    const gripType = document.getElementById("grip-type").value;

    // Handle missing required inputs
    if (!handLength || !handWidth) {
        alert("Please enter both hand length and hand width");
        return;
    }

    if (!gripType) {
        alert("Please select a grip type");
        return;
    }

    const formData = {
        hand_length: parseFloat(handLength),
        hand_width: parseFloat(handWidth),
        leniency: document.querySelector('input[name="leniency"]:checked').value,
        grip_type: gripType,
        shape: document.querySelector('input[name="shape"]:checked').value !== "Both" ? document.querySelector('input[name="shape"]:checked').value : null,
        connection: document.querySelector('input[name="connection"]:checked').value !== "Both" ? document.querySelector('input[name="connection"]:checked').value : null,
        weight: parseInt(document.getElementById("weight").value),
        side_buttons: document.getElementById("side-buttons").value ? parseInt(document.getElementById("side-buttons").value) : null,
        polling_rate: parseInt(document.getElementById("polling-rate").value)
    };

    fetch("https://mou5-backend.onrender.com/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        const resultsTable = document.getElementById("results-table").getElementsByTagName("tbody")[0];
        resultsTable.innerHTML = "";
        const noResultsMessage = document.getElementById('no-results-message');
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
        if (data.length === 0) {
            const noResults = document.createElement('div');
            noResults.id = 'no-results-message';
            noResults.textContent = 'No mice found matching the criteria.';
            document.body.appendChild(noResults);
        } else {
            data.forEach(mouse => {
                const row = resultsTable.insertRow();
                row.insertCell(0).textContent = mouse.name;
                row.insertCell(1).textContent = mouse.weight;
                row.insertCell(2).textContent = mouse.length;
                row.insertCell(3).textContent = mouse.width;
                row.insertCell(4).textContent = mouse.shape;
                row.insertCell(5).textContent = mouse.connectivity;
                row.insertCell(6).textContent = mouse.sensor;
                row.insertCell(7).textContent = mouse.polling_rate;
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
        const noResultsMessage = document.getElementById('no-results-message');
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
        const errorMessage = document.createElement('div');
        errorMessage.id = 'error-message';
        errorMessage.textContent = 'An error occurred while searching. Please try again later.';
        document.body.appendChild(errorMessage);
    })
    .finally(() => {
        // Hide loading message
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    });
}

function sortTable(columnIndex) {
    const table = document.getElementById("results-table");
    const rows = Array.from(table.getElementsByTagName("tbody")[0].rows);
    let direction = table.dataset.sortDirection === "asc" ? "desc" : "asc";
    table.dataset.sortDirection = direction;

    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        let aValue = isNaN(aText) ? aText.toLowerCase() : parseFloat(aText);
        let bValue = isNaN(bText) ? bText.toLowerCase() : parseFloat(bText);

        // Ensure polling rate is always treated as a number
        if (columnIndex === 7) { // assuming polling rate is in column 7
            aValue = parseInt(aText);
            bValue = parseInt(bText);
        }

        if (aValue < bValue) return direction === "asc" ? -1 : 1;
        if (aValue > bValue) return direction === "asc" ? 1 : -1;
        return 0;
    });

    const tbody = table.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));

    // Update header arrow direction
    const headerCells = table.getElementsByTagName("th");
    for (let i = 0; i < headerCells.length; i++) {
        headerCells[i].classList.remove("asc", "desc", "sortable-default");
        if (i === columnIndex) {
            headerCells[i].classList.add(direction);
        } else {
            headerCells[i].classList.add("sortable-default");
        }
    }
}


// Add default sortable indicator to headers
window.onload = function() {
    const headerCells = document.querySelectorAll("#results-table th.sortable");
    headerCells.forEach(header => {
        header.classList.add("sortable-default");
    });
}

// Function to update weight value display
function updateWeightValue(value) {
    const weightValue = document.getElementById("weight-value");
    if (value == 50) {
        weightValue.textContent = "<50";
    } else if (value == 100) {
        weightValue.textContent = "100+";
    } else {
        weightValue.textContent = value;
    }
}