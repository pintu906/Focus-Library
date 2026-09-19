from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, date, timedelta


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "focus_library_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///focus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# MODELS
# =========================================================

# -------------------------
# ADMIN
# -------------------------

class Admin(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# -------------------------
# STUDENT
# -------------------------

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    reg_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True
    )

    phone = db.Column(
        db.String(20)
    )

    password = db.Column(
        db.String(200)
    )


    # =========================
    # SEAT & SHIFT
    # =========================

    seat_no = db.Column(
        db.String(20),
        nullable=True
    )

    shift_time = db.Column(
        db.String(50),
        nullable=True
    )

    duration_hours = db.Column(
        db.Float,
        default=0
    )


    # =========================
    # MEMBERSHIP
    # =========================

    membership_start = db.Column(
        db.Date,
        nullable=True
    )

    membership_end = db.Column(
        db.Date,
        nullable=True
    )


    # =========================
    # LOCKER
    # =========================

    locker_no = db.Column(
        db.String(50),
        nullable=True
    )


    # =========================
    # PAYMENT
    # =========================

    membership_payment = db.Column(
        db.Float,
        default=0
    )

    locker_payment = db.Column(
        db.Float,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    paid_amount = db.Column(
        db.Float,
        default=0
    )

    payment_status = db.Column(
        db.String(20),
        default="Paid"
    )

    due_amount = db.Column(
        db.Float,
        default=0
    )
    payment_date = db.Column(
        db.Date,
        nullable=True
    )


    # =========================
    # STATUS
    # =========================

    status = db.Column(
        db.String(30),
        default="Active"
    )


    # =========================
    # PASSWORD
    # =========================

    def set_password(self, password):

        self.password = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )


# -------------------------
# SEAT
# -------------------------

class Seat(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    seat_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )


