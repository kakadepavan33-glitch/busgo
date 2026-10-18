
from flask import Flask, render_template, request, abort
import sqlite3

app = Flask(__name__)
DATABASE = "busgo.db"


BUSES = [
    {"id": 101, "name": "Shivneri Express", "source": "Pune",
     "destination": "Mumbai", "departure": "06:00",
     "fare": 450, "seats": 20, "duration": 240},

    {"id": 102, "name": "City Travels", "source": "Pune",
     "destination": "Mumbai", "departure": "08:30",
     "fare": 350, "seats": 12, "duration": 300},

    {"id": 103, "name": "Royal Bus", "source": "Pune",
     "destination": "Nashik", "departure": "07:00",
     "fare": 500, "seats": 15, "duration": 300},

    {"id": 104, "name": "Metro Travels", "source": "Mumbai",
     "destination": "Pune", "departure": "09:00",
     "fare": 400, "seats": 18, "duration": 260},

    {"id": 105, "name": "Green Line", "source": "Pune",
     "destination": "Mumbai", "departure": "11:00",
     "fare": 300, "seats": 8, "duration": 320},

    {"id": 106, "name": "Deccan Express", "source": "Pune",
     "destination": "Kolhapur", "departure": "07:30",
     "fare": 400, "seats": 20, "duration": 300},

    {"id": 107, "name": "Sai Travels", "source": "Pune",
     "destination": "Goa", "departure": "21:00",
     "fare": 900, "seats": 25, "duration": 600},

    {"id": 108, "name": "Orange Travels", "source": "Pune",
     "destination": "Nagpur", "departure": "20:00",
     "fare": 1000, "seats": 30, "duration": 720},

    {"id": 109, "name": "Maharashtra Express", "source": "Mumbai",
     "destination": "Nashik", "departure": "08:00",
     "fare": 350, "seats": 20, "duration": 240},

    {"id": 110, "name": "Royal Rajasthan", "source": "Mumbai",
     "destination": "Ahmedabad", "departure": "22:00",
     "fare": 800, "seats": 25, "duration": 540},

    {"id": 111, "name": "Intercity Travels", "source": "Mumbai",
     "destination": "Goa", "departure": "19:00",
     "fare": 850, "seats": 22, "duration": 720},

    {"id": 112, "name": "Orange City Bus", "source": "Nagpur",
     "destination": "Pune", "departure": "18:00",
     "fare": 950, "seats": 25, "duration": 720},

    {"id": 113, "name": "Coastal Express", "source": "Goa",
     "destination": "Pune", "departure": "20:30",
     "fare": 850, "seats": 20, "duration": 600},

    {"id": 114, "name": "Kolhapur Travels", "source": "Kolhapur",
     "destination": "Mumbai", "departure": "09:00",
     "fare": 500, "seats": 20, "duration": 420},

    {"id": 115, "name": "Nashik Express", "source": "Nashik",
     "destination": "Pune", "departure": "10:00",
     "fare": 400, "seats": 18, "duration": 300},

    {"id": 116, "name": "Ahmedabad Express", "source": "Ahmedabad",
     "destination": "Mumbai", "departure": "21:00",
     "fare": 750, "seats": 25, "duration": 480},

    {"id": 117, "name": "Bengaluru Travels", "source": "Pune",
     "destination": "Bengaluru", "departure": "19:30",
     "fare": 1200, "seats": 30, "duration": 720},

    {"id": 118, "name": "Hyderabad Express", "source": "Pune",
     "destination": "Hyderabad", "departure": "20:00",
     "fare": 1100, "seats": 25, "duration": 600},

    {"id": 119, "name": "Indore Travels", "source": "Mumbai",
     "destination": "Indore", "departure": "18:30",
     "fare": 1000, "seats": 24, "duration": 720},

    {"id": 120, "name": "Delhi Express", "source": "Mumbai",
     "destination": "Delhi", "departure": "17:00",
     "fare": 1800, "seats": 35, "duration": 1080},
]


# Database setup
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bus_id INTEGER NOT NULL,
                seat INTEGER NOT NULL,
                passenger TEXT NOT NULL,
                UNIQUE(bus_id, seat)
            )
        """)


initialize_db()


# DSA 1: Linear Search
def linear_search_buses(buses, source, destination):
    results = []

    for bus in buses:
        if (
            bus["source"].lower() == source.lower()
            and bus["destination"].lower() == destination.lower()
        ):
            results.append(bus)

    return results


# DSA 2: Merge Sort
def merge_sort(buses, key):
    if len(buses) <= 1:
        return buses

    middle = len(buses) // 2
    left = merge_sort(buses[:middle], key)
    right = merge_sort(buses[middle:], key)

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def find_bus(bus_id):
    for bus in BUSES:
        if bus["id"] == bus_id:
            return bus
    return None


def get_seats(bus):
    with get_db() as db:
        rows = db.execute(
            "SELECT seat FROM bookings WHERE bus_id = ?",
            (bus["id"],)
        ).fetchall()

    booked_numbers = {row["seat"] for row in rows}

    return [
        {"number": number, "booked": number in booked_numbers}
        for number in range(1, bus["seats"] + 1)
    ]


@app.route("/", methods=["GET", "POST"])
def home():
    source = request.values.get("source", "Pune").strip()
    destination = request.values.get("destination", "Mumbai").strip()
    sort_by = request.values.get("sort_by", "fare")

    # Apply Linear Search
    results = linear_search_buses(BUSES, source, destination)

    # Apply Merge Sort
    allowed_keys = {"fare", "departure", "duration", "seats"}
    if sort_by not in allowed_keys:
        sort_by = "fare"

    results = merge_sort(results, sort_by)

    return render_template(
        "index.html",
        buses=results,
        source=source,
        destination=destination,
        sort_by=sort_by
    )


# Display available seats
@app.route("/seats/<int:bus_id>")
def seats_page(bus_id):
    bus = find_bus(bus_id)

    if bus is None:
        abort(404)

    return render_template(
        "seats.html",
        bus=bus,
        seats=get_seats(bus),
        error=None
    )


# Book a seat
@app.route("/book/<int:bus_id>", methods=["POST"])
def book_bus(bus_id):
    bus = find_bus(bus_id)

    if bus is None:
        abort(404)

    passenger = request.form.get("passenger", "").strip()

    try:
        seat = int(request.form.get("seat", ""))
    except ValueError:
        seat = 0

    if not passenger or len(passenger) > 80:
        error = "Enter a passenger name (maximum 80 characters)."
    elif seat < 1 or seat > bus["seats"]:
        error = "Please select a valid seat."
    else:
        try:
            with get_db() as db:
                cursor = db.execute(
                    """INSERT INTO bookings (bus_id, seat, passenger)
                       VALUES (?, ?, ?)""",
                    (bus_id, seat, passenger)
                )
                booking_id = cursor.lastrowid

            booking = {
                "id": booking_id,
                "passenger": passenger,
                "bus_name": bus["name"],
                "source": bus["source"],
                "destination": bus["destination"],
                "departure": bus["departure"],
                "seat": seat,
                "fare": bus["fare"]
            }

            return render_template(
                "confirmation.html", booking=booking
            )

        except sqlite3.IntegrityError:
            error = "This seat is already booked. Please choose another."

    return render_template(
        "seats.html",
        bus=bus,
        seats=get_seats(bus),
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
