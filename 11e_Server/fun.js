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
