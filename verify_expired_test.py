from app import app, Event, Ticket, User
from datetime import datetime

def verify_expired_event_hidden():
    with app.app_context():
        now = datetime.utcnow()
        # Get active events from listing logic
        active_events = Event.query.filter(Event.end_time >= now).all()
        expired_events = Event.query.filter(Event.end_time < now).all()
        
        print(f"Total events in DB: {Event.query.count()}")
        print(f"Active events count (should not include 'Expired Event'): {len(active_events)}")
        for e in active_events:
            print(f"Active Event: {e.name}")
            if e.name == "Expired Event":
                print("FAILURE: Expired Event found in active events!")

        print(f"Expired events count: {len(expired_events)}")
        for e in expired_events:
            print(f"Expired Event: {e.name}")

if __name__ == "__main__":
    verify_expired_event_hidden()
