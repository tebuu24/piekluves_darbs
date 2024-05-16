// Pievienot lietotāju datubāzē 
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // lai nevar tukšu ievadīt
    var formData = new FormData(this);

    fetch('/add_user', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.type === 'success') {
            fetchUserList();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// funkcija iegūt un atjaunot lietotāju sarakstu
function fetchUserList() {
    fetch('/admin_panel')
    .then(response => response.text())
    .then(html => {
        // ievietot sarakstā no html lapas datus
        document.getElementById('userListContainer').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
