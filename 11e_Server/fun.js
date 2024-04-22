function deleteUser(userId) {
    // Confirm deletion
    if (confirm('Vai jūs vēlaties dzēst šo lietotāju')) {
        // Send DELETE request to Flask server
        fetch(`/delete_user/${userId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Remove the row from the HTML table
                document.getElementById(`user_row_${userId}`).remove();
            } else {
                // Display error message if deletion fails
                alert('Kļūda dzēšot lietotāju');
            }
        })
        .catch(error => {
            // Handle network or server errors
            console.error('Error:', error);
        });
    }
}
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
