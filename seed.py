import os
from models import (
    db, AdminUser, AdmissionApplication, ContactInquiry,
    NewsArticle, SchoolEvent, FacultyProfile, GalleryItem,
    FAQ, DownloadableResource, WebsiteSetting
)

def seed_database(app):
    with app.app_context():
        db.create_all()

        # 1. Admin User Setup
        admin = AdminUser.query.filter_by(username='admin').first()
        if not admin:
            admin = AdminUser(
                username='admin',
                email='admin@sanskarpublicschool.in',
                role='superadmin'
            )
            admin.set_password('Admin@Sanskar2026!')
            db.session.add(admin)
            print("Created default administrator: admin / Admin@Sanskar2026!")

        # 2. Website Settings
        settings = [
            ('school_name', 'Sanskar Public School', 'Official School Name'),
            ('school_motto', 'विद्या ददाति विनयम्', 'School Sanskrit Motto'),
            ('school_tagline', 'Nurturing Knowledge. Building Character.', 'Primary School Tagline'),
            ('school_phone', '+91 79790 48493', 'Official Contact Number'),
            ('school_alt_phone', '+91 79790 48493', 'Admissions Helpline'),
            ('school_email', 'sanskarpublicskl2000@gmail.com', 'Primary Contact Email'),
            ('admissions_email', 'sanskarpublicskl2000@gmail.com', 'Admissions Desk Email'),
            ('school_address', 'Sanskar Knowledge Park, Sector 14, Education City', 'Campus Address'),
            ('office_hours', 'Monday – Saturday: 8:00 AM – 3:30 PM (Closed on Second Saturdays & Sundays)', 'Office Working Hours'),
            ('affiliation_info', 'Affiliated with Central Board of Secondary Education (CBSE, New Delhi)', 'Board Affiliation'),
            ('admissions_open', 'true', 'Admissions Status (true/false)'),
            ('academic_year', '2026 – 2027', 'Current Academic Year'),
            ('stat_students', '1000+', 'Total Enrolled Students Metric'),
            ('stat_faculty', '50+', 'Dedicated Faculty Members'),
            ('stat_excellence', '25+', 'Years of Educational Excellence'),
            ('stat_values', '100%', 'Focus on Values and Character'),
            ('facebook_url', 'https://facebook.com/sanskarpublicschool', 'Facebook Page URL'),
            ('instagram_url', 'https://www.instagram.com/sanskarpublicskl1/?hl=en', 'Instagram Page URL'),
            ('youtube_url', 'https://www.youtube.com/@SANSKARPublicschool-en1/shorts', 'YouTube Channel URL'),
            ('map_embed_url', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d112061.22353139363!2d77.2089851!3d28.6324291!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390cfd37b027f357%3A0x839f0f8622aac7!2sSanskar%20School!5e0!3m2!1sen!2sin!4v1700000000000', 'Google Maps Embed Iframe URL'),
            ('ticker_announcement', 'Admissions open for Academic Session 2026-27 from Nursery to Grade XI. Download prospectus online or visit school front desk.', 'Top Notice Ticker Text')
        ]

        for key, val, desc in settings:
            if not WebsiteSetting.query.filter_by(key=key).first():
                db.session.add(WebsiteSetting(key=key, value=val, description=desc))

        # 3. Faculty Profiles
        if FacultyProfile.query.count() == 0:
            faculty_list = [
                FacultyProfile(
                    name="Dr. Arvind Sharma",
                    designation="Principal & Academic Director",
                    department="Leadership",
                    qualifications="Ph.D. in Educational Leadership, M.Sc. Physics, B.Ed.",
                    experience="26+ Years Experience",
                    bio="A visionary educator passionate about experiential learning, character formation, and holistic student growth.",
                    email="principal@sanskarpublicschool.in",
                    image_url="/static/images/faculty/principal.jpg",
                    display_order=1
                ),
                FacultyProfile(
                    name="Mrs. Sunita Verma",
                    designation="Vice Principal & Head of Academics",
                    department="Leadership",
                    qualifications="M.A. English Literature, M.Ed., Gold Medalist",
                    experience="20+ Years Experience",
                    bio="Dedicated to fostering an inclusive, student-centric academic atmosphere and curriculum enrichment.",
                    email="vp@sanskarpublicschool.in",
                    image_url="/static/images/faculty/vice_principal.jpg",
                    display_order=2
                ),
                FacultyProfile(
                    name="Mr. Rajesh Mukherjee",
                    designation="Senior Physics Faculty & STEM Head",
                    department="Science",
                    qualifications="M.Sc. Physics (IIT Roorkee), B.Ed.",
                    experience="15+ Years Experience",
                    bio="Mentoring young scientific minds in competitive exams, robotics, and hands-on lab experiments.",
                    email="rajesh.m@sanskarpublicschool.in",
                    image_url="/static/images/faculty/principal.jpg",
                    display_order=3
                ),
                FacultyProfile(
                    name="Dr. Meenakshi Joshi",
                    designation="Head of Mathematics",
                    department="Mathematics",
                    qualifications="Ph.D. Applied Mathematics, M.Sc., B.Ed.",
                    experience="18+ Years Experience",
                    bio="Pioneering conceptual mathematics pedagogy that turns abstract formulas into intuitive logical problem-solving.",
                    email="meenakshi.j@sanskarpublicschool.in",
                    image_url="/static/images/faculty/vice_principal.jpg",
                    display_order=4
                ),
                FacultyProfile(
                    name="Mr. Vikram Chauhan",
                    designation="Head of Physical Education & Sports",
                    department="Arts & Sports",
                    qualifications="M.P.Ed., Former State Athletics Medalist",
                    experience="12+ Years Experience",
                    bio="Promoting physical fitness, sportsmanship, and tactical prowess across basketball, football, and athletics.",
                    email="sports@sanskarpublicschool.in",
                    image_url="/static/images/faculty/principal.jpg",
                    display_order=5
                ),
                FacultyProfile(
                    name="Mrs. Shalini Rao",
                    designation="Senior Chemistry Faculty",
                    department="Science",
                    qualifications="M.Sc. Chemistry, CSIR-NET, B.Ed.",
                    experience="11+ Years Experience",
                    bio="Specializing in organic chemistry concepts and guiding student research for national science exhibitions.",
                    email="shalini.r@sanskarpublicschool.in",
                    image_url="/static/images/faculty/vice_principal.jpg",
                    display_order=6
                )
            ]
            db.session.add_all(faculty_list)

        # 4. News Articles
        if NewsArticle.query.count() == 0:
            news_items = [
                NewsArticle(
                    title="Sanskar Public School Bags Top Honors at Inter-School STEM Olympiad",
                    slug="stem-olympiad-victory-2026",
                    category="Achievements",
                    summary="Our middle and senior school robotics innovators clinched the first position at the National Science Innovation League.",
                    content="Students from Sanskar Public School showcased phenomenal creativity and technical finesse at the National Science Innovation League held this week. The four-member team designed an autonomous solar-powered water filtration prototype, earning high praise from eminent scientists and evaluators.",
                    image_url="/static/images/facilities/stem_lab.jpg",
                    is_published=True,
                    published_date="18 Oct 2026"
                ),
                NewsArticle(
                    title="Admissions Open for Academic Session 2026–2027",
                    slug="admissions-announcement-2026-27",
                    category="Notice",
                    summary="Registration for nursery to class XI is now underway. Parents can submit admission inquiries online or visit campus.",
                    content="Sanskar Public School is delighted to announce that admission applications for the upcoming academic session 2026–27 are officially open. With our state-of-the-art smart classrooms, world-class labs, and compassionate faculty, we welcome new learners to join our vibrant family.",
                    image_url="/static/images/hero/hero_classroom.jpg",
                    is_published=True,
                    published_date="10 Oct 2026"
                ),
                NewsArticle(
                    title="Annual Cultural Extravaganza 'Vasantotsav 2026' Concludes with Grandeur",
                    slug="annual-day-cultural-fest-2026",
                    category="Celebration",
                    summary="A dazzling showcase of classical dance, theatrical drama, and musical orchestras enthralled over 1500 parents and guests.",
                    content="The annual school day 'Vasantotsav 2026' was celebrated with immense enthusiasm and artistic splendor in the school auditorium. Students presented captivating cultural dance performances representing India's rich heritage, followed by a theatrical production on environmental stewardship.",
                    image_url="/static/images/gallery/cultural_event.jpg",
                    is_published=True,
                    published_date="28 Sep 2026"
                ),
                NewsArticle(
                    title="District Inter-School Athletic Meet: Sanskar Athletes Clinch 14 Medals",
                    slug="inter-school-athletic-meet-2026",
                    category="Sports",
                    summary="Our sprint relay teams and high-jump champions brought home 8 gold, 4 silver, and 2 bronze medals.",
                    content="Sanskar sports stars triumphed across multiple track and field events in the District Inter-School Athletic Championship. Principal Dr. Arvind Sharma congratulated the physical education department and student athletes for their discipline and exemplary team spirit.",
                    image_url="/static/images/facilities/sports.jpg",
                    is_published=True,
                    published_date="15 Sep 2026"
                )
            ]
            db.session.add_all(news_items)

        # 5. School Events
        if SchoolEvent.query.count() == 0:
            events = [
                SchoolEvent(
                    title="Annual Science & Innovation Exhibition 2026",
                    category="Academics",
                    description="Hands-on demonstration of scientific models, working robotics projects, eco-friendly energy prototypes, and digital experiments.",
                    event_date="05 Nov 2026",
                    event_time="09:30 AM – 03:00 PM",
                    location="School Science Center & Quadrangle",
                    image_url="/static/images/facilities/science_lab.jpg",
                    is_featured=True
                ),
                SchoolEvent(
                    title="Parent-Teacher Interaction Meeting (Term I Review)",
                    category="Parent-Teacher",
                    description="Comprehensive one-on-one progress review between parents and subject educators to discuss student holistic development.",
                    event_date="14 Nov 2026",
                    event_time="08:30 AM – 01:30 PM",
                    location="Respective Homerooms",
                    image_url="/static/images/campus/campus_building.jpg",
                    is_featured=True
                ),
                SchoolEvent(
                    title="Inter-House Football & Basketball Tournament",
                    category="Sports",
                    description="Exciting annual sports championship where the four school houses compete for the prestigious Rolling Sports Trophy.",
                    event_date="22 Nov 2026",
                    event_time="08:00 AM – 02:00 PM",
                    location="Main Athletic Complex",
                    image_url="/static/images/facilities/sports.jpg",
                    is_featured=False
                ),
                SchoolEvent(
                    title="National Mathematics Day Symposium & Quiz",
                    category="Academics",
                    description="Celebrating Srinivasa Ramanujan's legacy through inter-school math puzzles, speed calculations, and analytical challenges.",
                    event_date="22 Dec 2026",
                    event_time="10:00 AM – 01:00 PM",
                    location="School Auditorium",
                    image_url="/static/images/facilities/library.jpg",
                    is_featured=False
                )
            ]
            db.session.add_all(events)

        # 6. Gallery Items
        if GalleryItem.query.count() == 0:
            gallery = [
                GalleryItem(
                    title="Modern School Campus & Landscaped Lawns",
                    category="Campus",
                    image_url="/static/images/campus/campus_building.jpg",
                    caption="The architectural facade and lush green environment of Sanskar Public School.",
                    display_order=1
                ),
                GalleryItem(
                    title="Engaged Classroom Learning in Full Swing",
                    category="Academics",
                    image_url="/static/images/hero/hero_classroom.jpg",
                    caption="Students actively participating in conceptual learning and interactive discussions.",
                    display_order=2
                ),
                GalleryItem(
                    title="Advanced Science Laboratories",
                    category="Academics",
                    image_url="/static/images/facilities/science_lab.jpg",
                    caption="Students conducting hands-on chemistry and physics experiments with modern apparatus.",
                    display_order=3
                ),
                GalleryItem(
                    title="The Central Knowledge Library",
                    category="Campus",
                    image_url="/static/images/facilities/library.jpg",
                    caption="A quiet sanctuary housing over 15,000 volumes, academic journals, and digital e-readers.",
                    display_order=4
                ),
                GalleryItem(
                    title="Cutting-Edge Computer & Coding Lab",
                    category="Academics",
                    image_url="/static/images/facilities/computer_lab.jpg",
                    caption="Digital literacy, programming fundamentals, and AI concepts taught with high-speed systems.",
                    display_order=5
                ),
                GalleryItem(
                    title="Athletic Track & Outdoor Sports Arena",
                    category="Sports",
                    image_url="/static/images/facilities/sports.jpg",
                    caption="State-of-the-art running track, football turf, and professional coaching sessions.",
                    display_order=6
                ),
                GalleryItem(
                    title="Colorful Pre-Primary Play & Learn Zone",
                    category="Academics",
                    image_url="/static/images/academic/pre_primary.jpg",
                    caption="Montessori-inspired early childhood activity center with sensory play apparatus.",
                    display_order=7
                ),
                GalleryItem(
                    title="Annual Cultural Day 'Vasantotsav' Performances",
                    category="Cultural",
                    image_url="/static/images/gallery/cultural_event.jpg",
                    caption="Spectacular Indian classical dance performance celebrating cultural harmony.",
                    display_order=8
                ),
                GalleryItem(
                    title="STEM Innovation & Robotics Lab Workshop",
                    category="Academics",
                    image_url="/static/images/facilities/stem_lab.jpg",
                    caption="Secondary school innovators assembling robotic prototypes and automated circuitry.",
                    display_order=9
                )
            ]
            db.session.add_all(gallery)

        # 7. FAQs
        if FAQ.query.count() == 0:
            faqs = [
                FAQ(
                    category="Admissions",
                    question="What is the admission procedure for the 2026-27 academic session?",
                    answer="Admissions begin with submitting an online inquiry or application form through this portal. Once received, the admissions office will contact you to schedule an interaction session and campus walkthrough. Following document verification, admission confirmation is granted.",
                    display_order=1
                ),
                FAQ(
                    category="Admissions",
                    question="What is the minimum age criterion for Nursery and Class 1?",
                    answer="For Nursery, the child should have completed 3 years of age as of March 31 of the academic year. For Class 1, the minimum recommended age is 6 years as aligned with NEP guidelines.",
                    display_order=2
                ),
                FAQ(
                    category="Academics",
                    question="Which curriculum board is Sanskar Public School affiliated with?",
                    answer="Sanskar Public School follows the Central Board of Secondary Education (CBSE) curriculum, integrated with experiential pedagogy, project-based inquiry, and value education inspired by our motto 'विद्या ददाति विनयम्'.",
                    display_order=3
                ),
                FAQ(
                    category="Fees & Payments",
                    question="How can school fees be paid?",
                    answer="School fees can be paid quarterly through our secure online payment portal via Net Banking, UPI, Credit/Debit card, or by Cheque/Demand Draft at the school accounts desk during office hours.",
                    display_order=4
                ),
                FAQ(
                    category="Transport",
                    question="Does the school offer GPS-enabled bus transportation?",
                    answer="Yes, the school operates a well-managed fleet of air-conditioned and standard school buses covering all major residential corridors in the city. Every bus features GPS tracking, CCTV surveillance, first-aid kits, and trained female attendants.",
                    display_order=5
                ),
                FAQ(
                    category="Facilities",
                    question="What safety and medical measures are maintained on campus?",
                    answer="The campus is monitored 24/7 by CCTV security and trained guards. We house a fully equipped infirmary staffed by a qualified full-time nurse and an on-call pediatrician for emergencies.",
                    display_order=6
                )
            ]
            db.session.add_all(faqs)

        # 8. Downloadable Resources
        if DownloadableResource.query.count() == 0:
            resources = [
                DownloadableResource(
                    title="Admission Registration Form & Instructions (2026-27)",
                    category="Forms",
                    description="Official printable registration form with detailed guidelines for offline submission.",
                    file_url="#",
                    file_size="PDF (320 KB)"
                ),
                DownloadableResource(
                    title="Annual Academic Calendar (Session 2026-27)",
                    category="Calendar",
                    description="Comprehensive breakdown of term dates, examination schedules, gazetted holidays, and events.",
                    file_url="#",
                    file_size="PDF (450 KB)"
                ),
                DownloadableResource(
                    title="School Uniform & Dress Code Guidelines",
                    category="Guidelines",
                    description="Detailed specifications for summer and winter uniforms, house sportswear, and footwear.",
                    file_url="#",
                    file_size="PDF (180 KB)"
                ),
                DownloadableResource(
                    title="Curriculum Overview & Syllabus Breakdown (Grades I to XII)",
                    category="Syllabus",
                    description="Subject-wise syllabus, recommended reading lists, and internal assessment criteria.",
                    file_url="#",
                    file_size="PDF (850 KB)"
                ),
                DownloadableResource(
                    title="Fee Structure & Payment Schedule (2026-27)",
                    category="Fees",
                    description="Transparent itemized breakdown of tuition fees, activity charges, and transport slabs.",
                    file_url="#",
                    file_size="PDF (240 KB)"
                ),
                DownloadableResource(
                    title="Student Code of Conduct & Honor Policy",
                    category="Guidelines",
                    description="Principles of student discipline, attendance expectations, digital etiquette, and anti-bullying code.",
                    file_url="#",
                    file_size="PDF (210 KB)"
                )
            ]
            db.session.add_all(resources)

        # 9. Seed a couple sample admission applications & inquiries for admin demo
        if AdmissionApplication.query.count() == 0:
            apps = [
                AdmissionApplication(
                    application_number="SPS-2026-1001",
                    student_name="Aarav Sharma",
                    dob="2018-05-12",
                    gender="Male",
                    grade_applying="Class 3",
                    parent_name="Ramesh Sharma",
                    relationship="Father",
                    phone="+91 98111 22233",
                    email="ramesh.sharma@example.com",
                    address="Flat 402, Green Valley Apartments, Education City",
                    previous_school="Delhi Public International",
                    previous_grade="Class 2",
                    previous_percentage="94%",
                    additional_notes="Interested in school chess club and athletics.",
                    status="Under Review",
                    admin_remarks="Documents verified. Scheduled for parent interaction on Nov 3."
                ),
                AdmissionApplication(
                    application_number="SPS-2026-1002",
                    student_name="Ananya Iyer",
                    dob="2021-08-20",
                    gender="Female",
                    grade_applying="Pre-Primary (UKG)",
                    parent_name="Priya Iyer",
                    relationship="Mother",
                    phone="+91 98222 33344",
                    email="priya.iyer@example.com",
                    address="Villa 15, Palm Meadows, Sector 12",
                    previous_school="EuroKids Preschool",
                    previous_grade="LKG",
                    previous_percentage="A+",
                    additional_notes="Loves drawing and music.",
                    status="Pending",
                    admin_remarks="Awaiting birth certificate photocopy verification."
                )
            ]
            db.session.add_all(apps)

        if ContactInquiry.query.count() == 0:
            inquiries = [
                ContactInquiry(
                    name="Deepak Kapoor",
                    email="deepak.k@example.com",
                    phone="+91 97777 88888",
                    subject="Inquiry regarding Grade 11 Science Stream options",
                    message="Hello, I would like to inquire whether Sanskar Public School offers Integrated JEE coaching along with the CBSE syllabus for Class 11 Physics and Chemistry.",
                    status="New"
                ),
                ContactInquiry(
                    name="Kavita Saxena",
                    email="kavita.s@example.com",
                    phone="+91 96666 55555",
                    subject="School Bus Route Inquiry for Sector 21",
                    message="Respected Admin, we are moving to Sector 21 next month and would like to confirm if your school transport bus covers stop near Aster Plaza.",
                    status="In Progress",
                    admin_notes="Forwarded to Transport In-Charge Mr. Chauhan for route clearance."
                )
            ]
            db.session.add_all(inquiries)

        db.session.commit()
        print("Database seeded with comprehensive initial school content successfully!")
