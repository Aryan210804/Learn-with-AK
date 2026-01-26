from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    followed_roadmaps = db.relationship('UserRoadmap', back_populates='user', cascade='all, delete-orphan')
    progress = db.relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')
    created_roadmaps = db.relationship('Roadmap', back_populates='creator', foreign_keys='Roadmap.created_by')
    feedback = db.relationship('Feedback', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        """Generate a secure token for password reset"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        """Verify the reset token and return user"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Roadmap(db.Model):
    """Roadmap model with enhanced metadata support"""
    __tablename__ = 'roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # skill, course, job
    difficulty = db.Column(db.String(50), nullable=False)  # beginner, intermediate, advanced
    
    # New Fields for AI and Rich Content
    is_ai_generated = db.Column(db.Boolean, default=False)
    meta_data = db.Column(db.Text, default='{}')  # JSON string for skills, tools, career info
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    steps = db.relationship('RoadmapStep', back_populates='roadmap', cascade='all, delete-orphan', order_by='RoadmapStep.step_number')
    user_roadmaps = db.relationship('UserRoadmap', back_populates='roadmap', cascade='all, delete-orphan')
    progress_records = db.relationship('UserProgress', back_populates='roadmap', cascade='all, delete-orphan')
    creator = db.relationship('User', back_populates='created_roadmaps', foreign_keys=[created_by])
    
    def get_meta(self):
        """Parse meta_data JSON string to dictionary"""
        try:
            return json.loads(self.meta_data)
        except:
            return {}
            
    def set_meta(self, data):
        """Set meta_data from dictionary"""
        self.meta_data = json.dumps(data)
    
    def get_total_steps(self):
        """Get total number of steps in roadmap"""
        return len(self.steps)
    
    def get_user_progress(self, user_id):
        """Calculate user's progress percentage for this roadmap"""
        total_steps = self.get_total_steps()
        if total_steps == 0:
            return 0
        
        completed_steps = UserProgress.query.filter_by(
            user_id=user_id,
            roadmap_id=self.id,
            completed=True
        ).count()
        
        return int((completed_steps / total_steps) * 100)
    
    def __repr__(self):
        return f'<Roadmap {self.title}>'


class RoadmapStep(db.Model):
    """Individual steps with level support"""
    __tablename__ = 'roadmap_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    
    # New Level Field
    level = db.Column(db.String(50), default='Beginner')  # Beginner, Intermediate, Advanced
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    resources = db.Column(db.Text)  # JSON string or generic text
    
    # Relationships
    roadmap = db.relationship('Roadmap', back_populates='steps')
    progress_records = db.relationship('UserProgress', back_populates='step', cascade='all, delete-orphan')
    
    def is_completed_by_user(self, user_id):
        """Check if this step is completed by a specific user"""
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            step_id=self.id,
            completed=True
        ).first()
        return progress is not None
    
    def __repr__(self):
        return f'<RoadmapStep {self.step_number}: {self.title}>'


class UserRoadmap(db.Model):
    """Many-to-many relationship between users and roadmaps"""
    __tablename__ = 'user_roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='followed_roadmaps')
    roadmap = db.relationship('Roadmap', back_populates='user_roadmaps')
    
    # Ensure unique user-roadmap pairs
    __table_args__ = (db.UniqueConstraint('user_id', 'roadmap_id', name='unique_user_roadmap'),)
    
    def __repr__(self):
        return f'<UserRoadmap User:{self.user_id} Roadmap:{self.roadmap_id}>'


class UserProgress(db.Model):
    """Track user progress on individual roadmap steps"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('roadmap_steps.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='progress')
    roadmap = db.relationship('Roadmap', back_populates='progress_records')
    step = db.relationship('RoadmapStep', back_populates='progress_records')
    
    # Ensure unique user-step pairs
    __table_args__ = (db.UniqueConstraint('user_id', 'step_id', name='unique_user_step'),)
    
    def __repr__(self):
        return f'<UserProgress User:{self.user_id} Step:{self.step_id} Completed:{self.completed}>'


class Feedback(db.Model):
    """User feedback queries and suggestions"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General') # Custom, Bug, Feature
    rating = db.Column(db.Integer, default=5) # 1-5 stars
    status = db.Column(db.String(20), default='New') # New, Read, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='feedback')
    
    def __repr__(self):
        return f'<Feedback {self.id}: {self.category}>'
