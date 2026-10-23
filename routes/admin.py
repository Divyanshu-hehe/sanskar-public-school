import os
import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import (
    db, AdminUser, AdmissionApplication, ContactInquiry,
    NewsArticle, SchoolEvent, FacultyProfile, GalleryItem,
    FAQ, DownloadableResource, WebsiteSetting
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def check_admin():
    # Enforce login for all admin routes
    pass

@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    stats = {
        'total_admissions': AdmissionApplication.query.count(),
        'pending_admissions': AdmissionApplication.query.filter_by(status='Pending').count(),
        'approved_admissions': AdmissionApplication.query.filter_by(status='Approved').count(),
        'total_inquiries': ContactInquiry.query.count(),
        'new_inquiries': ContactInquiry.query.filter_by(status='New').count(),
        'total_news': NewsArticle.query.count(),
        'total_faculty': FacultyProfile.query.count(),
        'total_gallery': GalleryItem.query.count(),
        'total_faqs': FAQ.query.count(),
        'total_downloads': DownloadableResource.query.count()
    }
    recent_admissions = AdmissionApplication.query.order_by(AdmissionApplication.created_at.desc()).limit(5).all()
    recent_inquiries = ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_admissions=recent_admissions,
        recent_inquiries=recent_inquiries
    )

# --- Admissions Management ---
@admin_bp.route('/admissions')
def admissions():
    status = request.args.get('status', 'All')
    search = request.args.get('search', '').strip()
    query = AdmissionApplication.query
    
    if status != 'All':
        query = query.filter_by(status=status)
    if search:
        query = query.filter(
            AdmissionApplication.student_name.ilike(f'%{search}%') |
            AdmissionApplication.application_number.ilike(f'%{search}%') |
            AdmissionApplication.parent_name.ilike(f'%{search}%') |
            AdmissionApplication.phone.ilike(f'%{search}%')
        )
    
    applications = query.order_by(AdmissionApplication.created_at.desc()).all()
    return render_template('admin/admissions.html', applications=applications, current_status=status, search=search)

@admin_bp.route('/admissions/<int:id>/update-status', methods=['POST'])
def update_admission_status(id):
    app = AdmissionApplication.query.get_or_404(id)
    new_status = request.form.get('status')
    remarks = request.form.get('admin_remarks')
    
    if new_status:
        app.status = new_status
    if remarks is not None:
        app.admin_remarks = remarks
        
    db.session.commit()
    flash(f'Application {app.application_number} updated to {app.status}.', 'success')
    return redirect(request.referrer or url_for('admin.admissions'))

@admin_bp.route('/admissions/<int:id>/delete', methods=['POST'])
def delete_admission(id):
    app = AdmissionApplication.query.get_or_404(id)
    num = app.application_number
    db.session.delete(app)
    db.session.commit()
    flash(f'Application {num} deleted.', 'info')
    return redirect(url_for('admin.admissions'))

# --- Inquiries Management ---
@admin_bp.route('/inquiries')
def inquiries():
    status = request.args.get('status', 'All')
    query = ContactInquiry.query
    if status != 'All':
        query = query.filter_by(status=status)
    inquiries_list = query.order_by(ContactInquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries_list, current_status=status)

@admin_bp.route('/inquiries/<int:id>/update', methods=['POST'])
def update_inquiry(id):
    inquiry = ContactInquiry.query.get_or_404(id)
    inquiry.status = request.form.get('status', inquiry.status)
    inquiry.admin_notes = request.form.get('admin_notes', inquiry.admin_notes)
    db.session.commit()
    flash('Inquiry status updated successfully.', 'success')
    return redirect(url_for('admin.inquiries'))

# --- News & Announcements Management ---
@admin_bp.route('/news')
def news():
    articles = NewsArticle.query.order_by(NewsArticle.created_at.desc()).all()
    return render_template('admin/news.html', articles=articles)

@admin_bp.route('/news/add', methods=['POST'])
def add_news():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'General')
    summary = request.form.get('summary', '').strip()
    content = request.form.get('content', '').strip()
    image_url = request.form.get('image_url', '/static/images/hero/hero_classroom.jpg').strip()
    
    if not title or not summary or not content:
        flash('Please fill in title, summary, and content.', 'error')
        return redirect(url_for('admin.news'))
        
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    if NewsArticle.query.filter_by(slug=slug).first():
        slug = f"{slug}-{int(datetime.utcnow().timestamp())}"

    article = NewsArticle(
        title=title,
        slug=slug,
        category=category,
        summary=summary,
        content=content,
        image_url=image_url,
        is_published=True,
        published_date=datetime.now().strftime('%d %b, %Y')
    )
    db.session.add(article)
    db.session.commit()
    flash('News article published successfully!', 'success')
    return redirect(url_for('admin.news'))

@admin_bp.route('/news/<int:id>/delete', methods=['POST'])
def delete_news(id):
    article = NewsArticle.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('News article deleted.', 'info')
    return redirect(url_for('admin.news'))

# --- Events Management ---
@admin_bp.route('/events')
def events():
    events_list = SchoolEvent.query.order_by(SchoolEvent.created_at.desc()).all()
    return render_template('admin/events.html', events=events_list)