class Book(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    author = db.Column(
        db.String(100)
    )

    category = db.Column(
        db.String(100)
    )

    isbn = db.Column(
        db.String(50),
        unique=True
    )

    total_copies = db.Column(
        db.Integer,
        default=1
    )

    available_copies = db.Column(
        db.Integer,
        default=1
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Available"
    )

    def __repr__(self):

        return f"<Book {self.title}>"


# =========================================================
# LIBRARY VISIT
# =========================================================
class LibraryVisit(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    entry_time = db.Column(
        db.DateTime,
        nullable=True
    )

    duration_hours = db.Column(
        db.Integer,
        nullable=False
    )

    expected_end_time = db.Column(
        db.DateTime,
        nullable=True
    )

    exit_time = db.Column(
        db.DateTime,
        nullable=True
    )

    payment = db.Column(
        db.Float,
        default=0
    )

    payment_date = db.Column(
        db.DateTime,
        nullable=True
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    status = db.Column(
        db.String(20),
        default="Waiting"
    )

    student = db.relationship(
        "Student",
        backref="library_visits"
    )
# =========================================================
# BOOK ISSUE
# =========================================================

class BookIssue(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id"),
        nullable=False
    )

    issue_date = db.Column(
        db.Date,
        default=date.today
    )

    return_date = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(30),
        default="Issued"
    )

    student = db.relationship(
        "Student",
        backref="book_issues"
    )

    book = db.relationship(
        "Book",
        backref="book_issues"
    )

class Payment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -------------------------
    # STUDENT
    # -------------------------

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    # -------------------------
    # PAYMENT AMOUNT
    # -------------------------

    amount = db.Column(
        db.Float,
        nullable=False
    )

    # -------------------------
    # PAYMENT DATE
    # -------------------------

    payment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -------------------------
    # PAYMENT MODE
    # -------------------------

    payment_mode = db.Column(
        db.String(30),
        default="Cash"
    )

    # -------------------------
    # NOTE
    # -------------------------

    note = db.Column(
        db.String(255),
        nullable=True
    )

    # -------------------------
    # RELATIONSHIP
    # -------------------------

    student = db.relationship(
        "Student",
        backref="payments"
    )
# =========================================================
# DATABASE INITIALIZATION
# =========================================================

with app.app_context():
    with app.app_context():
       db.create_all()

    from sqlalchemy import text

    columns = db.session.execute(
        text("PRAGMA table_info(student)")
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "paid_amount" not in column_names:
        db.session.execute(
            text(
                "ALTER TABLE student "
                "ADD COLUMN paid_amount FLOAT DEFAULT 0"
            )
        )
        db.session.commit()
        print("paid_amount column added!")

    db.create_all()

    # -----------------------------------------
    # CREATE SEATS
    # -----------------------------------------

    if Seat.query.count() == 0:

        for i in range(1, 131):

            seat = Seat(
                seat_no=str(i),
                status="Available"
            )

            db.session.add(seat)

        db.session.commit()

        print("130 seats created!")

    # -----------------------------------------
    # CREATE ADMIN
    # -----------------------------------------

    admin = Admin.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if not admin:

        admin = Admin(
            email="admin@gmail.com",
            password=generate_password_hash("1234")
        )

        db.session.add(admin)

        db.session.commit()

        print("Admin created!")

    else:

        print("Admin already exists!")


# =========================================================
# HOME
# =========================================================

@app.route("/")
def dashboard():

    total_books = Book.query.count()

    total_students = Student.query.count()

    total_seats = Seat.query.count()

    available_seats = Seat.query.filter_by(
        status="Available"
    ).count()

    issued_books = BookIssue.query.filter_by(
        status="Issued"
    ).count()

    return render_template(
        "dashboard.html",

        total_books=total_books,

        total_students=total_students,

        total_seats=total_seats,

        available_seats=available_seats,

        issued_books=issued_books
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin_login",
    methods=["POST"]
)
def admin_login():

    email = request.form.get(
        "email"
    )

    password = request.form.get(
        "password"
    )

    admin = Admin.query.filter_by(
        email=email
    ).first()

    if admin and check_password_hash(
        admin.password,
        password
    ):

        session["admin_id"] = admin.id

        session["admin_email"] = admin.email

        session["role"] = "admin"

        return redirect(
            url_for("admin_dashboard")
        )

    flash(
        "Invalid email or password",
        "danger"
    )

    return redirect("/")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:

        return redirect("/")

    total_books = Book.query.count()

    total_students = Student.query.count()

    total_seats = Seat.query.count()

    available_seats = Seat.query.filter_by(
        status="Available"
    ).count()

    total_issued = BookIssue.query.filter_by(
        status="Issued"
    ).count()

    available_books = db.session.query(
        db.func.sum(
            Book.available_copies
        )
    ).scalar() or 0

    books = Book.query.order_by(
        Book.id.desc()
    ).limit(5).all()

    students = Student.query.order_by(
        Student.id.desc()
    ).limit(5).all()

    recent_issues = BookIssue.query.order_by(
        BookIssue.id.desc()
    ).limit(5).all()

    return render_template(
        "admin/admin_dash.html",

        total_books=total_books,

        total_students=total_students,

        total_seats=total_seats,

        available_seats=available_seats,

        total_issued=total_issued,

        available_books=available_books,

        books=books,

        students=students,

        recent_issues=recent_issues
    )

@app.route("/student/login", methods=["POST"])
def student_login():

    email = request.form.get(
        "email",
        ""
    ).strip()

    reg_no = request.form.get(
        "reg_no",
        ""
    ).strip()


    if not email or not reg_no:

        flash(
            "Email and Registration No. are required.",
            "danger"
        )

        return redirect("/")


    student = Student.query.filter(
        db.func.lower(Student.email) == email.lower(),
        Student.reg_no == reg_no
    ).first()


    if not student:

        flash(
            "Invalid Email or Registration No.",
            "danger"
        )

        return redirect("/")


    # ONLY ACTIVE STUDENTS

    if student.status != "Active":

        flash(
            "Your student account is inactive.",
            "danger"
        )

        return redirect("/")


    # ==============================
    # STUDENT SESSION
    # ==============================

    session["student_id"] = student.id

    session["student_name"] = student.name

    session["student_reg_no"] = student.reg_no


    return redirect(
        url_for("student_dashboard")
    )


@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:
        return redirect("/")

    student = Student.query.get_or_404(
        session["student_id"]
    )

    return render_template(
        "student/student_dash.html",
        student=student
    )    
@app.route("/student/logout")
def student_logout():

    session.pop("student_id", None)
    session.pop("student_name", None)
    session.pop("student_reg_no", None)

    return redirect("/")    

# =========================================================
# ADMIN - BOOKS
# =========================================================

@app.route("/admin/books")
def admin_books():

    search = request.args.get(
        "search",
        ""
    ).strip()

    if search:

        books = Book.query.filter(
            db.or_(

                Book.title.ilike(
                    f"%{search}%"
                ),

                Book.author.ilike(
                    f"%{search}%"
                ),

                Book.category.ilike(
                    f"%{search}%"
                )
            )
        ).all()

    else:

        books = Book.query.all()

    return render_template(
        "admin/admin_books.html",
        books=books
    )


# =========================================================
# ADD BOOK
# =========================================================

@app.route(
    "/admin/add_book",
    methods=["GET", "POST"]
)
def add_book():

    if request.method == "POST":

        title = request.form.get(
            "title"
        )

        author = request.form.get(
            "author"
        )

        category = request.form.get(
            "category"
        )

        isbn = request.form.get(
            "isbn"
        )

        total_copies = int(
            request.form.get(
                "total_copies",
                1
            )
        )

        description = request.form.get(
            "description"
        )

        book = Book(

            title=title,

            author=author,

            category=category,

            isbn=isbn,

            total_copies=total_copies,

            available_copies=total_copies,

            description=description,

            status="Available"
        )

        db.session.add(book)

        db.session.commit()

        flash(
            "Book added successfully!",
            "success"
        )

        return redirect(
            url_for("admin_books")
        )

    return render_template(
        "admin/add_book.html"
    )


# =========================================================
# EDIT BOOK
# =========================================================

@app.route(
    "/admin/edit_book/<int:id>",
    methods=["GET", "POST"]
)
def edit_book(id):

    book = Book.query.get_or_404(id)

    if request.method == "POST":

        book.title = request.form.get(
            "title"
        )

        book.author = request.form.get(
            "author"
        )

        book.category = request.form.get(
            "category"
        )

        book.isbn = request.form.get(
            "isbn"
        )

        book.description = request.form.get(
            "description"
        )

        db.session.commit()

        flash(
            "Book updated successfully!",
            "success"
        )

        return redirect(
            url_for("admin_books")
        )

    return render_template(
        "admin/edit_book.html",
        book=book
    )


# =========================================================
# DELETE BOOK
# =========================================================

@app.route(
    "/admin/delete_book/<int:id>",
    methods=["POST"]
)
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)

    db.session.commit()

    flash(
        "Book deleted successfully!",
        "success"
    )

    return redirect(
        url_for("admin_books")
    )


# =========================================================
# ADMIN - STUDENTS
# =========================================================
# =========================================================
# ADMIN STUDENTS
# =========================================================

@app.route("/admin/students")
def admin_students():

    search = request.args.get(
        "search",
        ""
    ).strip()

    # =====================================================
    # SEARCH
    # =====================================================

    if search:

        students = Student.query.filter(
            db.or_(

                Student.name.ilike(
                    f"%{search}%"
                ),

                Student.reg_no.ilike(
                    f"%{search}%"
                ),

                Student.email.ilike(
                    f"%{search}%"
                ),

                Student.phone.ilike(
                    f"%{search}%"
                )

            )
        ).order_by(
            Student.name.asc()
        ).all()

    # =====================================================
    # ALL STUDENTS
    # =====================================================

    else:

        students = Student.query.order_by(
            Student.name.asc()
        ).all()

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "admin/admin_students.html",
        students=students
    )


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/admin/add_student", methods=["GET", "POST"])
def add_student():

    if "admin_id" not in session:
        return redirect("/")

    if request.method == "POST":

        # =========================================
        # BASIC STUDENT DETAILS
        # =========================================

        name = request.form.get(
            "name",
            ""
        ).strip()

        reg_no = request.form.get(
            "reg_no",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        seat_no = request.form.get(
            "seat_no",
            ""
        ).strip()

        locker_no = request.form.get(
            "locker_no",
            ""
        ).strip()


        # =========================================
        # SLOT TIME
        # =========================================

        start_hour = request.form.get(
            "start_hour",
            ""
        ).strip()

        start_period = request.form.get(
            "start_period",
            ""
        ).strip()

        end_hour = request.form.get(
            "end_hour",
            ""
        ).strip()

        end_period = request.form.get(
            "end_period",
            ""
        ).strip()


        # =========================================
        # CHECK SLOT TIME
        # =========================================

        if not (
            start_hour
            and start_period
            and end_hour
            and end_period
        ):

            flash(
                "Please select complete slot timing.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # =========================================
        # CONVERT 12-HOUR TIME TO MINUTES
        # =========================================

        def convert_to_minutes(hour, period):

            hour = int(hour)

            period = period.upper()


            if period == "AM":

                if hour == 12:
                    hour = 0

            elif period == "PM":

                if hour != 12:
                    hour += 12


            return hour * 60


        start_minutes = convert_to_minutes(
            start_hour,
            start_period
        )

        end_minutes = convert_to_minutes(
            end_hour,
            end_period
        )


        # =========================================
        # CALCULATE DURATION
        # =========================================

        # Example:
        # 10 AM → 4 PM = 6 Hours
        #
        # Example:
        # 10 PM → 4 AM = 6 Hours

        if end_minutes <= start_minutes:

            end_minutes += 24 * 60


        difference_minutes = (
            end_minutes
            - start_minutes
        )


        duration_hours = (
            difference_minutes / 60
        )


        if duration_hours <= 0:

            flash(
                "Invalid slot timing.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # =========================================
        # CREATE SLOT TEXT
        # =========================================

        shift_time = (
            f"{start_hour}:00 {start_period} - "
            f"{end_hour}:00 {end_period}"
        )


        # =========================================
        # BASIC VALIDATION
        # =========================================

        if not name or not reg_no:

            flash(
                "Student name and registration number are required.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # =========================================
        # CHECK DUPLICATE EMAIL
        # =========================================

        if email:

            existing_email = Student.query.filter(
                Student.email == email
            ).first()


            if existing_email:

                flash(
                    "This email is already registered with another student.",
                    "danger"
                )

                return redirect(
                    url_for("add_student")
                )


        # =========================================
        # CHECK DUPLICATE REGISTRATION
        # =========================================

        existing_reg = Student.query.filter(
            Student.reg_no == reg_no
        ).first()


        if existing_reg:

            flash(
                "This registration number is already registered.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # =========================================
        # MEMBERSHIP START DATE
        # =========================================

        membership_start = request.form.get(
            "membership_start",
            ""
        ).strip()


        if membership_start:

            try:

                start_date = datetime.strptime(
                    membership_start,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                flash(
                    "Invalid membership start date.",
                    "danger"
                )

                return redirect(
                    url_for("add_student")
                )

        else:

            flash(
                "Please select membership start date.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # =========================================
        # MEMBERSHIP END DATE
        # =========================================

        from dateutil.relativedelta import relativedelta

        end_date = (
            start_date
            + relativedelta(months=1)
        )


        # =========================================
        # PAYMENT
        # =========================================

        try:

            membership_payment = float(
                request.form.get(
                    "membership_payment",
                    0
                ) or 0
            )

            locker_payment = float(
                request.form.get(
                    "locker_payment",
                    0
                ) or 0
            )

            due_amount = float(
                request.form.get(
                    "due_amount",
                    0
                ) or 0
            )

        except ValueError:

            flash(
                "Invalid payment amount.",
                "danger"
            )

            return redirect(
                url_for("add_student")
            )


        # Prevent negative values

        if membership_payment < 0:
            membership_payment = 0


        if locker_payment < 0:
            locker_payment = 0


        if due_amount < 0:
            due_amount = 0


        # =========================================
        # TOTAL AMOUNT
        # =========================================

        total_amount = (
            membership_payment
            + locker_payment
        )


        # =========================================
        # PAYMENT STATUS
        # =========================================

        payment_status = request.form.get(
            "payment_status",
            "Paid"
        )


        # =========================================
        # PAID / DUE CALCULATION
        # =========================================

        if payment_status == "Paid":

            due_amount = 0

            paid_amount = total_amount


        elif payment_status == "Due":

            if due_amount <= 0:

                flash(
                    "Please enter due amount.",
                    "danger"
                )

                return redirect(
                    url_for("add_student")
                )


            if due_amount > total_amount:

                flash(
                    "Due amount cannot be greater than total amount.",
                    "danger"
                )

                return redirect(
                    url_for("add_student")
                )


            # Total - Due = Paid

            paid_amount = (
                total_amount
                - due_amount
            )


        else:

            payment_status = "Paid"

            due_amount = 0

            paid_amount = total_amount


        # =========================================
        # STUDENT STATUS
        # =========================================

        status = request.form.get(
            "status",
            "Active"
        )


        # =========================================
        # CREATE STUDENT
        # =========================================

        student = Student(

            name=name,

            reg_no=reg_no,

            email=email
                if email
                else None,

            phone=phone
                if phone
                else None,

            seat_no=seat_no
                if seat_no
                else None,

            locker_no=locker_no
                if locker_no
                else None,


            # SLOT

            shift_time=shift_time,

            duration_hours=duration_hours,


            # MEMBERSHIP

            membership_start=start_date,

            membership_end=end_date,


            # PAYMENT

            membership_payment=membership_payment,

            locker_payment=locker_payment,

            total_amount=total_amount,

            paid_amount=paid_amount,

            payment_status=payment_status,

            due_amount=due_amount,


            # STATUS

            status=status
        )


        # =========================================
        # SAVE DATABASE
        # =========================================

        db.session.add(student)

        db.session.commit()


        # =========================================
        # SUCCESS MESSAGE
        # =========================================

        flash(
            f"Student added successfully! "
            f"Slot: {shift_time} | "
            f"Duration: {duration_hours:g} Hours | "
            f"Total: ₹{total_amount:.2f} | "
            f"Paid: ₹{paid_amount:.2f} | "
            f"Due: ₹{due_amount:.2f}",
            "success"
        )


        return redirect(
            url_for("admin_students")
        )


    # =========================================
    # GET REQUEST
    # =========================================

    return render_template(
        "admin/add_student.html"
    )

# =========================================================
# EDIT STUDENT
# =========================================================
# =========================================================
# EDIT STUDENT
# =========================================================

@app.route(
    "/admin/edit_student/<int:id>",
    methods=["GET", "POST"]
)
def edit_student(id):

    # Get student
    student = Student.query.get_or_404(id)

    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        # =================================================
        # NAME / REG NO / EMAIL / PHONE
        # =================================================
        # Ye fields edit nahi honge.
        # Existing database values same rahenge.

        # =================================================
        # SEAT
        # =================================================

        seat_no = request.form.get(
            "seat_no",
            ""
        ).strip()

        student.seat_no = (
            seat_no if seat_no else None
        )

        # =================================================
        # LOCKER
        # =================================================

        locker_no = request.form.get(
            "locker_no",
            ""
        ).strip()

        student.locker_no = (
            locker_no if locker_no else None
        )

        # =================================================
        # SLOT TIME
        # OPTIONAL
        # =================================================
        # Purana slot automatically same rahega.
        # Agar complete new slot select kiya gaya,
        # tabhi slot change hoga.

        start_hour = request.form.get(
            "start_hour",
            ""
        ).strip()

        start_period = request.form.get(
            "start_period",
            ""
        ).strip()

        end_hour = request.form.get(
            "end_hour",
            ""
        ).strip()

        end_period = request.form.get(
            "end_period",
            ""
        ).strip()

        # Complete new slot selected
        if (
            start_hour
            and start_period
            and end_hour
            and end_period
        ):

            student.shift_time = (
                f"{start_hour}:00 {start_period} - "
                f"{end_hour}:00 {end_period}"
            )

            # Duration
            duration_hours = request.form.get(
                "duration_hours",
                type=float
            )

            if (
                duration_hours is not None
                and duration_hours > 0
            ):

                student.duration_hours = (
                    duration_hours
                )

        # =================================================
        # MEMBERSHIP START DATE
        # =================================================

        start_date = request.form.get(
            "membership_start",
            ""
        ).strip()

        if start_date:

            try:

                student.membership_start = (
                    datetime.strptime(
                        start_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                flash(
                    "Invalid membership start date.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "edit_student",
                        id=id
                    )
                )

        # =================================================
        # MEMBERSHIP END DATE
        # =================================================

        end_date = request.form.get(
            "membership_end",
            ""
        ).strip()

        if end_date:

            try:

                student.membership_end = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                flash(
                    "Invalid membership expiry date.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "edit_student",
                        id=id
                    )
                )

        # =================================================
        # PAYMENT
        # =================================================

        total_amount = float(
            student.total_amount or 0
        )

        old_paid_amount = float(
            student.paid_amount or 0
        )

        # Payment received NOW
        new_payment = float(
            request.form.get(
                "new_payment",
                0
            ) or 0
        )

        # Negative payment not allowed
        if new_payment < 0:

            new_payment = 0

        # =================================================
        # CALCULATE PAID
        # =================================================

        paid_amount = (
            old_paid_amount
            + new_payment
        )

        # Paid cannot exceed total
        if paid_amount > total_amount:

            paid_amount = total_amount

        # =================================================
        # CALCULATE DUE
        # =================================================

        due_amount = (
            total_amount
            - paid_amount
        )

        if due_amount < 0:

            due_amount = 0

        # =================================================
        # PAYMENT STATUS
        # =================================================

        if due_amount <= 0:

            payment_status = "Paid"

        else:

            payment_status = "Due"

        # =================================================
        # SAVE PAYMENT
        # =================================================

        student.paid_amount = paid_amount

        student.due_amount = due_amount

        student.payment_status = payment_status

        # =================================================
        # STUDENT STATUS
        # =================================================

        student.status = request.form.get(
            "status",
            student.status or "Active"
        )

        # =================================================
        # SAVE DATABASE
        # =================================================

        try:

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error updating student: {str(e)}",
                "danger"
            )

            return redirect(
                url_for(
                    "edit_student",
                    id=id
                )
            )

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        if payment_status == "Paid":

            payment_message = (
                f"Payment Paid ₹{paid_amount:.2f}"
            )

        else:

            payment_message = (
                f"Paid ₹{paid_amount:.2f} | "
                f"Due ₹{due_amount:.2f}"
            )

        flash(
            f"Student updated successfully! "
            f"{payment_message}",
            "success"
        )

        return redirect(
            url_for("admin_students")
        )

    # =====================================================
    # GET REQUEST
    # =====================================================

    return render_template(
        "admin/edit_student.html",
        student=student
    )
# =========================================================
# DELETE STUDENT
# =========================================================

@app.route(
    "/admin/delete_student/<int:id>",
    methods=["POST"]
)
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    flash(
        "Student deleted successfully!",
        "success"
    )

    return redirect(
        url_for("admin_students")
    )


# =========================================================
# STAFF REGISTER
# =========================================================

@app.route(
    "/staff/register",
    methods=["GET", "POST"]
)
def staff_register():

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        # NOTE:
        # Staff model should be added separately
        # if you want staff registration.

        return redirect(
            "/staff/login"
        )

    return render_template(
        "staff/register.html"
    )


# =========================================================
# ISSUE BOOK
# =========================================================

@app.route(
    "/admin/issue_book",
    methods=["GET", "POST"]
)
def issue_book():

    if "admin_id" not in session:

        return redirect("/")

    if request.method == "POST":

        student_id = int(
            request.form.get(
                "student_id"
            )
        )

        book_id = int(
            request.form.get(
                "book_id"
            )
        )

        book = Book.query.get_or_404(
            book_id
        )

        if book.available_copies <= 0:

            flash(
                "Book is not available!",
                "danger"
            )

            return redirect(
                url_for("issue_book")
            )

        issue = BookIssue(

            student_id=student_id,

            book_id=book_id,

            issue_date=date.today(),

            status="Issued"
        )

        book.available_copies -= 1

        if book.available_copies == 0:

            book.status = "Unavailable"

        db.session.add(issue)

        db.session.commit()

        flash(
            "Book issued successfully!",
            "success"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    students = Student.query.all()

    books = Book.query.filter(
        Book.available_copies > 0
    ).all()

    return render_template(
        "admin/issue_book.html",

        students=students,

        books=books
    )


# =========================================================
# RETURN BOOK
# =========================================================

@app.route(
    "/admin/return_book/<int:id>"
)
def return_book(id):

    if "admin_id" not in session:

        return redirect("/")

    issue = BookIssue.query.get_or_404(id)

    if issue.status == "Issued":

        issue.status = "Returned"

        issue.return_date = date.today()

        issue.book.available_copies += 1

        issue.book.status = "Available"

        db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# STUDENT CHECK-IN
# =========================================================

@app.route(
"/admin/student_checkin",
methods=["GET", "POST"]
)
def student_checkin():


    if "admin_id" not in session:
       return redirect("/")

    students = Student.query.all()

    seats = Seat.query.filter_by(
       status="Available"
    ).all()

    if request.method == "POST":

        student_id = int(
            request.form.get("student_id")
        )

        seat_id = int(
            request.form.get("seat_id")
        )

        duration_hours = int(
            request.form.get("duration_hours")
        )

    # -----------------------------------------
    # CHECK SEAT
    # -----------------------------------------

        seat = Seat.query.get_or_404(
            seat_id
        )

        if seat.status != "Available":

            flash(
                "This seat is already occupied!",
                "danger"
            )

            return redirect(
                url_for("student_checkin")
            )

    # -----------------------------------------
    # CHECK STUDENT ALREADY ACTIVE
    # -----------------------------------------

        active_visit = LibraryVisit.query.filter(
            LibraryVisit.student_id == student_id,
            LibraryVisit.status.in_(
            ["Active", "Expired"]
        )
        ).first()

        if active_visit:

            flash(
                "This student already has an active visit!",
                "danger"
            )

            return render_template(
    "    admin/student_checkin.html",
    students=students,
    seats=seats
)

    # -----------------------------------------
    # START TIME
    # -----------------------------------------

        entry_time = datetime.now()

    # -----------------------------------------
    # EXPECTED END TIME
    # -----------------------------------------

        expected_end_time = (
            entry_time +
            timedelta(hours=duration_hours)
        )

    # -----------------------------------------
    # CREATE VISIT
    # -----------------------------------------

        visit = LibraryVisit(

            student_id=student_id,

            seat_id=seat_id,

            entry_time=entry_time,

            duration_hours=duration_hours,

            expected_end_time=expected_end_time,

            exit_time=None,

            payment=0,

            payment_status="Pending",

            status="Active"
        )

    # -----------------------------------------
    # OCCUPY SEAT
    # -----------------------------------------

        seat.status = "Occupied"

        db.session.add(visit)

        db.session.commit()

        flash(
            "Student checked in successfully!",
            "success"
        )

        return redirect(
            url_for("seat_tracking")
        )

    return render_template(
    "   admin/student_checkin.html",
        students=students,
        seats=seats
    )


# =========================================================
# SEAT TRACKING
# =========================================================
# @app.route("/admin/seat_tracking", methods=["GET", "POST"])
# def seat_tracking():

#     if "admin_id" not in session:
#         return redirect("/")

#     # -----------------------------------------
#     # UPDATE EXPIRED VISITS
#     # -----------------------------------------

#     now = datetime.now()

#     active_visits = LibraryVisit.query.filter_by(
#         status="Active"
#     ).all()

#     for visit in active_visits:

#         if (
#             visit.expected_end_time
#             and now >= visit.expected_end_time
#         ):
#             visit.status = "Expired"

#     db.session.commit()

#     # -----------------------------------------
#     # CHECK-IN FROM SAME PAGE
#     # -----------------------------------------

#     if request.method == "POST":

#         student_id = request.form.get("student_id")
#         seat_id = request.form.get("seat_id")

#         if not student_id or not seat_id:

#             flash(
#                 "Please select student and seat.",
#                 "danger"
#             )

#             return redirect(
#                 url_for("seat_tracking")
#             )

#         student = Student.query.get_or_404(
#             int(student_id)
#         )

#         seat = Seat.query.get_or_404(
#             int(seat_id)
#         )

#         # -----------------------------------------
#         # CHECK SEAT
#         # -----------------------------------------

#         if seat.status != "Available":

#             flash(
#                 "This seat is already occupied!",
#                 "danger"
#             )

#             return redirect(
#                 url_for("seat_tracking")
#             )

#         # -----------------------------------------
#         # CHECK STUDENT
#         # -----------------------------------------

#         existing_visit = LibraryVisit.query.filter(
#             LibraryVisit.student_id == student.id,
#             LibraryVisit.status.in_(
#                 ["Waiting", "Active", "Expired"]
#             )
#         ).first()

#         if existing_visit:

#             flash(
#                 "This student is already checked-in!",
#                 "danger"
#             )

#             return redirect(
#                 url_for("seat_tracking")
#             )

#         # -----------------------------------------
#         # AUTOMATIC TIME
#         # -----------------------------------------

#         entry_time = datetime.now()

#         # Default 8 hour shift
#         duration_hours = 8

#         expected_end_time = (
#             entry_time +
#             timedelta(hours=duration_hours)
#         )

#         # -----------------------------------------
#         # CREATE VISIT
#         # -----------------------------------------

#         visit = LibraryVisit(

#             student_id=student.id,

#             seat_id=seat.id,

#             entry_time=entry_time,

#             duration_hours=duration_hours,

#             expected_end_time=expected_end_time,

#             exit_time=None,

#             payment=0,

#             payment_status="Pending",

#             status="Active"
#         )

#         # -----------------------------------------
#         # OCCUPY SEAT
#         # -----------------------------------------

#         seat.status = "Occupied"

#         db.session.add(visit)

#         db.session.commit()

#         flash(
#             f"{student.name} checked-in successfully!",
#             "success"
#         )

#         return redirect(
#             url_for("seat_tracking")
#         )

#     # -----------------------------------------
#     # SEARCH
#     # -----------------------------------------

#     search = request.args.get(
#         "search",
#         ""
#     ).strip()

#     # -----------------------------------------
#     # ACTIVE / EXPIRED STUDENTS
#     # -----------------------------------------

#     query = LibraryVisit.query.filter(
#         LibraryVisit.status.in_(
#             ["Active", "Expired"]
#         )
#     )

#     # -----------------------------------------
#     # SEARCH
#     # -----------------------------------------

#     if search:

#         query = query.join(
#             Student
#         ).join(
#             Seat
#         ).filter(
#             db.or_(

#                 Student.name.ilike(
#                     f"%{search}%"
#                 ),

#                 Student.reg_no.ilike(
#                     f"%{search}%"
#                 ),

#                 Seat.seat_no.ilike(
#                     f"%{search}%"
#                 )
#             )
#         )

#     visits = query.order_by(
#         LibraryVisit.id.desc()
#     ).all()

#     # -----------------------------------------
#     # STUDENTS
#     # -----------------------------------------

#     students = Student.query.order_by(
#         Student.name.asc()
#     ).all()

#     # -----------------------------------------
#     # AVAILABLE SEATS
#     # -----------------------------------------

#     seats = Seat.query.filter_by(
#         status="Available"
#     ).order_by(
#         Seat.seat_no.asc()
#     ).all()

#     return render_template(
#         "admin/seat_tracking.html",

#         visits=visits,

#         students=students,

#         seats=seats,

#         search=search
#     )
# =========================================================
# VISIT HISTORY
# =========================================================

@app.route("/admin/visit_history")
def visit_history():

    if "admin_id" not in session:
        return redirect("/")

    search = request.args.get(
        "search",
        ""
    ).strip()

    # -----------------------------------------
    # ALL VISITS
    # -----------------------------------------

    query = LibraryVisit.query

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    if search:

        query = query.join(
            Student
        ).filter(
            db.or_(
                Student.name.ilike(
                    f"%{search}%"
                ),

                Student.reg_no.ilike(
                    f"%{search}%"
                ),

                Student.phone.ilike(
                    f"%{search}%"
                )
            )
        )

    # -----------------------------------------
    # LATEST VISIT FIRST
    # -----------------------------------------

    visits = query.order_by(
        LibraryVisit.id.desc()
    ).all()

    return render_template(
        "admin/visit_history.html",
        visits=visits,
        search=search
    )


@app.route(
    "/admin/start_visit/<int:id>"
)
def start_visit(id):

    if "admin_id" not in session:

        return redirect("/")

    visit = LibraryVisit.query.get_or_404(
        id
    )

    # -----------------------------------------
    # ONLY WAITING CAN START
    # -----------------------------------------

    if visit.status == "Waiting":

        start_time = datetime.now()

        visit.entry_time = start_time

        visit.expected_end_time = (
            start_time +
            timedelta(
                hours=visit.duration_hours
            )
        )

        visit.status = "Active"

        # Seat occupied
        visit.seat.status = "Occupied"

        db.session.commit()

        flash(
            f"{visit.student.name} started successfully!",
            "success"
        )

    else:

        flash(
            "This visit cannot be started.",
            "warning"
        )

    return redirect(
        url_for("seat_tracking")
    )


# =========================================================
# STUDENT ENTRY PAGE
# =========================================================
@app.route("/admin/entry")
def student_entry():

    if "admin_id" not in session:
        return redirect("/")

    search = request.args.get(
        "search",
        ""
    ).strip()

    # =========================================
    # ACTIVE STUDENTS
    # =========================================

    query = Student.query.filter_by(
        status="Active"
    )

    if search:

        query = query.filter(
            db.or_(
                Student.name.ilike(
                    f"%{search}%"
                ),
                Student.reg_no.ilike(
                    f"%{search}%"
                )
            )
        )

    students = query.order_by(
        Student.name.asc()
    ).all()


    # =========================================
    # FIND COMPLETED SHIFTS
    # =========================================

    now = datetime.now()

    active_visits = LibraryVisit.query.filter_by(
        status="Active"
    ).all()

    completed_visits = []

    for visit in active_visits:

        student = visit.student

        if not student:
            continue

        shift = student.shift_time

        if not shift:
            continue

        try:

            # Example:
            # "7:00 AM - 10:00 AM"

            parts = shift.split("-")

            if len(parts) != 2:
                continue

            end_text = parts[1].strip()

            # Convert shift end time
            shift_end = datetime.strptime(
                end_text,
                "%I:%M %p"
            ).time()

            # Use today's date
            shift_end_datetime = datetime.combine(
                now.date(),
                shift_end
            )

            # =====================================
            # NIGHT SHIFT
            # Example: 11:00 AM - 12:00 AM
            # =====================================

            if shift_end_datetime < now:

                # Normally this is already completed
                pass


            # =====================================
            # SHIFT COMPLETED
            # =====================================

            if now >= shift_end_datetime:

                completed_visits.append(
                    visit
                )

        except Exception as e:

            print(
                "SHIFT TIME ERROR:",
                student.name,
                student.shift_time,
                e
            )


    # =========================================
    # DEBUG
    # =========================================

    print("--------------------------------")
    print("CURRENT TIME:", now)
    print(
        "COMPLETED VISITS:",
        len(completed_visits)
    )

    for visit in completed_visits:

        print(
            visit.student.name,
            visit.student.reg_no,
            visit.student.shift_time
        )

    print("--------------------------------")


    return render_template(
        "admin/entry.html",
        students=students,
        search=search,
        completed_visits=completed_visits
    )


# =========================================================
# SET STUDENT ENTRY TIME
# =========================================================

@app.route(
    "/admin/entry/student/<int:student_id>",
    methods=["POST"]
)
def student_entry_time(student_id):

    if "admin_id" not in session:
        return redirect("/")

    student = Student.query.get_or_404(
        student_id
    )

    entry_time = request.form.get(
        "entry_time"
    )

    if not entry_time:

        flash(
            "Please enter entry time.",
            "danger"
        )

        return redirect(
            url_for("student_entry")
        )

    try:

        # =========================================
        # ENTRY TIME
        # =========================================

        actual_entry_time = datetime.fromisoformat(
            entry_time
        )


        # =========================================
        # DURATION
        # =========================================

        duration = int(
            student.duration_hours or 0
        )


        if duration <= 0:

            flash(
                "Student duration is not set.",
                "danger"
            )

            return redirect(
                url_for("student_entry")
            )


        # =========================================
        # EXPECTED END TIME
        # =========================================

        expected_end = (
            actual_entry_time
            + timedelta(hours=duration)
        )


        # =========================================
        # CREATE VISIT
        # =========================================

        visit = LibraryVisit(

            student_id=student.id,

            entry_time=actual_entry_time,

            duration_hours=duration,

            expected_end_time=expected_end,

            exit_time=None,

            payment=0,

            payment_date=None,

            payment_status="Pending",

            status="Active"
        )


        db.session.add(visit)

        db.session.commit()


        # =========================================
        # DEBUG
        # =========================================

        print("=================================")
        print("VISIT CREATED")
        print("Student:", student.name)
        print("Entry:", actual_entry_time)
        print("Duration:", duration)
        print("Expected End:", expected_end)
        print("Status:", visit.status)
        print("=================================")


        flash(
            f"{student.name} entry recorded successfully!",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "ENTRY ERROR:",
            e
        )

        flash(
            "Entry save nahi ho payi.",
            "danger"
        )

    return redirect(
        url_for("student_entry")
    )

@app.route(
    "/admin/exit/<int:visit_id>",
    methods=["POST"]
)
def set_exit_time(visit_id):

    if "admin_id" not in session:
        return redirect("/")

    visit = LibraryVisit.query.get_or_404(
        visit_id
    )

    exit_time = request.form.get(
        "exit_time"
    )

    if not exit_time:

        flash(
            "Please enter exit time.",
            "danger"
        )

        return redirect(
            url_for("student_entry")
        )

    try:

        # =========================================
        # SAVE EXIT TIME
        # =========================================

        visit.exit_time = datetime.fromisoformat(
            exit_time
        )

        visit.status = "Completed"


        # =========================================
        # RELEASE STUDENT SEAT
        # =========================================

        student = visit.student

        student.seat_no = None


        db.session.commit()


        flash(
            f"{student.name} exit successfully recorded!",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "EXIT ERROR:",
            e
        )

        flash(
            "Exit time save nahi ho paya.",
            "danger"
        )

    return redirect(
        url_for("student_entry")
    )

@app.route("/admin/payment")
def payment():

    if "admin_id" not in session:
        return redirect("/")

    search = request.args.get("search", "").strip()

    today = date.today()

    # Expired OR Due students
    query = Student.query.filter(
        db.or_(
            Student.membership_end < today,
            Student.due_amount > 0
        )
    )

    # Search
    if search:

        query = query.filter(
            db.or_(
                Student.name.ilike(f"%{search}%"),
                Student.reg_no.ilike(f"%{search}%"),
                Student.phone.ilike(f"%{search}%")
            )
        )

    students = query.order_by(
        Student.name.asc()
    ).all()

    return render_template(
        "admin/payment.html",
        students=students,
        search=search,
        today=today
    )

@app.route("/admin/payment/add", methods=["POST"])
def add_payment():

    if "admin_id" not in session:
        return redirect("/")

    student_id = request.form.get("student_id")
    amount = request.form.get("amount")

    student = Student.query.get(student_id)

    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("payment"))

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        flash("Invalid payment amount!", "danger")
        return redirect(url_for("payment"))

    # Add payment
    student.paid_amount = (student.paid_amount or 0) + amount

    # Calculate due
    student.due_amount = (
        (student.total_amount or 0)
        - student.paid_amount
    )

    if student.due_amount <= 0:
        student.due_amount = 0
        student.payment_status = "Paid"
    else:
        student.payment_status = "Due"

    # Payment date
    student.payment_date = date.today()

    db.session.commit()

    flash("Payment successfully added!", "success")

    return redirect(url_for("payment"))

@app.route(
    "/admin/payment/edit/<int:student_id>",
    methods=["GET", "POST"]
)
def edit_payment(student_id):

    # ==========================================
    # ADMIN LOGIN CHECK
    # ==========================================

    if "admin_id" not in session:
        return redirect("/")


    # ==========================================
    # GET STUDENT
    # ==========================================

    student = Student.query.get_or_404(student_id)


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        try:

            # ==========================================
            # OLD DUE
            # ==========================================

            old_due = float(
                student.due_amount or 0
            )


            # ==========================================
            # MEMBERSHIP PAYMENT
            # ==========================================

            membership_payment = float(
                request.form.get(
                    "membership_payment",
                    0
                ) or 0
            )


            # ==========================================
            # LOCKER PAYMENT
            # ==========================================

            locker_payment = float(
                request.form.get(
                    "locker_payment",
                    0
                ) or 0
            )


            # ==========================================
            # NEW TOTAL
            # ==========================================

            new_total = (
                membership_payment
                + locker_payment
            )


            # ==========================================
            # TOTAL PAYABLE
            # OLD DUE + NEW PAYMENT
            # ==========================================

            total_payable = (
                old_due
                + new_total
            )


            # ==========================================
            # PAYMENT RECEIVED NOW
            # ==========================================

            paid_now = float(
                request.form.get(
                    "paid_amount",
                    0
                ) or 0
            )


            # Negative payment not allowed

            if paid_now < 0:

                paid_now = 0


            # Payment cannot exceed payable amount

            if paid_now > total_payable:

                paid_now = total_payable


            # ==========================================
            # REMAINING DUE
            # ==========================================

            remaining_due = (
                total_payable
                - paid_now
            )


            # ==========================================
            # UPDATE PAYMENT DETAILS
            # ==========================================

            student.membership_payment = (
                membership_payment
            )


            student.locker_payment = (
                locker_payment
            )


            student.total_amount = (
                new_total
            )


            student.paid_amount = (
                paid_now
            )


            student.due_amount = (
                remaining_due
            )


            # ==========================================
            # PAYMENT DATE
            # ==========================================
            # Agar payment receive hua hai
            # tabhi payment date save hogi

            if paid_now > 0:

                student.payment_date = date.today()


            # ==========================================
            # PAYMENT STATUS
            # ==========================================

            if remaining_due > 0:

                student.payment_status = "Due"

            else:

                student.payment_status = "Paid"


            # ==========================================
            # MEMBERSHIP RENEWAL
            # ==========================================

            if new_total > 0:

                # --------------------------------------
                # FIND BASE DATE
                # --------------------------------------

                if student.membership_end:

                    # Membership expired

                    if student.membership_end < date.today():

                        base_date = date.today()

                    else:

                        # Existing membership still active

                        base_date = student.membership_end

                else:

                    base_date = date.today()


                # --------------------------------------
                # ADD 1 MONTH
                # --------------------------------------

                month = base_date.month + 1

                year = base_date.year


                if month > 12:

                    month = 1

                    year += 1


                # --------------------------------------
                # KEEP SAME DAY
                # --------------------------------------

                import calendar


                last_day = calendar.monthrange(
                    year,
                    month
                )[1]


                day = min(
                    base_date.day,
                    last_day
                )


                # --------------------------------------
                # MEMBERSHIP START
                # --------------------------------------

                student.membership_start = (
                    base_date
                )


                # --------------------------------------
                # MEMBERSHIP END
                # --------------------------------------

                student.membership_end = date(
                    year,
                    month,
                    day
                )


            # ==========================================
            # STUDENT STATUS
            # ==========================================

            if student.membership_end:

                if student.membership_end >= date.today():

                    student.status = "Active"

                else:

                    student.status = "Inactive"


            # ==========================================
            # SAVE DATABASE
            # ==========================================

            db.session.commit()


            # ==========================================
            # SUCCESS MESSAGE
            # ==========================================

            flash(
                f"Payment updated successfully for {student.name}.",
                "success"
            )


            # ==========================================
            # REDIRECT
            # ==========================================

            return redirect(
                url_for("payment")
            )


        # ==========================================
        # ERROR
        # ==========================================

        except Exception as e:

            db.session.rollback()


            print(
                "PAYMENT ERROR:",
                e
            )


            flash(
                "Payment update nahi ho paya.",
                "danger"
            )


    # ==========================================
    # PAYMENT EDIT PAGE
    # ==========================================

    return render_template(
        "admin/edit_payment.html",
        student=student
    )
@app.route("/admin/seat-tracking")
def seat_tracking():

    if "admin_id" not in session:
        return redirect("/")

    students = Student.query.filter_by(
        status="Active"
    ).all()

    reserved_students = {}

    for student in students:

        if student.seat_no:

            reserved_students[
                int(student.seat_no)
            ] = student

    total_seats = 130

    return render_template(
        "admin/seat_tracking.html",
        students=students,
        reserved_students=reserved_students,
        total_seats=total_seats
    )
@app.route("/admin/reserve-seat", methods=["POST"])
def reserve_seat():

    student_id = request.form.get("student_id")
    seat_no = request.form.get("seat_no")

    student = Student.query.get_or_404(student_id)

    # Check seat already reserved
    existing = Student.query.filter_by(
        seat_no=int(seat_no)
    ).first()

    if existing:
        flash("This seat is already reserved.", "danger")
        return redirect(url_for("seat_tracking"))

    # Reserve seat
    student.seat_no = int(seat_no)

    db.session.commit()

    flash(
        f"Seat {seat_no} reserved for {student.name}.",
        "success"
    )

    return redirect(url_for("seat_tracking"))

@app.route("/admin/release-seat/<int:student_id>", methods=["POST"])
def release_seat(student_id):

    student = Student.query.get_or_404(student_id)

    seat_no = student.seat_no

    student.seat_no = None

    db.session.commit()

    flash(
        f"Seat {seat_no} is now available.",
        "success"
    )

    return redirect(url_for("seat_tracking"))


# ============================================================
# STUDENT PROFILE
# ============================================================

@app.route("/student/profile")
def student_profile():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])

    if not student:
        session.pop("student_id", None)
        session.pop("student_name", None)

        return redirect(url_for("student_login"))

    return render_template(
        "student/profile.html",
        student=student
    )


# ============================================================
# STUDENT PAYMENT HISTORY
# ============================================================

@app.route("/student/payment-history")
def student_payment_history():

    if "student_id" not in session:
        return redirect("/")

    student = Student.query.get_or_404(
        session["student_id"]
    )

    today = date.today()

    return render_template(
        "student/payment_history.html",
        student=student,
        today=today
    )


# ============================================================
# STUDENT VISIT HISTORY
# ============================================================

@app.route("/student/visit-history")
def student_visit_history():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])

    if not student:
        session.pop("student_id", None)
        session.pop("student_name", None)

        return redirect(url_for("student_login"))

    visits = LibraryVisit.query.filter_by(
        student_id=student.id
    ).order_by(
        LibraryVisit.id.desc()
    ).all()

    return render_template(
        "student/visit_history.html",
        student=student,
        visits=visits
    )


# ============================================================
# STUDENT SEATS
# ============================================================

@app.route("/student/seats")
def student_seats():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    students = Student.query.all()

    reserved_students = {}

    for student in students:

        if student.seat_no:

            try:
                seat_no = int(student.seat_no)
                reserved_students[seat_no] = student

            except (ValueError, TypeError):
                pass

    total_seats = 130

    return render_template(
        "student/seats.html",
        reserved_students=reserved_students,
        total_seats=total_seats
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )