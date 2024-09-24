// Sample data to simulate available pans, reservoirs, and PCRs
let panList = [];

// Loop through numbers 1 to 32
for (let i = 1; i <= 32; i++) {
    // Create an object with the desired id and name
    let pan = {
        id: 'Pan' + i,  // e.g., Pan1, Pan2, ..., Pan32
        name: 'Pan ' + i  // e.g., Pan 1, Pan 2, ..., Pan 32
    };
    
    // Add the object to the panList array
    panList.push(pan);
}

const panData = {
    pan: panList,
    reservoir: [
        { id: 'R1', name: 'Reservoir 1' },
        { id: 'R2', name: 'Reservoir 2' },
        { id: 'R3', name: 'Reservoir 3' },
        { id: 'R4', name: 'Reservoir 4' },
        { id: 'R5', name: 'Reservoir 5' }
    ],
    pcr: [
        { id: 'PCR1', name: 'PCR 1' },
        { id: 'PCR2', name: 'PCR 2' }
    ]
};

// Function to dynamically populate the pan options based on the selected pan type
function updatePanOptions() {
    const panType = $("#pan_type").val();
    $("#pan").empty();

    panData[panType].forEach(function(pan) {
        // Use append to add each option, not overwrite
        $("#pan").append(`<option value="${pan.id}">${pan.name}</option>`);
    });
}

// Function to handle form submission
function submitForm(event) {
    event.preventDefault();

    const panType = $("#pan_type").val();
    const panId = $("#pan").val();
    const salinity = $("#salinity").val();
    const brineLevel = $("#brine").val(); // Corrected 'Brine' to 'brine'

    const data = {
        pan_type: panType,
        pan_id: panId,
        salinity_level: salinity,
        brine_level: brineLevel
    };

    // Simulating the form submission with jQuery AJAX
    $.ajax({
        url: 'url',  // Replace 'url' with your actual server URL
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('Success:', response);
            alert(`${panId} data submitted successfully!`);
        },
        error: function(error) {
            console.error('Error:', error);
            alert('Failed to submit salinity data');
        }
    });
}

// Initialize the form with default pan type options on page load
$(document).ready(function() {
    updatePanOptions();

    // Bind the form submission handler
    $('#salinityForm').on('submit', submitForm);

    // Bind the pan type change handler
    $('#pan_type').on('change', updatePanOptions);
});
