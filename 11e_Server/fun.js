const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('darbinieki.db');

function deleteUser(userId) {
    const query = `DELETE FROM users WHERE id = ?`;
    db.run(query, [userId], function(err) {
        if (err) {
            console.error('Dzēšanas kļūda:', err);
        } else {
            console.log('Lietotājs veiksmīgi dzēsts');
        }
    });
}

deleteUser(user_id);
