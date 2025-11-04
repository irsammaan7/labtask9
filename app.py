import os
from functools import wraps
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from forms import StudentForm, RegisterForm, LoginForm
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load env vars from .env (development convenience)
load_dotenv()

app = Flask(__name__)

# --- Configuration (from env, with safe defaults) ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///firstapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session cookie hardening: enable Secure only in production
if os.getenv('FLASK_ENV', 'development') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
else:
    # For local testing with http://127.0.0.1:5000, we must allow insecure cookies
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.config['SESSION_COOKIE_HTTPONLY'] = True

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

# --- Models ---
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# --- Helper: login_required decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    # Useful debug prints (remove in production)
    app.logger.debug("Form submitted? %s", form.is_submitted())
    app.logger.debug("Form validated? %s", form.validate_on_submit())
    app.logger.debug("Errors: %s", form.errors)

    if form.validate_on_submit():
        student = Student(
            firstname=form.firstname.data.strip(),
            lastname=form.lastname.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip()
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added.', 'success')
        return redirect(url_for('index'))
    allStudents = Student.query.all()
    return render_template('index.html', allStudents=allStudents, form=form)

@app.route('/delete/<int:sno>', methods=['POST'])
@login_required
def delete(sno):
    student = Student.query.filter_by(sno=sno).first_or_404()
    db.session.delete(student)
    db.session.commit()
    flash('Deleted.', 'info')
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    student = Student.query.filter_by(sno=sno).first_or_404()
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.firstname = form.firstname.data.strip()
        student.lastname = form.lastname.data.strip()
        student.email = form.email.data.strip()
        student.phone = form.phone.data.strip()
        db.session.commit()
        flash('Updated.', 'success')
        return redirect(url_for('index'))
    return render_template('update.html', student=student, form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data.strip()).first()
        if existing:
            flash('Username already exists. Choose another.', 'danger')
            return render_template('register.html', form=form)
        u = User(username=form.username.data.strip())
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('User registered. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.args.get('next') or url_for('index')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully.', 'success')
            return redirect(next_url)
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    # In development use debug=True; in production use a proper WSGI server
    debug_flag = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(debug=debug_flag)
