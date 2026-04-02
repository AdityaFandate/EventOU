from app import app, Ticket, User, Event
from datetime import datetime

def verify_student_dashboard_expired():
    with app.app_context():
        now = datetime.utcnow()
        # Find the student with the expired ticket
        student = User.query.filter_by(email="student1@college.edu").first()
        if not student:
            print("Student not found")
            return

        tickets = Ticket.query.filter_by(student_id=student.id).all()
        print(f"Total tickets for student: {len(tickets)}")
        for t in tickets:
            is_expired = t.event.end_time < now
            print(f"Ticket for event: {t.event.name}, Expired: {is_expired}")

if __name__ == "__main__":
    verify_student_dashboard_expired()
