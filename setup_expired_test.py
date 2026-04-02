from app import app, db, Event, Ticket, User, TimeSlot
from datetime import datetime, timedelta

def setup_expired_event():
    with app.app_context():
        # Find or create a student
        student = User.query.filter_by(role='student').first()
        if not student:
            student = User(name="Test Student", email="student@test.com", password="password", role="student")
            db.session.add(student)
            db.session.commit()

        # Find or create a host
        host = User.query.filter_by(role='host').first()
        if not host:
            host = User(name="Test Host", email="host@test.com", password="password", role="host")
            db.session.add(host)
            db.session.commit()

        # Create an expired event
        expired_event = Event(
            name="Expired Event",
            location="Old Hall",
            start_time=datetime.utcnow() - timedelta(days=2),
            end_time=datetime.utcnow() - timedelta(days=1),
            max_capacity=100,
            host_id=host.id
        )
        db.session.add(expired_event)
        db.session.commit()

        # Create a time slot
        ts = TimeSlot(
            start_time=expired_event.start_time,
            end_time=expired_event.end_time,
            max_participants=100,
            event_id=expired_event.id
        )
        db.session.add(ts)
        db.session.commit()

        # Create a ticket for the expired event
        ticket = Ticket(
            event_id=expired_event.id,
            student_id=student.id,
            time_slot_id=ts.id,
            paid=True,
            qr_token="expired_token"
        )
        db.session.add(ticket)
        db.session.commit()
        
        print(f"Created expired event ID: {expired_event.id}")
        print(f"Created ticket ID: {ticket.id} for student: {student.email}")

if __name__ == "__main__":
    setup_expired_event()
