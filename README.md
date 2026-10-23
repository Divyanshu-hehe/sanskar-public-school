# Sanskar Public School — Complete Full-Stack Website

A full-stack, responsive web application for **Sanskar Public School**, built with a deep forest green and gold palette (`#004B35`, `#003B2D`, `#F4B900`), inspired by the institutional reference design and official school emblem with the Sanskrit motto: *"विद्या ददाति विनयम्"*.

---

## 🌟 Key Features

### 🏛️ Public School Website (13+ Pages)
1. **Home (`/`)**:
   - Top information bar with phone, email, motto, and social channels.
   - Dynamic notice ticker for active circulars and announcements.
   - Hero section with schoolchildren in class, headline *"Nurturing Knowledge. Building Character."*, and floating golden badge *"Better Students, Brighter Tomorrows"*.
   - Floating quick-access cards bar (Admissions, Academic Calendar, Fee Structure, Downloads, Parent Portal, Virtual Tour).
   - About Sanskar section with campus photo and 4 dynamic statistics cards (1000+ Students, 50+ Dedicated Faculty, 25+ Years of Excellence, 100% Focus on Values).
   - Academic program cards (Pre-Primary, Primary, Middle School, Senior Secondary).
   - World-class facilities strip (Classrooms, Labs, Library, Sports, Smart Learning, Safety).
   - Latest news and upcoming events calendar.
   - "Join the Sanskar Family" admissions call-to-action banner.
   - Comprehensive footer with quick links, contacts, social media, and policy links.

2. **About Us (`/about`)**:
   - Institutional heritage, vision, mission, and core values (*Satya, Shresthata, Vinamrata, Sahayata*).
   - Principal's address by Dr. Arvind Sharma with portrait and credentials.
   - Historical milestones timeline from 2001 to present.

3. **Academics (`/academics`)**:
   - In-depth breakdown of Pre-Primary, Primary, Middle School, and Senior Secondary (Science, Commerce, Humanities).
   - Teaching methodologies (Smart Classrooms, Experiential Inquiry, Continuous Evaluation).
   - Downloadable curriculum outlines.

4. **Admissions (`/admissions`)**:
   - 4-step streamlined admission workflow.
   - Age criteria table aligned with NEP recommendations.
   - Required documents checklist.
   - Interactive AJAX application form with live validation and unique application number generation (`SPS-2026-XXXX`).

5. **Application Status Tracking (`/admission-status`)**:
   - Search by application reference number (e.g., `SPS-2026-1001`).
   - Live status display (Pending, Under Review, Approved, Rejected) with counselor remarks.

6. **Dedicated Faculty (`/faculty`)**:
   - Department filter tabs (All, Leadership, Science, Mathematics, Languages, Arts & Sports).
   - Educator cards with photos, designations, qualifications, and experience.

7. **World-Class Facilities (`/facilities`)**:
   - Spacious smart classrooms, composite science labs, coding & AI lab, central knowledge library, multi-sport arena, GPS buses, medical infirmary.

8. **Photo Gallery (`/gallery`)**:
   - Category filtering (Campus, Academics, Sports, Cultural, Celebrations).
   - Fullscreen lightbox modal with Previous/Next controls, image counters, and keyboard navigation.

9. **News & Events (`/news` & `/news/<slug>`)**:
   - Search bar and category filters.
   - Pagination controls.
   - Detailed news article reader with social share buttons.
   - Upcoming events calendar with dates, times, and venues.

10. **Student Life (`/student-life`)**:
    - The Four Houses (*Agni, Vayu, Prithvi, Jal*).
    - 6 student co-curricular clubs (Robotics, Debate, Art & Pottery, Nature, Music, Social Service).

11. **Parent Resources (`/parent-resources`)**:
    - Parent ERP Connect guide.
    - Downloadable forms (Registration, Calendar, Syllabus, Dress Code, Code of Conduct).
    - Fee structure and payment policy guidelines.

12. **Contact Us (`/contact`)**:
    - Interactive contact inquiry form with database logging.
    - Campus address, telephone lines, inquiry emails, and office working hours.
    - Embedded interactive Google Map and directions link.

13. **Frequently Asked Questions (`/faqs`)**:
    - Searchable expandable accordion interface categorized by Admissions, Academics, Fees, Transport, and Facilities.

14. **School Policies (`/policies`)**:
    - Privacy Policy, Website Terms, Student Code of Conduct, Attendance Policy, Child Safeguarding (CPC/POSH), and WCAG Accessibility Statement.

---

### 🛡️ Secure Admin Portal (`/admin`)
- **Protected with authentication** (`@login_required`).
- **Dashboard Overview (`/admin/dashboard`)**:
  - Live metric counters for Total Admissions, Pending Review, Inquiries, Faculty, News, Gallery items, FAQs, and Downloads.
  - Recent admission submissions table with quick review links.
  - Recent parent inquiries log.
- **Admissions Management (`/admin/admissions`)**:
  - Filter by status: All, Pending, Under Review, Approved, Rejected.
  - Search by student name, application reference number, or phone.
  - Update application status and log counselor remarks.
  - Permanently delete records with safety prompt.
- **Contact Inquiries Management (`/admin/inquiries`)**:
  - Status updates (New, In Progress, Resolved) and resolution notes.
- **Content CRUD Modules**:
  - News articles publishing (`/admin/news`).
  - School events calendar scheduler (`/admin/events`).
  - Faculty directory management (`/admin/faculty`).
  - Gallery photo upload & category tagging (`/admin/gallery`).
  - FAQ questions & answers editor (`/admin/faqs`).
  - Downloadable resource links (`/admin/downloads`).
- **School Settings (`/admin/settings`)**:
  - Update school name, Sanskrit motto, tagline, contact numbers, emails, physical address, working hours.
  - Admissions toggle (Open / Closed).
  - Configurable statistics cards (Students, Faculty, Years of Excellence, Focus on Values).
  - Live scrolling notice ticker text.
  - Social media URLs and Google Maps embed link.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug.
- **Database**: SQLite (local development), PostgreSQL-ready with `DATABASE_URL`.
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System with CSS variables), Vanilla JavaScript (ES6+).
- **Icons & Typography**: Font Awesome 6, Google Fonts (`Outfit`, `Plus Jakarta Sans`, `Cinzel`).
- **Production Server**: Gunicorn.
- **Testing**: Pytest & Pytest-Asyncio.

---

## 📂 Project Structure

