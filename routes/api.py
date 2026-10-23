import re
import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import (
    db, AdmissionApplication, ContactInquiry,
    NewsArticle, SchoolEvent, FacultyProfile, GalleryItem,
    FAQ, DownloadableResource, WebsiteSetting
)

api_bp = Blueprint('api', __name__, url_prefix='/api')

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@api_bp.route('/news', methods=['GET'])
def get_news():
    category = request.args.get('category')
    limit = request.args.get('limit', type=int)
    query = NewsArticle.query.filter_by(is_published=True)
    if category and category != 'All':
        query = query.filter_by(category=category)
    query = query.order_by(NewsArticle.created_at.desc())
    if limit:
        query = query.limit(limit)
    articles = [a.to_dict() for a in query.all()]
    return jsonify({'success': True, 'count': len(articles), 'data': articles})

@api_bp.route('/events', methods=['GET'])
def get_events():
    limit = request.args.get('limit', type=int)
    featured = request.args.get('featured')
    query = SchoolEvent.query
    if featured == 'true':
        query = query.filter_by(is_featured=True)
    query = query.order_by(SchoolEvent.created_at.desc())
    if limit:
        query = query.limit(limit)
    events = [e.to_dict() for e in query.all()]
    return jsonify({'success': True, 'count': len(events), 'data': events})

@api_bp.route('/faculty', methods=['GET'])
def get_faculty():
    dept = request.args.get('dept')
    query = FacultyProfile.query
    if dept and dept != 'All':
        query = query.filter_by(department=dept)
    query = query.order_by(FacultyProfile.display_order.asc())
    faculty_list = [f.to_dict() for f in query.all()]
    return jsonify({'success': True, 'count': len(faculty_list), 'data': faculty_list})

@api_bp.route('/gallery', methods=['GET'])
def get_gallery():
    cat = request.args.get('category')
    query = GalleryItem.query
    if cat and cat != 'All':
        query = query.filter_by(category=cat)
    query = query.order_by(GalleryItem.display_order.asc())
    items = [g.to_dict() for g in query.all()]
    return jsonify({'success': True, 'count': len(items), 'data': items})

@api_bp.route('/faqs', methods=['GET'])
def get_faqs():
    cat = request.args.get('category')
    query_str = request.args.get('q', '').strip()
    query = FAQ.query.filter_by(is_active=True)
    if cat and cat != 'All':
        query = query.filter_by(category=cat)
    if query_str:
        query = query.filter(FAQ.question.ilike(f'%{query_str}%') | FAQ.answer.ilike(f'%{query_str}%'))
    query = query.order_by(FAQ.display_order.asc())
    faqs = [f.to_dict() for f in query.all()]
    return jsonify({'success': True, 'count': len(faqs), 'data': faqs})

@api_bp.route('/resources', methods=['GET'])
def get_resources():
    cat = request.args.get('category')
    query = DownloadableResource.query
    if cat:
        query = query.filter_by(category=cat)
    res = [r.to_dict() for r in query.all()]
    return jsonify({'success': True, 'count': len(res), 'data': res})

@api_bp.route('/admissions', methods=['POST'])
def submit_admission():
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Required validation
    required_fields = ['student_name', 'dob', 'gender', 'grade_applying', 'parent_name', 'phone', 'email', 'address']
    missing = [f for f in required_fields if not data.get(f) or not str(data.get(f)).strip()]
    if missing:
        return jsonify({
            'success': False,
            'message': f"Please fill all required fields: {', '.join(missing).replace('_', ' ').title()}"
        }), 400

    email = data.get('email', '').strip()
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    phone = data.get('phone', '').strip()
    if len(re.sub(r'\D', '', phone)) < 10:
        return jsonify({'success': False, 'message': 'Please enter a valid 10-digit phone number.'}), 400

    # Generate unique application number: SPS-2026-XXXX
    year = datetime.now().year
    rand_id = random.randint(1000, 9999)
    app_number = f"SPS-{year}-{rand_id}"
    while AdmissionApplication.query.filter_by(application_number=app_number).first():
        rand_id = random.randint(1000, 9999)
        app_number = f"SPS-{year}-{rand_id}"

    new_app = AdmissionApplication(
        application_number=app_number,
        student_name=data.get('student_name', '').strip(),
        dob=data.get('dob', '').strip(),
        gender=data.get('gender', '').strip(),
        grade_applying=data.get('grade_applying', '').strip(),
        parent_name=data.get('parent_name', '').strip(),
        relationship=data.get('relationship', 'Parent').strip(),
        phone=phone,
        email=email,
        address=data.get('address', '').strip(),
        previous_school=data.get('previous_school', '').strip(),
        previous_grade=data.get('previous_grade', '').strip(),
        previous_percentage=data.get('previous_percentage', '').strip(),
        additional_notes=data.get('additional_notes', '').strip(),
        status='Pending'
    )

    try:
        db.session.add(new_app)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Admission application submitted successfully!',
            'application_number': app_number,
            'student_name': new_app.student_name,
            'grade_applying': new_app.grade_applying
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'A database error occurred. Please try again.'}), 500

@api_bp.route('/admissions/status/<app_number>', methods=['GET'])
def get_admission_status(app_number):
    app = AdmissionApplication.query.filter_by(application_number=app_number.strip()).first()
    if not app:
        return jsonify({'success': False, 'message': 'Application not found. Please verify your reference number.'}), 404
    return jsonify({
        'success': True,
        'data': {
            'application_number': app.application_number,
            'student_name': app.student_name,
            'grade_applying': app.grade_applying,
            'parent_name': app.parent_name,
            'status': app.status,
            'created_at': app.created_at.strftime('%d %B, %Y') if app.created_at else '',
            'admin_remarks': app.admin_remarks or 'Your application is currently under preliminary review.'
        }
    })

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not subject or not message:
        return jsonify({'success': False, 'message': 'Please fill all required fields.'}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    inquiry = ContactInquiry(
        name=name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
        status='New'
    )

    try:
        db.session.add(inquiry)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Thank you! Your message has been received. Our office will respond within 24 hours.'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Unable to process your message at this time.'}), 500
