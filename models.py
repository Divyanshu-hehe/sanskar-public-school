from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='admin')  # superadmin, admin, editor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class AdmissionApplication(db.Model):
    __tablename__ = 'admission_applications'

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    student_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    grade_applying = db.Column(db.String(50), nullable=False)
    
    parent_name = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(50), default='Father')
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    previous_school = db.Column(db.String(150))
    previous_grade = db.Column(db.String(50))
    previous_percentage = db.Column(db.String(20))
    additional_notes = db.Column(db.Text)
    
    status = db.Column(db.String(30), default='Pending')  # Pending, Under Review, Interview Scheduled, Approved, Rejected
    admin_remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'application_number': self.application_number,
            'student_name': self.student_name,
            'dob': self.dob,
            'gender': self.gender,
            'grade_applying': self.grade_applying,
            'parent_name': self.parent_name,
            'relationship': self.relationship,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'previous_school': self.previous_school,
            'previous_grade': self.previous_grade,
            'previous_percentage': self.previous_percentage,
            'status': self.status,
            'admin_remarks': self.admin_remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }


class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='New')  # New, In Progress, Resolved
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), default='General')  # Academic, Sports, Achievements, Notice, Celebration
    summary = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)
    published_date = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'category': self.category,
            'summary': self.summary,
            'content': self.content,
            'image_url': self.image_url,
            'is_published': self.is_published,
            'published_date': self.published_date or (self.created_at.strftime('%d %b, %Y') if self.created_at else ''),
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None
        }


class SchoolEvent(db.Model):
    __tablename__ = 'school_events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Event')
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.String(50), nullable=False)  # Display string e.g. "15 Nov 2026"
    event_time = db.Column(db.String(50))  # e.g. "09:00 AM - 02:00 PM"
    location = db.Column(db.String(150), default='School Campus Auditorium')
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'event_date': self.event_date,
            'event_time': self.event_time,
            'location': self.location,
            'image_url': self.image_url,
            'is_featured': self.is_featured
        }


class FacultyProfile(db.Model):
    __tablename__ = 'faculty_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(60), nullable=False)  # Leadership, Science, Mathematics, Languages, Social Sciences, Arts & Sports
    qualifications = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(50), default='10+ Years')
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    image_url = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'department': self.department,
            'qualifications': self.qualifications,
            'experience': self.experience,
            'bio': self.bio,
            'email': self.email,
            'image_url': self.image_url,
            'display_order': self.display_order
        }


class GalleryItem(db.Model):
    __tablename__ = 'gallery_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Campus, Academics, Sports, Cultural, Celebrations
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'image_url': self.image_url,
            'caption': self.caption,
            'display_order': self.display_order
        }


class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), default='General')  # Admissions, Academics, Fees, Facilities, General
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'question': self.question,
            'answer': self.answer,
            'display_order': self.display_order,
            'is_active': self.is_active
        }


class DownloadableResource(db.Model):
    __tablename__ = 'downloadable_resources'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Forms, Calendar, Syllabus, Fees, Guidelines
    description = db.Column(db.String(300))
    file_url = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(30), default='PDF (250 KB)')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'updated_at': self.updated_at.strftime('%b %Y') if self.updated_at else 'Recent'
        }


class WebsiteSetting(db.Model):
    __tablename__ = 'website_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))

    @staticmethod
    def get_setting(key, default=''):
        item = WebsiteSetting.query.filter_by(key=key).first()
        return item.value if item else default

    @staticmethod
    def set_setting(key, value, description=None):
        item = WebsiteSetting.query.filter_by(key=key).first()
        if not item:
            item = WebsiteSetting(key=key, value=value, description=description)
            db.session.add(item)
        else:
            item.value = value
            if description:
                item.description = description
        db.session.commit()