@admin_bp.route('/events/add', methods=['POST'])
def add_event():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'Event')
    description = request.form.get('description', '').strip()
    event_date = request.form.get('event_date', '').strip()
    event_time = request.form.get('event_time', '').strip()
    location = request.form.get('location', 'Campus Auditorium').strip()
    image_url = request.form.get('image_url', '/static/images/facilities/sports.jpg').strip()

    if not title or not description or not event_date:
        flash('Title, description and date are required.', 'error')
        return redirect(url_for('admin.events'))

    event = SchoolEvent(
        title=title,
        category=category,
        description=description,
        event_date=event_date,
        event_time=event_time,
        location=location,
        image_url=image_url
    )
    db.session.add(event)
    db.session.commit()
    flash('School event added successfully.', 'success')
    return redirect(url_for('admin.events'))

@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
def delete_event(id):
    event = SchoolEvent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('admin.events'))

# --- Faculty Management ---
@admin_bp.route('/faculty')
def faculty():
    faculty_list = FacultyProfile.query.order_by(FacultyProfile.display_order.asc()).all()
    return render_template('admin/faculty.html', faculty_list=faculty_list)

@admin_bp.route('/faculty/add', methods=['POST'])
def add_faculty():
    name = request.form.get('name', '').strip()
    designation = request.form.get('designation', '').strip()
    department = request.form.get('department', 'Science')
    qualifications = request.form.get('qualifications', '').strip()
    experience = request.form.get('experience', '5+ Years').strip()
    email = request.form.get('email', '').strip()
    bio = request.form.get('bio', '').strip()
    image_url = request.form.get('image_url', '/static/images/faculty/principal.jpg').strip()

    if not name or not designation or not qualifications:
        flash('Name, designation and qualifications are required.', 'error')
        return redirect(url_for('admin.faculty'))

    member = FacultyProfile(
        name=name,
        designation=designation,
        department=department,
        qualifications=qualifications,
        experience=experience,
        email=email,
        bio=bio,
        image_url=image_url
    )
    db.session.add(member)
    db.session.commit()
    flash('Faculty member added successfully.', 'success')
    return redirect(url_for('admin.faculty'))

@admin_bp.route('/faculty/<int:id>/delete', methods=['POST'])
def delete_faculty(id):
    f = FacultyProfile.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash('Faculty profile removed.', 'info')
    return redirect(url_for('admin.faculty'))

# --- Gallery Management ---
@admin_bp.route('/gallery')
def gallery():
    items = GalleryItem.query.order_by(GalleryItem.display_order.asc()).all()
    return render_template('admin/gallery.html', items=items)

@admin_bp.route('/gallery/add', methods=['POST'])
def add_gallery():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'Campus')
    image_url = request.form.get('image_url', '').strip()
    caption = request.form.get('caption', '').strip()

    if not title or not image_url:
        flash('Title and image URL are required.', 'error')
        return redirect(url_for('admin.gallery'))

    item = GalleryItem(title=title, category=category, image_url=image_url, caption=caption)
    db.session.add(item)
    db.session.commit()
    flash('Gallery photo added.', 'success')
    return redirect(url_for('admin.gallery'))

@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
def delete_gallery(id):
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item removed.', 'info')
    return redirect(url_for('admin.gallery'))

# --- FAQ Management ---
@admin_bp.route('/faqs')
def faqs():
    faqs_list = FAQ.query.order_by(FAQ.display_order.asc()).all()
    return render_template('admin/faqs.html', faqs=faqs_list)

@admin_bp.route('/faqs/add', methods=['POST'])
def add_faq():
    category = request.form.get('category', 'General')
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()

    if not question or not answer:
        flash('Question and answer are required.', 'error')
        return redirect(url_for('admin.faqs'))

    faq = FAQ(category=category, question=question, answer=answer)
    db.session.add(faq)
    db.session.commit()
    flash('FAQ created successfully.', 'success')
    return redirect(url_for('admin.faqs'))

@admin_bp.route('/faqs/<int:id>/delete', methods=['POST'])
def delete_faq(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ removed.', 'info')
    return redirect(url_for('admin.faqs'))

# --- Downloads / Resources ---
@admin_bp.route('/downloads')
def downloads():
    resources = DownloadableResource.query.order_by(DownloadableResource.category.asc()).all()
    return render_template('admin/downloads.html', resources=resources)

@admin_bp.route('/downloads/add', methods=['POST'])
def add_download():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'Forms')
    description = request.form.get('description', '').strip()
    file_url = request.form.get('file_url', '#').strip()
    file_size = request.form.get('file_size', 'PDF (300 KB)').strip()

    if not title:
        flash('Resource title is required.', 'error')
        return redirect(url_for('admin.downloads'))

    res = DownloadableResource(
        title=title,
        category=category,
        description=description,
        file_url=file_url,
        file_size=file_size
    )
    db.session.add(res)
    db.session.commit()
    flash('Downloadable resource added.', 'success')
    return redirect(url_for('admin.downloads'))

@admin_bp.route('/downloads/<int:id>/delete', methods=['POST'])
def delete_download(id):
    res = DownloadableResource.query.get_or_404(id)
    db.session.delete(res)
    db.session.commit()
    flash('Resource removed.', 'info')
    return redirect(url_for('admin.downloads'))

# --- Website Settings ---
@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        for key in request.form:
            WebsiteSetting.set_setting(key, request.form[key])
        flash('Website settings saved successfully!', 'success')
        return redirect(url_for('admin.settings'))

    all_settings = {s.key: s.value for s in WebsiteSetting.query.all()}
    return render_template('admin/settings.html', settings=all_settings)
