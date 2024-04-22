// Update the form submission event listener
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    var formData = new FormData(this);

    fetch('/add_user', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the success message dynamically on the page
        alert(data.message);
        if (data.type === 'success') {
            // Optionally, you can update the user list here without reloading the page
            fetchUserList(); // Fetch and update the user list
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to fetch and update the user list (you can customize this according to your needs)
function fetchUserList() {
    fetch('/admin_panel')
    .then(response => response.text())
    .then(html => {
        // Update the user list container with the new HTML content
        document.getElementById('userListContainer').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
