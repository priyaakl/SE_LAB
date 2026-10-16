"""Flight reservation system with booking and reporting features."""

import hashlib
import secrets
from pathlib import Path

flights = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

revenue = {"total": 0.0}


def book_flight_seat(
    flight_no,
    passenger,
    luggage_weight=15,
    baggage_tags=None,
):
    """Book an available seat and update booking information."""
    if baggage_tags is None:
        baggage_tags = []

    flight = flights.get(flight_no)
    if flight is None or flight["is_full"] or flight["seats"] <= 0:
        return False

    flight["seats"] -= 1
    if flight["seats"] <= 0:
        flight["is_full"] = True

    revenue["total"] += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger "
        f"{passenger} with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel a booking by restoring one seat when possible."""
    flight = flights.get(flight_no)

    if flight is None:
        return False

    if flight["seats"] >= 5:
        return False

    flight["seats"] += 1
    flight["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return whether a flight has an available seat."""
    flight = flights.get(flight_no)
    return flight is not None and not flight["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate=0.15):
    """Calculate a baggage surcharge using the flight fare."""
    flight = flights.get(flight_no)

    if flight is None:
        raise ValueError(f"Unknown flight number: {flight_no}")

    if not 0 <= surcharge_rate <= 1:
        raise ValueError("Surcharge rate must be between 0 and 1.")

    return flight["fare"] * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 digest of the passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit PIN using a secure random source."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write flight information to a manifest file."""
    manifest_path = Path(filename)
    manifest_path.write_text(str(flights), encoding="utf-8")
    print(f"Boarding manifest printed: {manifest_path.name}")


def get_flight_summary(flight_data):
    """Count flights that are not marked as full."""
    return sum(
        1
        for details in flight_data.values()
        if not details["is_full"]
    )


def main():
    """Run a demonstration of the flight reservation system."""
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")

    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101"))
    print(
        "Passenger Hash:",
        generate_passenger_hash("PASSPORT_IND_119"),
    )
    print("Boarding PIN:", generate_boarding_pin())

    export_flight_manifest()
    print("Available flights:", get_flight_summary(flights))


if __name__ == "__main__":
    main()
