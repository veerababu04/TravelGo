"""
TravelGo v2 — app.py
====================
Run:  python app.py
Open: http://localhost:5000
"""

from flask import Flask, render_template, request, session, redirect, url_for
import random, string, datetime

app = Flask(__name__)
app.secret_key = "travelgo_v2_secret_2025"

# ── 30 Indian Cities ──────────────────────────────────────────────────────────
STATIONS = [
    "Hyderabad", "Delhi", "Mumbai", "Chennai", "Bangalore",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Visakhapatnam", "Surat", "Nagpur", "Indore", "Bhopal",
    "Patna", "Vadodara", "Ludhiana", "Agra", "Nashik",
    "Vijayawada", "Madurai", "Varanasi", "Coimbatore", "Kochi",
    "Guwahati", "Chandigarh", "Amritsar", "Mangalore", "Thiruvananthapuram"
]

# ── Generators ────────────────────────────────────────────────────────────────
def gen_trains(frm, to, date):
    names = [
        "Rajdhani Express", "Shatabdi Express", "Duronto Express",
        "Garib Rath", "Jan Shatabdi", "Humsafar Express",
        "Vande Bharat", "Tejas Express", "Sampark Kranti",
        "Intercity Express", "Double Decker", "Superfast Express",
        "Premium Express", "Mail Express", "Passenger Express",
        "Night Express", "Heritage Express", "Coastal Express",
        "Gateway Express", "Capital Express", "Metro Express",
        "Silver Line", "Golden Chariot", "Royal Express",
        "Valley Express", "Mountain Express", "Desert Express",
        "Monsoon Express", "Sunrise Express", "Sunset Express"
    ]
    classes = ["Sleeper", "3AC", "2AC", "1AC"]
    trains = []
    for i in range(30):
        dep_h = (5 + i * 47 // 30) % 24
        dur = random.randint(4, 14)
        arr_h = (dep_h + dur) % 24
        trains.append({
            "id": f"TR{1001+i}",
            "name": names[i % len(names)],
            "from": frm, "to": to, "date": date,
            "dep": f"{dep_h:02d}:{['00','15','30','45'][i%4]}",
            "arr": f"{arr_h:02d}:{['00','15','30','45'][(i+1)%4]}",
            "duration": f"{dur}h",
            "price": random.randint(350, 3200),
            "seats": random.randint(5, 80),
            "seat_class": classes[i % 4],
            "type": "train",
            "rating": round(random.uniform(3.5, 5.0), 1),
        })
    return trains

def gen_buses(frm, to, date):
    operators = [
        "APSRTC", "TSRTC", "KSRTC", "MSRTC", "UPSRTC",
        "RedBus Express", "Orange Travels", "SRS Travels",
        "VRL Travels", "Neeta Tours", "Parveen Travels",
        "Hans Travels", "Raj Travels", "Sri Travels", "Balaji Travels",
        "Green Line", "Blue Line", "Gold Line", "Silver Travels", "Eagle Travels",
        "Highway King", "Star Bus", "Metro Bus", "City Link", "NightRider",
        "Comfort Coach", "Volvo Express", "Luxury Coach", "Super Deluxe", "AC Express"
    ]
    bus_types = ["Sleeper", "Semi-Sleeper", "AC Seater", "Luxury AC", "Volvo AC", "Non-AC Seater"]
    buses = []
    for i in range(30):
        dep_h = (6 + i * 43 // 30) % 24
        dur = random.randint(5, 15)
        arr_h = (dep_h + dur) % 24
        buses.append({
            "id": f"BS{2001+i}",
            "name": operators[i % len(operators)],
            "from": frm, "to": to, "date": date,
            "dep": f"{dep_h:02d}:{['00','30'][i%2]}",
            "arr": f"{arr_h:02d}:{['00','30'][(i+1)%2]}",
            "duration": f"{dur}h",
            "price": random.randint(250, 2000),
            "seats": random.randint(3, 45),
            "seat_class": bus_types[i % len(bus_types)],
            "type": "bus",
            "rating": round(random.uniform(3.2, 5.0), 1),
        })
    return buses

def gen_flights(frm, to, date):
    airlines = [
        "Air India", "IndiGo", "SpiceJet", "Vistara", "GoAir",
        "AirAsia India", "Star Air", "Blue Dart", "Alliance Air", "Zoom Air",
        "Akasa Air", "TruJet", "Air India Express", "IndiGo Express", "SpiceJet Plus",
        "Vistara Business", "GoFirst", "AirAsia Premium", "Star Express", "Blue Wings",
        "Fly Easy", "Sky One", "Air Deccan", "Paramount Airways", "Kingfisher Revive",
        "Pawan Hans", "Heritage Air", "Coastal Air", "Deccan Air", "Premier Airways"
    ]
    cabins = ["Economy", "Business", "First Class", "Premium Economy"]
    flights = []
    for i in range(30):
        dep_h = (5 + i * 38 // 30) % 24
        dur = random.randint(1, 5)
        arr_h = (dep_h + dur) % 24
        airline = airlines[i % len(airlines)]
        flights.append({
            "id": f"FL{3001+i}",
            "name": airline,
            "flight_no": f"{airline[:2].upper()}{200+i}",
            "from": frm, "to": to, "date": date,
            "dep": f"{dep_h:02d}:{['00','20','40'][i%3]}",
            "arr": f"{arr_h:02d}:{['00','20','40'][(i+1)%3]}",
            "duration": f"{dur}h",
            "price": random.randint(2200, 14000),
            "seats": random.randint(2, 35),
            "seat_class": cabins[i % len(cabins)],
            "type": "flight",
            "rating": round(random.uniform(3.5, 5.0), 1),
        })
    return flights

def gen_booking_id():
    return "TG" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    today = datetime.date.today().isoformat()
    return render_template("index.html", stations=STATIONS, today=today)


@app.route("/search", methods=["POST"])
def search():
    travel_type = request.form.get("travel_type", "train")
    frm         = request.form.get("from_city", "")
    to          = request.form.get("to_city", "")
    date        = request.form.get("travel_date", "")
    passengers  = int(request.form.get("passengers", 1))

    if not frm or not to or frm == to:
        return redirect(url_for("index"))

    if travel_type == "train":
        results = gen_trains(frm, to, date)
    elif travel_type == "bus":
        results = gen_buses(frm, to, date)
    else:
        results = gen_flights(frm, to, date)

    return render_template("search_results.html",
        results=results,
        travel_type=travel_type,
        frm=frm, to=to, date=date,
        passengers=passengers,
        stations=STATIONS,
    )


@app.route("/book", methods=["POST"])
def book():
    passengers = int(request.form.get("passengers", 1))
    price      = int(request.form.get("price", 0))
    data = {
        "booking_id":      gen_booking_id(),
        "travel_id":       request.form.get("travel_id"),
        "travel_type":     request.form.get("travel_type"),
        "vehicle_name":    request.form.get("vehicle_name"),
        "flight_no":       request.form.get("flight_no", ""),
        "from_city":       request.form.get("from_city"),
        "to_city":         request.form.get("to_city"),
        "date":            request.form.get("travel_date"),
        "dep":             request.form.get("dep"),
        "arr":             request.form.get("arr"),
        "duration":        request.form.get("duration"),
        "price":           price,
        "passengers":      passengers,
        "seat_class":      request.form.get("seat_class", ""),
        "passenger_name":  request.form.get("passenger_name", ""),
        "passenger_email": request.form.get("passenger_email", ""),
        "passenger_phone": request.form.get("passenger_phone", ""),
        "booked_at":       datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "total_price":     price * passengers,
    }

    if "bookings" not in session:
        session["bookings"] = []
    bookings = list(session["bookings"])
    bookings.append(data)
    session["bookings"] = bookings

    return render_template("confirmation.html", booking=data)


@app.route("/my-bookings")
def my_bookings():
    bookings = session.get("bookings", [])
    return render_template("my_bookings.html", bookings=bookings)


@app.route("/cancel/<booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    bookings = session.get("bookings", [])
    session["bookings"] = [b for b in bookings if b["booking_id"] != booking_id]
    return redirect(url_for("my_bookings"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
