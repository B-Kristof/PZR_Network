const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql2/promise');

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true
}));

// Database connection parameters
const dbConfig = {
    host: '127.0.0.1',
    user: 'urbex',
    password: 'PZRUrbexsql',
    database: 'pzr_urbex'
};

// Hash function
async function calculateHash(input) {
    const saltRounds = 10;
    return await bcrypt.hash(input, saltRounds);
}

async function loginWithHash(conn, inputUsername, inputPassword) {
    const [rows] = await conn.execute('SELECT * FROM users WHERE username = ?', [inputUsername]);
    if (rows.length > 0) {
        const user = rows[0];
        const match = await bcrypt.compare(inputPassword, user.password);
        if (match) {
            return user;
        }
    }
    return null;
}

app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    let conn;

    try {
        conn = await mysql.createConnection(dbConfig);
        const user = await loginWithHash(conn, username, password);
        if (user) {
            req.session.authenticated = true;
            req.session.username = username;
            res.redirect('/locations');
        } else {
            res.send('Invalid username or password.');
        }
    } catch (err) {
        res.status(500).send('Database connection failed: ' + err.message);
    } finally {
        if (conn) conn.end();
    }
});

app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Urbex Login</title>
            <link rel="stylesheet" href="styles/index.css" media="screen and (min-device-width: 767px)">
            <link rel="stylesheet" type="text/css" media="screen and (max-device-width: 767px)" href="styles/mobile/index_mobile.css"/>
        </head>
        <body>
            <div class="container">
                <div class="login-container">
                    <h2>PZR Urbex Portal</h2>
                    <form id="login-form" method="post" action="/login">
                        <div class="input-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="input-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit" name="login">Login</button>
                    </form><br>
                    <form action="register.php">
                        <button type="submit">Create new account</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    `);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
