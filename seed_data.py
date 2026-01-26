from app import app, db
from models import User, Roadmap, RoadmapStep, Feedback, UserRoadmap, UserProgress
from config import Config
from roadmap_content import ALL_ROADMAPS
import json

def seed_database():
    with app.app_context():
        # Drop and Recreate tables to update schema
        db.drop_all()
        db.create_all()
        print("Database schema updated and reset.")

        # 1. Create Super Admin
        admin = User(
            username="AryanKumar",
            email=Config.SUPER_ADMIN_EMAIL,
            is_admin=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print(f"Admin User created: {Config.SUPER_ADMIN_EMAIL}")

        # 2. Seed Roadmaps from Content File
        print(f"Seeding {len(ALL_ROADMAPS)} roadmaps...")
        
        for rm_data in ALL_ROADMAPS:
            roadmap = Roadmap(
                title=rm_data["title"],
                description=rm_data["description"],
                category=rm_data["category"],
                difficulty=rm_data["difficulty"],
                created_by=admin.id
            )
            # Set the rich metadata
            roadmap.set_meta(rm_data["meta_data"])
            
            db.session.add(roadmap)
            db.session.commit()

            for idx, step_data in enumerate(rm_data["steps"]):
                step = RoadmapStep(
                    roadmap_id=roadmap.id,
                    step_number=idx + 1,
                    title=step_data["title"],
                    description=step_data["desc"], # Using 'desc' to match content file
                    resources=step_data["resources"],
                    level=step_data["level"]
                )
                db.session.add(step)
            
            db.session.commit()

        print("Rich Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
