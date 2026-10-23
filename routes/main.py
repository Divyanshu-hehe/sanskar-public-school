from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import (
    db, AdminUser, AdmissionApplication, ContactInquiry,
    NewsArticle, SchoolEvent, FacultyProfile, GalleryItem,
    FAQ, DownloadableResource, WebsiteSetting
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_news = NewsArticle.query.filter_by(is_published=True).order_by(NewsArticle.created_at.desc()).limit(3).all()
    upcoming_events = SchoolEvent.query.order_by(SchoolEvent.created_at.desc()).limit(3).all()
    featured_faculty = FacultyProfile.query.order_by(FacultyProfile.display_order.asc()).limit(4).all()
    gallery_preview = GalleryItem.query.order_by(GalleryItem.display_order.asc()).limit(6).all()
    faqs_preview = FAQ.query.filter_by(is_active=True).order_by(FAQ.display_order.asc()).limit(4).all()
    
    return render_template(
        'index.html',
        featured_news=featured_news,
        upcoming_events=upcoming_events,
        featured_faculty=featured_faculty,
        gallery_preview=gallery_preview,
        faqs_preview=faqs_preview
    )

@main_bp.route('/about')
def about():
    leadership = FacultyProfile.query.filter_by(department='Leadership').order_by(FacultyProfile.display_order.asc()).all()
    return render_template('about.html', leadership=leadership)

@main_bp.route('/academics')
def academics():
    resources = DownloadableResource.query.filter_by(category='Syllabus').all()
    return render_template('academics.html', resources=resources)

@main_bp.route('/admissions')
def admissions():
    faqs = FAQ.query.filter_by(category='Admissions', is_active=True).all()
    forms = DownloadableResource.query.filter_by(category='Forms').all()
    return render_template('admissions.html', faqs=faqs, forms=forms)

@main_bp.route('/admission-status')
def admission_status():
    app_num = request.args.get('app_num', '').strip()
    application = None
    if app_num:
        application = AdmissionApplication.query.filter_by(application_number=app_num).first()
    return render_template('admission_status.html', application=application, searched_app_num=app_num)

@main_bp.route('/faculty')
def faculty():
    departments = ['All', 'Leadership', 'Science', 'Mathematics', 'Languages', 'Arts & Sports']
    selected_dept = request.args.get('dept', 'All')
    
    if selected_dept and selected_dept != 'All':
        faculty_members = FacultyProfile.query.filter_by(department=selected_dept).order_by(FacultyProfile.display_order.asc()).all()
    else:
        faculty_members = FacultyProfile.query.order_by(FacultyProfile.display_order.asc()).all()
        
    return render_template('faculty.html', faculty_members=faculty_members, departments=departments, selected_dept=selected_dept)

@main_bp.route('/facilities')
def facilities():
    return render_template('facilities.html')

@main_bp.route('/gallery')
def gallery():
    categories = ['All', 'Campus', 'Academics', 'Sports', 'Cultural', 'Celebrations']
    selected_cat = request.args.get('category', 'All')
    
    if selected_cat and selected_cat != 'All':
        items = GalleryItem.query.filter_by(category=selected_cat).order_by(GalleryItem.display_order.asc()).all()
    else:
        items = GalleryItem.query.order_by(GalleryItem.display_order.asc()).all()
        
    return render_template('gallery.html', items=items, categories=categories, selected_cat=selected_cat)

@main_bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'All')
    search = request.args.get('search', '').strip()
    
    query = NewsArticle.query.filter_by(is_published=True)
    if category != 'All':
        query = query.filter_by(category=category)
    if search:
        query = query.filter(NewsArticle.title.ilike(f'%{search}%') | NewsArticle.summary.ilike(f'%{search}%'))
        
    articles_pagination = query.order_by(NewsArticle.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    events = SchoolEvent.query.order_by(SchoolEvent.created_at.desc()).all()
    
    return render_template(
        'news.html',
        articles=articles_pagination.items,
        pagination=articles_pagination,
        events=events,
        selected_cat=category,
        search_query=search
    )

@main_bp.route('/news/<slug>')
def news_detail(slug):
    article = NewsArticle.query.filter_by(slug=slug, is_published=True).first_or_404()
    recent = NewsArticle.query.filter(NewsArticle.id != article.id, NewsArticle.is_published == True).order_by(NewsArticle.created_at.desc()).limit(3).all()
    return render_template('news_detail.html', article=article, recent=recent)

@main_bp.route('/student-life')
def student_life():
    return render_template('student_life.html')

@main_bp.route('/parent-resources')
def parent_resources():
    resources = DownloadableResource.query.order_by(DownloadableResource.category.asc()).all()
    return render_template('parent_resources.html', resources=resources)

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/faqs')
def faqs():
    categories = ['All', 'Admissions', 'Academics', 'Fees & Payments', 'Transport', 'Facilities', 'General']
    selected_cat = request.args.get('category', 'All')
    search = request.args.get('search', '').strip()
    
    query = FAQ.query.filter_by(is_active=True)
    if selected_cat != 'All':
        query = query.filter_by(category=selected_cat)
    if search:
        query = query.filter(FAQ.question.ilike(f'%{search}%') | FAQ.answer.ilike(f'%{search}%'))
        
    faqs_list = query.order_by(FAQ.display_order.asc()).all()
    return render_template('faqs.html', faqs=faqs_list, categories=categories, selected_cat=selected_cat, search=search)

@main_bp.route('/policies')
def policies():
    return render_template('policies.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = bool(request.form.get('remember'))

        user = AdminUser.query.filter(
            (AdminUser.username == username_or_email) | (AdminUser.email == username_or_email)
        ).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.login'))
