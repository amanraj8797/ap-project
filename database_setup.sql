-- Create Movies table
CREATE TABLE Movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    duration INTEGER,
    rating TEXT
);

-- Create Showtimes table
CREATE TABLE Showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    showtime TEXT,
    FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

-- Create Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
);

-- Create Bookings table
CREATE TABLE Bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    showtime_id INTEGER,
    seats INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (showtime_id) REFERENCES Showtimes(id)
);
