import io
import re
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
import pyotp
import qrcode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security Cookie Settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ph = PasswordHasher()

# --- Database User Model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    otp_secret = db.Column(db.String(32), nullable=True)
    is_2fa_enabled = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            name=self.email, issuer_name="SecureAuthApp"
        )

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Server-Side Input Validator ---
def validate_inputs(username, email, password):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return "Username must be 3-20 characters long and contain only letters, numbers, or underscores."
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Invalid email address format."
    if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
        return "Password must be at least 8 characters long and contain at least one digit and one uppercase letter."
    return None

# --- Routes ---

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        error = validate_inputs(username, email, password)
        if error:
            flash(error, 'danger')
            return render_template('register.html')

        # Check existing user using ORM (SQL Injection Proof)
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists.', 'warning')
            return render_template('register.html')

        new_user = User(username=username, email=email, otp_secret=pyotp.random_base32())
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_2fa_enabled:
                # Redirect to 2FA verification step
                return redirect(url_for('verify_2fa', user_id=user.id))
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/2fa/<int:user_id>', methods=['GET', 'POST'])
def verify_2fa(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        if user.verify_totp(token):
            login_user(user)
            flash('2FA Verification Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA Code. Please try again.', 'danger')

    return render_template('2fa.html', user_id=user_id)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/enable-2fa', methods=['POST'])
@login_required
def enable_2fa():
    token = request.form.get('token', '').strip()
    if current_user.verify_totp(token):
        current_user.is_2fa_enabled = True
        db.session.commit()
        flash('Two-Factor Authentication is now enabled for your account!', 'success')
    else:
        flash('Invalid code. 2FA setup failed.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/qr-code')
@login_required
def qr_code():
    uri = current_user.get_totp_uri()
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('login'))

# --- DB Initialization ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
    