```
sanskar-public-school/
├── app.py                     # Flask application factory, error handlers & context processor
├── config.py                  # Database & session configuration
├── models.py                  # SQLAlchemy ORM database models
├── seed.py                    # Database seeder with sample school data & default admin
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Complete documentation
├── routes/
│   ├── __init__.py
│   ├── main.py                # Public routes (Home, About, Academics, Admissions, etc.)
│   ├── api.py                 # REST API endpoints (/api/news, /api/admissions, etc.)
│   └── admin.py               # Protected admin CRUD routes
├── templates/
│   ├── base.html              # Master layout with top bar, sticky header, mobile drawer & footer
│   ├── index.html             # Homepage matching reference design
│   ├── about.html             # About Us page
│   ├── academics.html         # Academics & wings page
│   ├── admissions.html        # Admissions page with interactive application form
│   ├── admission_status.html  # Live application status tracking page
│   ├── faculty.html           # Dedicated faculty directory with department filters
│   ├── facilities.html        # Campus facilities showcase
│   ├── gallery.html           # Photo gallery with category filter & lightbox
│   ├── news.html              # News & notices index
│   ├── news_detail.html       # Individual article detail view
│   ├── student_life.html      # House systems, co-curricular clubs, sports
│   ├── parent_resources.html  # Parent resources, downloads & fee policies
│   ├── contact.html           # Contact form, campus info & Google Maps
│   ├── faqs.html              # Accordion FAQ page with search
│   ├── policies.html          # Privacy, terms, discipline, safeguarding
│   ├── login.html             # Admin login screen
│   ├── admin/
│   │   ├── base.html          # Admin portal master layout with sidebar
│   │   ├── dashboard.html     # Metrics & recent records overview
│   │   ├── admissions.html    # Admission application status review & remarks
│   │   ├── inquiries.html     # Contact inquiries resolution
│   │   ├── news.html          # News & notices CRUD
│   │   ├── events.html        # School events calendar manager
│   │   ├── faculty.html       # Faculty directory manager
│   │   ├── gallery.html       # Gallery manager
│   │   ├── faqs.html          # FAQ editor
│   │   ├── downloads.html     # Resource downloads manager
│   │   └── settings.html      # School contact & website settings
│   └── errors/
│       ├── 404.html           # Branded 404 error page
│       └── 500.html           # Branded 500 error page
├── static/
│   ├── css/
│   │   ├── style.css          # Core design tokens, components, hero, modals & toast styles
│   │   ├── responsive.css     # Breakpoint layouts & mobile drawer
│   │   └── admin.css          # Admin portal styling & tables
│   ├── js/
│   │   ├── main.js            # Sticky header, mobile drawer, accordions, toast notifications
│   │   ├── forms.js           # AJAX admission submission, modal confirmation, contact form
│   │   ├── gallery.js         # Fullscreen lightbox modal with keyboard navigation
│   │   └── admin.js           # Table search filter & deletion confirmation
│   └── images/
│       ├── logo.svg           # Official vector logo (green & gold with Sanskrit motto)
│       ├── hero/              # Hero classroom photography
│       ├── campus/            # Campus architecture photography
│       ├── academic/          # Pre-primary, primary, secondary wings
│       ├── faculty/           # Principal & faculty portraits
│       └── facilities/        # Science lab, library, computer lab, sports arena
└── tests/
    ├── __init__.py
    └── test_routes.py         # Pytest test suite for routes, APIs and authentication
```

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Clone / Open Directory
```bash
cd "sanskar public school"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python app.py
```
*Note: On first launch, the database (`sanskar_school.db`) is automatically initialized and seeded with rich content, including academic programs, faculty profiles, facilities, gallery photos, news articles, events, FAQs, downloads, and an initial administrator account.*

### 5. Access in Browser
- **Public Website**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Admin Portal**: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

---

## 🔐 Administrator Setup & Credentials

An initial administrator account is automatically provisioned for local testing:
- **Username / Email**: `admin` or `admin@sanskarpublicschool.in`
- **Password**: `Admin@Sanskar2026!`

In production, change the password immediately via the settings or database, or set the administrator via environment variables.

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite:
```bash
pytest
```
*All 7 integration test suites test:*
- 200 OK rendering on all 15 public pages.
- REST API response verification (`/api/news`, `/api/events`, `/api/faculty`, `/api/gallery`).
- Online admission submission with application number generation (`SPS-2026-XXXX`).
- Live application status lookup.
- Contact inquiry creation.
- Admin authentication barriers and dashboard authorization.

---

## 🌐 Production Deployment Guide (Render / Cloud)

### Render Deployment Steps
1. Push repository to GitHub/GitLab.
2. In Render Dashboard, click **New +** -> **Web Service**.
3. Select your repository.
4. Set Build and Start Commands:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Configure Environment Variables in Render:
   - `SECRET_KEY`: Set to a strong random 64-character secret.
   - `DATABASE_URL`: Add a Render PostgreSQL database connection string (e.g. `postgresql://user:pass@host:5432/sanskar_db`).
   - `PORT`: `5000` (or leave default assigned by Render).
6. Click **Deploy Web Service**.
