TravelGo v2 — Setup & Run
=========================

Step 1: Install dependency
  pip install flask

Step 2: Run the app
  python app.py

Step 3: Open browser
  http://localhost:5000

Features
--------
- Search Trains, Buses, Flights across 30 Indian cities
- 30 results per search (trains, buses, flights)
- Departure/arrival times, price, seats, class, rating per result
- Book button opens passenger detail form with live total calculator
- Instant confirmation page with Booking ID and full ticket layout
- My Bookings dashboard with cancel option
- No database needed — runs fully in memory (session-based)
- Same dark navy + teal + orange theme throughout

Project Structure
-----------------
travelgo_v2/
  app.py                  <- Flask backend (30 results per type)
  requirements.txt        <- pip install flask
  templates/
    base.html             <- shared navbar, CSS variables & layout
    index.html            <- home page with search (train/bus/flight tabs)
    search_results.html   <- 30 results with filter sidebar + book modal
    confirmation.html     <- booking confirmation ticket page
    my_bookings.html      <- bookings dashboard with cancel
