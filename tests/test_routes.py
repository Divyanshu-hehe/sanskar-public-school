import pytest
from app import create_app
from models import db, AdminUser, AdmissionApplication, ContactInquiry
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Seed test admin
        admin = AdminUser(username='testadmin', email='test@sanskar.in', role='admin')
        admin.set_password('TestPass123!')
        db.session.add(admin)
        db.session.commit()
        
        with app.test_client() as client:
            yield client
            
        db.session.remove()
        db.drop_all()

def test_public_pages_render(client):
    routes = [
        '/',
        '/about',
        '/academics',
        '/admissions',
        '/admission-status',
        '/faculty',
        '/facilities',
        '/gallery',
        '/news',
        '/student-life',
        '/parent-resources',
        '/contact',
        '/faqs',
        '/policies',
        '/login'
    ]
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} failed with status {response.status_code}"

def test_api_news_and_events(client):
    res_news = client.get('/api/news')
    assert res_news.status_code == 200
    assert res_news.json['success'] is True

    res_events = client.get('/api/events')
    assert res_events.status_code == 200
    assert res_events.json['success'] is True

def test_api_faculty_and_gallery(client):
    res_faculty = client.get('/api/faculty')
    assert res_faculty.status_code == 200
    assert res_faculty.json['success'] is True

    res_gallery = client.get('/api/gallery')
    assert res_gallery.status_code == 200
    assert res_gallery.json['success'] is True

def test_admission_submission_and_tracking(client):
    payload = {
        'student_name': 'Kavya Singh',
        'dob': '2017-06-15',
        'gender': 'Female',
        'grade_applying': 'Class 4',
        'parent_name': 'Vikram Singh',
        'relationship': 'Father',
        'phone': '9876501234',
        'email': 'vikram.singh@example.com',
        'address': 'Sector 15, Green Park',
        'previous_school': 'National Academy',
        'previous_percentage': '91%'
    }
    
    # POST admission
    response = client.post('/api/admissions', json=payload)
    assert response.status_code == 201
    data = response.json
    assert data['success'] is True
    assert 'application_number' in data
    app_num = data['application_number']

    # GET status
    status_res = client.get(f'/api/admissions/status/{app_num}')
    assert status_res.status_code == 200
    assert status_res.json['data']['student_name'] == 'Kavya Singh'
    assert status_res.json['data']['status'] == 'Pending'

def test_contact_inquiry_submission(client):
    payload = {
        'name': 'Anita Roy',
        'email': 'anita.roy@example.com',
        'phone': '9876543210',
        'subject': 'Bus Route Inquiry',
        'message': 'Kindly inform if transport covers Palm Avenue.'
    }
    response = client.post('/api/contact', json=payload)
    assert response.status_code == 201
    assert response.json['success'] is True

def test_admin_authentication_barrier(client):
    # Unauthenticated access to admin dashboard should redirect to login
    response = client.get('/admin/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_admin_login_and_dashboard_access(client):
    login_res = client.post('/login', data={
        'username': 'testadmin',
        'password': 'TestPass123!'
    }, follow_redirects=True)
    assert login_res.status_code == 200
    assert b'Dashboard Overview' in login_res.data

def test_contact_and_social_links(client):
    res = client.get('/contact')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'sanskarpublicskl2000@gmail.com' in html
    assert '79790 48493' in html or '7979048493' in html
    assert 'https://www.instagram.com/sanskarpublicskl1/?hl=en' in html
    assert 'https://www.youtube.com/@SANSKARPublicschool-en1/shorts' in html
    assert 'MGW7+J27, Bongawar, Bharechnagar, Jharkhand 829117' in html
    assert 'facebook' not in html.lower()

def test_updated_requirements(client):
    # Check index page for academic year, 500+ students, and Pre-Primary grades
    res_index = client.get('/')
    assert res_index.status_code == 200
    html_index = res_index.data.decode('utf-8')
    assert '2027 – 2028' in html_index or '2027-28' in html_index
    assert '500+' in html_index
    assert 'Play Group • Nursery • LKG • UKG' in html_index
    assert 'Class 9 – 10' in html_index
    assert 'facebook' not in html_index.lower()

    # Check admissions page for Play Group, Nursery, LKG, UKG, Class 1-10
    res_adm = client.get('/admissions')
    assert res_adm.status_code == 200
    html_adm = res_adm.data.decode('utf-8')
    assert 'Play Group' in html_adm
    assert 'Class 10' in html_adm
    assert 'Class 11 (Science)' not in html_adm

    # Check student life: no Four Pillars of School Spirit, no Robotics
    res_life = client.get('/student-life')
    assert res_life.status_code == 200
    html_life = res_life.data.decode('utf-8')
    assert 'Four Pillars of School Spirit' not in html_life
    assert 'Robotics' not in html_life
    assert 'Clubs & Co-Curricular Societies' not in html_life

    # Check journey in about page: 2018 foundation, 500+ enrolled
    res_about = client.get('/about')
    assert res_about.status_code == 200
    html_about = res_about.data.decode('utf-8')
    assert '2018' in html_about
    assert 'Foundation of Sanskar' in html_about
    assert '500+' in html_about
