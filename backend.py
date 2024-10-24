from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to SQLite3 database
def get_db_connection():
    conn = sqlite3.connect('movie_booking.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route: Home
@app.route('/')
def home():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM Movies').fetchall()
    conn.close()
    return render_template('home.html', movies=movies)

# Route: Showtimes for a Movie
@app.route('/movie/<int:movie_id>')
def showtimes(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM Movies WHERE id = ?', (movie_id,)).fetchone()
    showtimes = conn.execute('SELECT * FROM Showtimes WHERE movie_id = ?', (movie_id,)).fetchall()
    conn.close()
    return render_template('showtimes.html', movie=movie, showtimes=showtimes)

# Route: Booking
@app.route('/book/<int:showtime_id>', methods=('GET', 'POST'))
def book(showtime_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        seats = request.form['seats']

        if not user_id:
            return redirect(url_for('login'))

        conn = get_db_connection()
        conn.execute('INSERT INTO Bookings (user_id, showtime_id, seats) VALUES (?, ?, ?)',
                     (user_id, showtime_id, seats))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    conn = get_db_connection()
    showtime = conn.execute('SELECT * FROM Showtimes WHERE id = ?', (showtime_id,)).fetchone()
    conn.close()
    return render_template('book.html', showtime=showtime)

# Route: User Login
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials!'

    return render_template('login.html')

# Route: User Registration
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        conn.execute('INSERT INTO Users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
