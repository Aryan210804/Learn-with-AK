from flask import Flask, render_template, url_for, flash, redirect, request, abort, jsonify
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load .env file before anything else reads os.environ
from config import Config
from models import db, User, Roadmap, RoadmapStep, UserRoadmap, UserProgress, Feedback
from forms import SignupForm, LoginForm, RoadmapForm, StepForm, RequestResetForm, ResetPasswordForm, FeedbackForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from functools import wraps
from ai_roadmap import generate_roadmap

app = Flask(__name__)
app.config.from_object(Config)

import os
import shutil

# Vercel filesystem is read-only. We copy the seeded DB to /tmp/ so it's readable and writable.
if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL'):
    source_db = os.path.join(app.config['BASE_DIR'], 'learn_with_ak.db')
    target_db = os.path.join('/tmp', 'learn_with_ak.db')
    if os.path.exists(source_db) and not os.path.exists(target_db):
        shutil.copyfile(source_db, target_db)

db.init_app(app)

def auto_seed():
    """Seed the database automatically if empty. Vercel-friendly."""
    if User.query.filter_by(is_admin=True).first():
        return # Skip if already seeded
    
    print("Auto-seeding database...")
    from roadmap_content import ALL_ROADMAPS
    
    # 1. Create Super Admin
    admin = User(
        username="Admin",
        email=app.config['SUPER_ADMIN_EMAIL'],
        is_admin=True
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()

    # 2. Seed Roadmaps
    for rm_data in ALL_ROADMAPS:
        roadmap = Roadmap(
            title=rm_data["title"],
            description=rm_data["description"],
            category=rm_data["category"],
            difficulty=rm_data["difficulty"],
            created_by=admin.id
        )
        roadmap.set_meta(rm_data["meta_data"])
        db.session.add(roadmap)
        db.session.commit()

        for idx, step_data in enumerate(rm_data["steps"]):
            step = RoadmapStep(
                roadmap_id=roadmap.id,
                step_number=idx + 1,
                title=step_data["title"],
                description=step_data["desc"],
                resources=step_data["resources"],
                level=step_data["level"]
            )
            db.session.add(step)
        db.session.commit()
    print("Auto-seeding complete.")

# Ensure tables are created and data is seeded
with app.app_context():
    db.create_all()
    auto_seed()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Custom Jinja2 filter for formatting dates
@app.template_filter('format_date')
def format_date(value):
    """Format a datetime object to a readable string"""
    if value is None:
        return ""
    # Format: Jan 26, 2026
    return value.strftime('%b %d, %Y')

# --- Public Routes ---

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/browse")
def browse_roadmaps():
    search_query = request.args.get('search', '')
    category = request.args.get('category', 'all')
    
    query = Roadmap.query
    
    if category != 'all':
        query = query.filter_by(category=category)
        
    if search_query:
        query = query.filter(Roadmap.title.ilike(f'%{search_query}%'))
    
    roadmaps = query.all()
    
    followed_ids = []
    if current_user.is_authenticated:
        followed = UserRoadmap.query.filter_by(user_id=current_user.id).all()
        followed_ids = [ur.roadmap_id for ur in followed]
        
    return render_template('user/browse.html', roadmaps=roadmaps, 
                           search_query=search_query, current_category=category,
                           followed_ids=followed_ids)

# Renaming to match template expectation 'follow_roadmap'
@app.route("/roadmap/<int:roadmap_id>/enroll", methods=['POST'])
@login_required
def follow_roadmap(roadmap_id): # Renamed function, route kept for clarity but endpoint is function name
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    # Check if already enrolled
    if UserRoadmap.query.filter_by(user_id=current_user.id, roadmap_id=roadmap.id).first():
        flash('You are already enrolled in this roadmap.', 'info')
    else:
        user_roadmap = UserRoadmap(user_id=current_user.id, roadmap_id=roadmap.id)
        db.session.add(user_roadmap)
        db.session.commit()
        flash(f'You have started learning {roadmap.title}!', 'success')
    return redirect(url_for('view_roadmap', roadmap_id=roadmap_id))

@app.route("/roadmap/<int:roadmap_id>")
def view_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    is_following = False
    progress = 0
    steps_data = []
    
    # Get all steps ordered
    # Logic to populate steps_data with progress if user is logged in
    
    if current_user.is_authenticated:
        # Check following status
        if UserRoadmap.query.filter_by(user_id=current_user.id, roadmap_id=roadmap.id).first():
            is_following = True
            progress = roadmap.get_user_progress(current_user.id)
            
    # Construct steps_data which is a list of dicts or objects with 'step' and 'completed'
    # The template expects: for level_name, steps in steps_data|groupby('step.level')
    # So steps_data should be a list of custom objects or simple dicts
    
    # Let's align with the template expectations: item.step and item.completed
    all_steps = RoadmapStep.query.filter_by(roadmap_id=roadmap.id).order_by(RoadmapStep.step_number).all()
    
    for step in all_steps:
        completed = False
        if current_user.is_authenticated:
            completed = step.is_completed_by_user(current_user.id)
            
        steps_data.append({
            'step': step,
            'completed': completed
        })
            
    return render_template('user/roadmap.html', roadmap=roadmap, 
                           steps_data=steps_data, is_following=is_following,
                           progress=progress)

# --- Authentication ---

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        # First user is admin (optional logic, but stuck to strict reqs)
        # Checking if it's the super admin email
        if form.email.data.lower() == Config.SUPER_ADMIN_EMAIL.lower():
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/signup.html', title='Sign Up', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True) # Always remember for now
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_dashboard'))
        else:
            flash(f'Login Unsuccessful for {form.email.data}. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- User Routes ---

@app.route("/dashboard")
@login_required
def user_dashboard():
    # Helper to get started roadmaps
    roadmap_data = []
    user_roadmaps = UserRoadmap.query.filter_by(user_id=current_user.id).all()
    
    # Calculate stats
    total = len(user_roadmaps)
    completed = 0
    in_progress = 0
    
    for ur in user_roadmaps:
        roadmap = ur.roadmap
        progress = roadmap.get_user_progress(current_user.id)
        
        if progress == 100:
            completed += 1
        else:
            in_progress += 1
            
        roadmap_data.append({
            'roadmap': roadmap,
            'progress': progress
        })
    
    stats = {
        'total': total,
        'completed': completed,
        'in_progress': in_progress
    }
        
    return render_template('user/dashboard.html', stats=stats, roadmap_data=roadmap_data)

@app.route("/roadmap/<int:roadmap_id>/unfollow", methods=['POST'])
@login_required
def unfollow_roadmap(roadmap_id):
    user_roadmap = UserRoadmap.query.filter_by(user_id=current_user.id, roadmap_id=roadmap_id).first()
    if user_roadmap:
        db.session.delete(user_roadmap)
        # Optional: Also delete progress? For now, we keep progress in case they re-follow.
        # But if we want a clean wipe:
        # UserProgress.query.filter_by(user_id=current_user.id, roadmap_id=roadmap_id).delete()
        db.session.commit()
        flash('Roadmap removed from your dashboard.', 'success')
    else:
        flash('Roadmap not found in your dashboard.', 'warning')
    return redirect(url_for('user_dashboard'))

# Duplicate route removed - using follow_roadmap instead

# --- Admin Routes ---

@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    # Comprehensive Statistics
    total_users = User.query.count()
    total_roadmaps = Roadmap.query.count()
    total_steps = RoadmapStep.query.count()
    total_enrollments = UserRoadmap.query.count()
    total_progress = UserProgress.query.filter_by(completed=True).count()
    
    stats = {
        'users': total_users,
        'roadmaps': total_roadmaps,
        'steps': total_steps,
        'enrollments': total_enrollments,
        'completed_steps': total_progress
    }
    
    # Recent users (last 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Recent roadmaps (last 5)
    recent_roadmaps = Roadmap.query.order_by(Roadmap.created_at.desc()).limit(5).all()
    
    # Recent activity (last 10 progress updates)
    recent_activity = UserProgress.query.filter_by(completed=True)\
        .order_by(UserProgress.completed_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                          stats=stats,
                          recent_users=recent_users,
                          recent_roadmaps=recent_roadmaps,
                          recent_activity=recent_activity)

@app.route("/admin/users")
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route("/admin/roadmaps")
@login_required
@admin_required
def admin_roadmaps():
    roadmaps = Roadmap.query.all()
    return render_template('admin/roadmaps.html', roadmaps=roadmaps)

@app.route("/admin/user/<int:user_id>")
@login_required
@admin_required
def admin_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get user's enrolled roadmaps with progress
    enrollments = UserRoadmap.query.filter_by(user_id=user.id).all()
    roadmap_progress = []
    for enrollment in enrollments:
        roadmap = enrollment.roadmap
        progress = roadmap.get_user_progress(user.id)
        roadmap_progress.append({
            'roadmap': roadmap,
            'progress': progress,
            'enrolled_at': enrollment.followed_at
        })
    
    # Get user's progress records (activity)
    progress_records = UserProgress.query.filter_by(user_id=user.id)\
        .order_by(UserProgress.completed_at.desc()).limit(50).all()
    
    # Get user's feedback
    feedbacks = Feedback.query.filter_by(user_id=user.id)\
        .order_by(Feedback.created_at.desc()).all()
    
    # Calculate statistics
    total_enrollments = len(enrollments)
    completed_steps = UserProgress.query.filter_by(user_id=user.id, completed=True).count()
    total_steps = sum([r.roadmap.get_total_steps() for r in enrollments]) if enrollments else 0
    
    stats = {
        'enrollments': total_enrollments,
        'completed_steps': completed_steps,
        'total_steps': total_steps,
        'feedback_count': len(feedbacks)
    }
    
    return render_template('admin/user_detail.html', 
                          user=user, 
                          roadmap_progress=roadmap_progress,
                          progress_records=progress_records,
                          feedbacks=feedbacks,
                          stats=stats)

@app.route("/admin/user/<int:user_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted successfully.', 'success')
    return redirect(url_for('admin_users'))

@app.route("/admin/user/<int:user_id>/reset-password", methods=['POST'])
@login_required
@admin_required
def admin_reset_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get('new_password', '').strip()
    if not new_password or len(new_password) < 6:
        flash('Password must be at least 6 characters.', 'danger')
        return redirect(url_for('admin_user_detail', user_id=user_id))
    user.set_password(new_password)
    db.session.commit()
    flash(f'Password for {user.username} has been reset successfully!', 'success')
    return redirect(url_for('admin_user_detail', user_id=user_id))

@app.route("/user/progress/<int:step_id>", methods=['POST'])
@login_required
def toggle_progress(step_id):
    step = RoadmapStep.query.get_or_404(step_id)
    
    # Check if user is enrolled
    if not UserRoadmap.query.filter_by(user_id=current_user.id, roadmap_id=step.roadmap_id).first():
        return {'success': False, 'message': 'Not enrolled'}, 403
        
    progress_record = UserProgress.query.filter_by(user_id=current_user.id, step_id=step_id).first()
    
    completed = False
    if progress_record:
        # Toggle off
        if progress_record.completed:
            progress_record.completed = False
            progress_record.completed_at = None
        else:
            progress_record.completed = True
            progress_record.completed_at = datetime.utcnow()
        completed = progress_record.completed
    else:
        # Create new record
        progress_record = UserProgress(
            user_id=current_user.id,
            roadmap_id=step.roadmap_id,
            step_id=step.id,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.session.add(progress_record)
        completed = True
        
    db.session.commit()
    
    # Get Updated Roadmap Progress
    roadmap = Roadmap.query.get(step.roadmap_id)
    new_progress = roadmap.get_user_progress(current_user.id)
    
    return {
        'success': True, 
        'completed': completed, 
        'progress': new_progress
    }

@app.route("/admin/roadmap/new", methods=['GET', 'POST'])
@login_required
@admin_required
def add_roadmap():
    form = RoadmapForm()
    if request.method == 'POST':
        if form.validate():
            roadmap = Roadmap(title=form.title.data, 
                              description=form.description.data,
                              category=form.category.data,
                              difficulty=form.difficulty.data,
                              created_by=current_user.id)
            db.session.add(roadmap)
            db.session.commit()
            flash('Roadmap created! Now you can add steps.', 'success')
            return redirect(url_for('edit_roadmap', roadmap_id=roadmap.id))
            
    return render_template('admin/add_roadmap.html', title='New Roadmap', form=form)

@app.route("/admin/roadmap/<int:roadmap_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    form = RoadmapForm(obj=roadmap)
    if form.validate_on_submit():
        roadmap.title = form.title.data
        roadmap.description = form.description.data
        roadmap.category = form.category.data
        roadmap.difficulty = form.difficulty.data
        db.session.commit()
        flash('Roadmap updated successfully!', 'success')
        return redirect(url_for('admin_roadmaps'))
        
    return render_template('admin/add_roadmap.html', title='Edit Roadmap', form=form, roadmap=roadmap)

@app.route("/admin/roadmap/<int:roadmap_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    db.session.delete(roadmap)
    db.session.commit()
    flash(f'Roadmap "{roadmap.title}" has been deleted.', 'success')
    return redirect(url_for('admin_roadmaps'))

@app.route("/admin/roadmap/<int:roadmap_id>/step/add", methods=['POST'])
@login_required
@admin_required
def add_step(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    title = request.form.get('title')
    description = request.form.get('description')
    resources = request.form.get('resources')
    
    if title and description:
        step_number = len(roadmap.steps) + 1
        new_step = RoadmapStep(
            roadmap_id=roadmap.id,
            step_number=step_number,
            title=title,
            description=description,
            resources=resources,
            level=roadmap.difficulty
        )
        db.session.add(new_step)
        db.session.commit()
        flash('Step added successfully!', 'success')
    else:
        flash('Title and description are required.', 'danger')
        
    return redirect(url_for('edit_roadmap', roadmap_id=roadmap_id))

@app.route("/admin/step/<int:step_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_step(step_id):
    step = RoadmapStep.query.get_or_404(step_id)
    roadmap_id = step.roadmap_id
    db.session.delete(step)
    
    # Re-order remaining steps
    remaining_steps = RoadmapStep.query.filter_by(roadmap_id=roadmap_id).order_by(RoadmapStep.step_number).all()
    for i, s in enumerate(remaining_steps):
        s.step_number = i + 1
        
    db.session.commit()
    flash('Step deleted and ordering updated.', 'success')
    return redirect(url_for('edit_roadmap', roadmap_id=roadmap_id))

@app.route("/feedback", methods=['GET', 'POST'])
@login_required
def submit_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            user_id=current_user.id,
            category=form.category.data,
            rating=int(form.rating.data),
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback! It has been sent to the admin.', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('user/feedback.html', title='Feedback', form=form)

@app.route("/admin/feedback")
@login_required
@admin_required
def admin_feedback():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('admin/feedback.html', feedbacks=feedbacks)

@app.route("/admin/feedback/<int:feedback_id>/resolve", methods=['POST'])
@login_required
@admin_required
def resolve_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.status = 'Resolved'
    db.session.commit()
    flash('Feedback marked as resolved.', 'success')
    return redirect(url_for('admin_feedback'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Mock sending email - just flash for now since we don't have mail server setup
        token = user.get_reset_token()
        # In a real app we'd send an email here.
        flash(f'An email has been sent with instructions to reset your password. (Dev Token: {token})', 'info')
        return redirect(url_for('login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)


# --- AI Roadmap Generator ---

@app.route("/ai-roadmap", methods=['GET', 'POST'])
@login_required
def ai_roadmap():
    roadmap_data = None
    topic = ''
    error = None

    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        if not topic:
            error = 'Please enter a topic or skill to generate a roadmap for.'
        elif len(topic) > 200:
            error = 'Topic is too long. Please keep it under 200 characters.'
        else:
            # Check if we already have a roadmap that closely matches this topic
            existing = Roadmap.query.filter(Roadmap.title.ilike(f'%{topic}%')).first()
            if existing:
                flash(f'We found an existing roadmap for "{topic}"!', 'info')
                return redirect(url_for('view_roadmap', roadmap_id=existing.id))

            try:
                # Generate new one via AI
                roadmap_data = generate_roadmap(topic)
                
                # AUTO-SAVE to public roadmaps if it's new
                title = roadmap_data.get('title', f"Learning Path: {topic}")
                
                # Double check exact title match to avoid duplicates
                if not Roadmap.query.filter_by(title=title).first():
                    new_rm = Roadmap(
                        title=title,
                        description=roadmap_data.get('description', ''),
                        category='skill',
                        difficulty=roadmap_data.get('difficulty', 'intermediate').lower(),
                        is_ai_generated=True,
                        created_by=current_user.id if current_user.is_authenticated else None
                    )
                    # Save meta data (skills, tools, etc.)
                    new_rm.set_meta(roadmap_data.get('meta_data', {}))
                    db.session.add(new_rm)
                    db.session.flush() # Get ID

                    for s in roadmap_data.get('steps') or []:
                        res_text = ""
                        for r in (s.get('resources') or []):
                            res_text += f"[{r.get('name')}]({r.get('url')}) — {r.get('type')}\n"
                        
                        step = RoadmapStep(
                            roadmap_id=new_rm.id,
                            step_number=s.get('step_number', 1),
                            title=s.get('title', 'Next Step'),
                            description=s.get('description', ''),
                            resources=res_text.strip(),
                            level=s.get('level', 'Beginner')
                        )
                        db.session.add(step)
                    
                    db.session.commit()
                    flash(f'New roadmap for "{topic}" has been added to our collection!', 'success')
                
            except Exception as e:
                err_msg = str(e)
                # Clean up long API error dumps for the user
                if '429' in err_msg or 'quota' in err_msg.lower():
                    error = ('🚫 AI service is temporarily busy (quota limit reached). '
                             'Try a popular topic like "Data Science" or "Web Development" '
                             'to get a roadmap from our curated collection, or try again later.')
                else:
                    error = err_msg

    return render_template('ai_roadmap.html',
                           roadmap_data=roadmap_data,
                           topic=topic,
                           error=error)


@app.route("/ai-roadmap/save", methods=['POST'])
@login_required
def save_ai_roadmap():
    """Save a previously generated AI roadmap to the database."""
    import json as _json
    try:
        data = request.get_json(force=True)
        roadmap_json = data.get('roadmap')
        if not roadmap_json:
            return jsonify({'success': False, 'message': 'No roadmap data provided.'}), 400

        title = roadmap_json.get('title', 'AI Generated Roadmap')
        description = roadmap_json.get('description', '')
        estimated_time = roadmap_json.get('estimated_time', '')
        difficulty = roadmap_json.get('difficulty', 'Intermediate')

        # Map difficulty to valid DB values
        diff_map = {'Beginner': 'beginner', 'Intermediate': 'intermediate', 'Advanced': 'advanced'}
        difficulty = diff_map.get(difficulty, 'intermediate')

        new_roadmap = Roadmap(
            title=title,
            description=f"{description}\n\nEstimated Time: {estimated_time}",
            category='skill',
            difficulty=difficulty,
            created_by=current_user.id
        )
        db.session.add(new_roadmap)
        db.session.flush()  # Get the ID before commit

        for step_data in (roadmap_json.get('steps') or []):
            resources_text = ''
            for r in (step_data.get('resources') or []):
                resources_text += f"[{r.get('name', '')}]({r.get('url', '')}) — {r.get('type', '')}\n"

            step = RoadmapStep(
                roadmap_id=new_roadmap.id,
                step_number=step_data.get('step_number', 1),
                title=step_data.get('title', ''),
                description=step_data.get('description', ''),
                resources=resources_text.strip(),
                level=difficulty
            )
            db.session.add(step)

        db.session.commit()
        return jsonify({'success': True, 'roadmap_id': new_roadmap.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route("/debug-db")
def debug_db():
    if not os.environ.get('VERCEL'):
        return "Local development"
    
    users = User.query.all()
    user_list = [f"{u.username} ({u.email}) - Admin: {u.is_admin}" for u in users]
    
    db_status = {
        "db_path": Config.SQLALCHEMY_DATABASE_URI,
        "exists": os.path.exists('/tmp/learn_with_ak.db'),
        "users_found": len(user_list),
        "user_details": user_list,
        "super_admin_config": Config.SUPER_ADMIN_EMAIL
    }
    return jsonify(db_status)

if __name__ == '__main__':
    app.run(debug=True)
