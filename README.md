# 🔐 SecureAuth – Secure Authentication System

SecureAuth is a Flask-based authentication system that demonstrates modern authentication and web security practices. The application provides secure user registration, login, session management, password hashing using **Argon2id**, and optional **Time-based One-Time Password (TOTP) Two-Factor Authentication (2FA)** for enhanced account security.

The project is designed for educational purposes to showcase secure authentication techniques, password protection, session handling, and user account management using Python and Flask.

> **Note:** This project is intended for learning and demonstration purposes. It should be reviewed and further hardened before being used in a production environment.

---

# ✨ Features

* 🔑 Secure user registration
* 👤 User login and logout
* 🔒 Password hashing using **Argon2id**
* 🗄️ SQLite database integration
* 🛡️ SQL injection protection through ORM/parameterized database queries
* ✅ Input validation for usernames, emails, and passwords
* 🔐 Session management with protected routes
* 📱 Optional Time-based One-Time Password (TOTP) Two-Factor Authentication
* 📷 QR code generation for authenticator applications
* 📊 Responsive and user-friendly interface

---

# 🖥️ Technology Stack

## Backend

* Python
* Flask
* SQLite
* SQLAlchemy
* Argon2
* PyOTP

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap (if applicable)

---

# 🔒 Security Features

SecureAuth incorporates several security practices, including:

* Argon2id password hashing
* Passwords are never stored in plain text
* User session management
* Logout functionality
* Input validation
* Protection against SQL injection using parameterized database operations
* Time-based One-Time Password (TOTP) verification
* QR code generation for authenticator setup

---

# 📱 Two-Factor Authentication (2FA)

SecureAuth supports optional TOTP-based Two-Factor Authentication.

Compatible authenticator applications include:

* Google Authenticator
* Microsoft Authenticator
* Authy

Once enabled, users must enter a valid six-digit verification code after logging in with their username and password.

---

# 📂 Project Structure

```text
SecureAuth/
│
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── README.md
│
├── database/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    └── 2fa.html
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/SecureAuth-Flask-Authentication-System.git
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the Application

```bash
python app.py
```

## 4. Open the Application

Navigate to:

```text
http://127.0.0.1:5000
```

---

# 📸 Application Workflow

### User Registration

* Register with a unique username and valid email address.
* Passwords are securely hashed using Argon2id before storage.

### User Login

* Authenticate using registered credentials.
* A secure session is created upon successful login.

### Enable Two-Factor Authentication

* Generate a QR code from the dashboard.
* Scan it using a compatible authenticator application.
* Verify the generated six-digit code to enable 2FA.

### Login with 2FA

* After successful username/password authentication, users with 2FA enabled are prompted to enter their six-digit verification code.
* Access is granted only after successful verification.

### Logout

* Securely ends the authenticated session and redirects the user to the login page.

---

# 🎯 Learning Objectives

This project demonstrates practical implementation of:

* Secure user authentication
* Password hashing with Argon2id
* Session management
* Flask web development
* SQLite database integration
* Two-Factor Authentication (TOTP)
* QR code generation
* Secure coding practices

---

# 📚 Future Improvements

Potential enhancements include:

* Password reset via email
* Account verification through email
* Remember Me functionality
* Login activity logs
* Account lockout after repeated failed login attempts
* OAuth login (Google, GitHub, Microsoft)
* User profile management

---

# 📄 License

This project is released under the **MIT License**.


