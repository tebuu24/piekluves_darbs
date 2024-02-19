document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission

  var formData = new FormData(this); // Get form data
  var requestData = {}; // Prepare request data object

  // Convert form data to JSON
  for (var [key, value] of formData.entries()) {
      requestData[key] = value;
  }

  // Send POST request to the server
  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
  })
  .then(response => response.json())
  .then(data => {
      // Handle response from the server
      alert(data.message);
  })
  .catch(error => {
      console.error('Error:', error);
  });
});
