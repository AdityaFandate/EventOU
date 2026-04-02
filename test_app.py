import pytest
from app import app, db, User, Event, Ticket, FoodCoupon
from datetime import datetime, timedelta
import io

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create a test admin
        admin = User(name="Test Admin", email="admin@test.com", role="admin")
        admin.set_password("admin123")
        # Create a test host
        host = User(name="Test Host", email="host@test.com", role="host")
        host.set_password("host123")
        # Create a test student
        student = User(name="Test Student", email="student@test.com", role="student")
        student.set_password("student123")
        
        db.session.add_all([admin, host, student])
        db.session.commit()
        
        # Create a test event
        now = datetime.utcnow()
        event = Event(
            name="Test Event",
            location="Test Lab",
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=5),
            max_capacity=100,
            host_id=host.id
        )
        db.session.add(event)
        db.session.commit()
    
    with app.test_client() as client:
        yield client
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def test_landing_page(client):
    """Test if landing page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Smart Crowd Manager" in response.data

def test_admin_dashboard_access(client):
    """Test that only admin can access admin dashboard."""
    # Try as guest
    response = client.get('/admin/dashboard')
    assert response.status_code == 302 # Redirect to login
    
    # Login as admin
    login(client, "admin@test.com", "admin123")
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data

def test_host_event_creation(client):
    """Test that host can create an event."""
    login(client, "host@test.com", "host123")
    now = datetime.utcnow()
    data = {
        "name": "New Host Event",
        "location": "Host Hall",
        "start_time": (now + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
        "end_time": (now + timedelta(days=1, hours=2)).strftime("%Y-%m-%dT%H:%M"),
        "max_capacity": 50,
        "event_type": "technical"
    }
    response = client.post('/events/create', data=data, follow_redirects=True)
    assert b"Event created successfully" in response.data
    
    with app.app_context():
        event = Event.query.filter_by(name="New Host Event").first()
        assert event is not None
        assert event.location == "Host Hall"

def test_student_ticket_registration(client):
    """Test that student can register for a pass."""
    login(client, "student@test.com", "student123")
    with app.app_context():
        event = Event.query.first()
        event_id = event.id
        
    response = client.post(f'/events/{event_id}/tickets/create', data={"quantity": 1}, follow_redirects=True)
    assert b"Registration successful" in response.data
    
    with app.app_context():
        ticket = Ticket.query.filter_by(student_id=3).first() # student id is 3
        assert ticket is not None
        assert ticket.event_id == event_id

def test_qr_verification_api(client):
    """Test the QR verification API."""
    # Create a ticket first
    with app.app_context():
        student = User.query.filter_by(role="student").first()
        event = Event.query.first()
        ticket = Ticket(qr_token="test_token_123", event_id=event.id, student_id=student.id, paid=True)
        db.session.add(ticket)
        db.session.commit()
        
    # Test verification API
    login(client, "host@test.com", "host123")
    response = client.get('/api/verify/test_token_123')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['student_name'] == "Test Student"

def test_host_remove_user(client):
    """Test that host can remove a volunteer/faculty."""
    with app.app_context():
        volunteer = User(name="Test Volunteer", email="vol@test.com", role="volunteer")
        volunteer.set_password("vol123")
        db.session.add(volunteer)
        db.session.commit()
        volunteer_id = volunteer.id
        
    login(client, "host@test.com", "host123")
    response = client.post(f'/host/remove_user/{volunteer_id}', follow_redirects=True)
    assert b"removed successfully" in response.data
    
    with app.app_context():
        user = db.session.get(User, volunteer_id)
        assert user is None

def test_data_exports(client):
    """Test PDF and Excel export routes."""
    login(client, "host@test.com", "host123")
    
    # Test Entry Logs PDF
    response = client.get('/host/export_entry_logs_pdf')
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    
    # Test Entry Logs Excel
    response = client.get('/host/export_entry_logs_excel')
    assert response.status_code == 200
    assert response.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
