"""
Helper script to set admin flag for the super admin email
Run this if admin panel is not showing after login
"""
from app import app
from models import db, User
from config import Config

with app.app_context():
    # Find user by admin email
    admin_user = User.query.filter_by(email=Config.SUPER_ADMIN_EMAIL).first()
    
    if admin_user:
        print(f"Found user: {admin_user.username} ({admin_user.email})")
        print(f"Current admin status: {admin_user.is_admin}")
        
        if not admin_user.is_admin:
            admin_user.is_admin = True
            db.session.commit()
            print(f"✅ Admin flag set to True for {admin_user.username}")
            print("\n⚠️  IMPORTANT: Log out and log back in for changes to take effect!")
        else:
            print(f"✅ User already has admin privileges")
            print("\n⚠️  If admin panel is not showing, please LOG OUT and LOG BACK IN")
    else:
        print(f"❌ No user found with email: {Config.SUPER_ADMIN_EMAIL}")
        print("Please sign up with this email first")
