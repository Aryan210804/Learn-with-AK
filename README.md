# Learn with AK – AI-Powered Skill & Career Roadmap Platform

Learn with AK is a production-ready, full-stack learning platform designed to help users navigate their career and skill acquisition journeys through structured, AI-enhanced roadmaps. **Optimized for Vercel Deployment.**

## 🚀 Key Features

- **✨ AI Roadmap Generator**: Instantly generate custom learning paths for any topic using **Google Gemini AI**.
- **📋 Curated Roadmaps**: Over 18+ high-quality, pre-built roadmaps covering IT, AI/ML, Cloud, Cyber, Govt Exams, Finance, and more.
- **Personalized Dashboards**: Track your learning progress with real-time visual indicators.
- **Progress Tracking**: Interactive steps with completion toggles and automated progress percentage calculation.
- **Admin Command Center**: Powerful panel to manage users, curation, and user feedback.
- **Modern Cyber Aesthetics**: A premium, vibrant dark theme (Electric Blue, Cyber Purple, Emerald Green).
- **Vercel Friendly**: Fully optimized for serverless deployment with automated database seeding and /tmp storage handling.

## 🛠️ Tech Stack

- **Backend**: Python 3 (Flask)
- **AI Engine**: Google Gemini (generativeai)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla Performance)
- **Database**: SQLite (SQLAlchemy ORM) - *Smart Serverless Migration*
- **Deployment**: Vercel & Gunicorn

## 📂 Project Structure

```text
learn-with-ak/
├── app.py              # Main Application & Auto-Seeding Logic
├── ai_roadmap.py       # Gemini AI Integration & Offline Fallback
├── config.py           # Environment & Vercel Config
├── roadmap_content.py  # 18+ Curated Roadmap Datasets
├── models.py           # Database Schema (SQLAlchemy)
├── static/             # Assets (CSS, JS, Images)
├── templates/          # HTML Templates (Jinja2)
└── vercel.json         # Vercel Deployment Configuration
```

## ⚙️ Deployment to Vercel

1. **GitHub**: Push this repository to your GitHub account.
2. **Vercel**: Import the project.
3. **Environment Variables**:
   - `GEMINI_API_KEY`: Your Google AI Studio API Key.
   - `SECRET_KEY`: A secure random string for sessions.
4. **Deploy**: Vercel will automatically build the project using `vercel.json`.

## ⚙️ Local Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup .env**:
   Create a `.env` file and add your `GEMINI_API_KEY`.
3. **Run the Application**:
   ```bash
   python app.py
   ```
   *Note: The database will auto-seed with 18+ roadmaps on the first run.*

## 👑 Admin Access

The platform features a built-in admin panel accessible only to the super-admin.

- **Default Admin Email**: `aryankumar735588@gmail.com`


**Admin Features**:
- Real-time dashboard statistics.
- User management and feedback resolution.
- Manual roadmap & step curation.
- Performance monitoring.

## 👤 User Experience

- **AI Generation**: Type any topic; get a custom roadmap in seconds.
- **Browse & Filter**: Find specialized roadmaps by category.
- **Interactive Tracking**: Progress bars update instantly as you complete steps.
- **Feedback Loops**: Submit feature requests or report bugs directly to admins.

## 📄 License

© 2026 ARYAN KUMAR OJHA. All Rights Reserved.
