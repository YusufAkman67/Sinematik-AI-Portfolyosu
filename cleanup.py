import os
from sqlalchemy import select, or_
from app import create_app, db
from app.models import Tag

# Load config name from environment or use development default
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

def run_cleanup():
    with app.app_context():
        print("Checking database for tags to clean up...")
        
        # SQLAlchemy 2.x query to find tags that either:
        # - have no associated prompts (~Tag.prompts.any())
        # - are named '##night' or '#night'
        stmt = select(Tag).where(
            or_(
                ~Tag.prompts.any(),
                Tag.name.in_(['##night', '#night'])
            )
        )
        tags_to_delete = db.session.scalars(stmt).all()
        
        deleted_count = 0
        if tags_to_delete:
            print(f"Found {len(tags_to_delete)} tag(s) to delete:")
            for tag in tags_to_delete:
                prompt_count = len(tag.prompts)
                print(f"  - [DELETE] Tag ID: {tag.id}, Name: '{tag.name}', Associated Prompts: {prompt_count}")
                db.session.delete(tag)
                deleted_count += 1
            
            db.session.commit()
            print(f"Success: Database cleanup completed. Total {deleted_count} tag(s) deleted.")
        else:
            print("No tags found that match the cleanup criteria.")

if __name__ == '__main__':
    run_cleanup()
