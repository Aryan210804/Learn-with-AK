# Learn with AK – Personalized Skill & Career Roadmap Platform

Learn with AK is a production-ready, full-stack learning platform designed to help users navigate their career and skill acquisition journeys through structured roadmaps.

## 🚀 Key Features

- **Personalized Dashboards**: Track your learning progress with visual indicators.
- **Structured Roadmaps**: Step-by-step guides for Skills (Python, AI), Courses (Web Dev), and Job Roles (Data Analyst).
- **Progress Tracking**: Mark steps as completed and monitor your percentage for each roadmap.
- **Admin Panel**: Comprehensive management system for users and roadmaps.
- **Modern Neon UI**: Vibrant dark theme with Electric Blue, Cyber Purple, and Emerald Green accents.
- **Responsive Design**: Optimized for mobile, tablet, and desktop.

## 🛠️ Tech Stack

- **Backend**: Python 3 (Flask)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## 📂 Project Structure

```text
learn-with-ak/
├── app.py              # Application entry point & routes
├── config.py           # Configuration & Secret Keys
├── models.py           # Database Schema (SQLAlchemy)
├── forms.py            # Form validation (WTForms)
├── utils.py            # Helper decorators & functions
├── seed_data.py        # Database seeding script
├── static/             # Assets (CSS, JS, Images)
└── templates/          # HTML Templates (Jinja2)
```

## ⚙️ Setup & Installation

1. **Clone the project** to your local machine.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the Database**:
   ```bash
   python seed_data.py
   ```
4. **Run the Application**:
   ```bash
   python app.py
   ```
## 👑 Admin Access

The platform features a built-in admin panel for the designated super-admin email.

- **Admin Email**: `aryankumar735588@gmail.com`

**Admin Features**:
- Dashboard statistics
- User management (View/Delete)
- Roadmap management (Add/Edit/Delete)
- Roadmap Step creation

## 👤 User Features

- **Sign up / Login**: Secure authentication.
- **Browse**: Filter roadmaps by category (Skills, Courses, Jobs) or search by keyword.
- **Follow**: Add roadmaps to your personal dashboard.
- **Track**: Click steps to mark them as completed; your progress bar updates in real-time.

## 📄 License

© 2026 ARYAN KUMAR OJHA. All Rights Reserved.
