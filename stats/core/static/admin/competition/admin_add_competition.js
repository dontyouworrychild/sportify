// document.addEventListener('DOMContentLoaded', function() {
//     // Function to toggle the region field visibility
//     function toggleRegionField() {
//       // Get the value of the competition type field
//       var competitionType = document.getElementById('id_competition_type').value;
//       // Get the region field container by its ID or class
//       var regionFieldContainer = document.querySelector('.field-region');
      
//       // Check the competition type and show/hide the region field
//       if (competitionType === 'regional') {
//         regionFieldContainer.style.display = 'block'; // Show the region field
//       } else {
//         regionFieldContainer.style.display = 'none'; // Hide the region field
//       }
//     }
    
//     // Call the function to set the initial state
//     toggleRegionField();
  
//     // Add an event listener to the competition type field to handle changes
//     document.getElementById('id_competition_type').addEventListener('change', toggleRegionField);
//   });



document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle the region field visibility
    function toggleRegionField() {
      // Get the elements for competition type and region fields
      var competitionType = document.getElementById('id_competition_type');
      var regionFieldRow = document.getElementById('id_region').closest('.form-row');
  
      // Check if the competition type field exists and the region field container is found
      if (competitionType && regionFieldRow) {
        // Show or hide the region field based on the competition type value
        if (competitionType.value === 'regional') {
          regionFieldRow.style.display = ''; // Show the region field
        } else {
          regionFieldRow.style.display = 'none'; // Hide the region field
        }
      }
    }
  
    // Bind the toggle function to the competition type field's change event
    var competitionTypeField = document.getElementById('id_competition_type');
    if (competitionTypeField) {
      competitionTypeField.addEventListener('change', toggleRegionField);
    }
  
    // Call the toggle function initially in case the field is pre-populated
    toggleRegionField();
  });
  

// document.addEventListener('DOMContentLoaded', function() {
//     const typeSelect = document.querySelector('#id_competition_type');
//     const regionField = document.querySelector('.field-region');

//     function toggleRegionField() {
//         // Check if the selected value is 'regional'
//         if (typeSelect.value === 'regional') {
//             regionField.style.display = 'block';
//         } else {
//             regionField.style.display = 'none';
//         }
//     }

//     // Initial toggle on load
//     toggleRegionField();

//     // Setup event listener for changes
//     typeSelect.addEventListener('change', toggleRegionField);
// });