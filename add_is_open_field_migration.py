"""
Migration script to add is_open field to service_providers table
Run this script to update the database schema
"""
from app import create_app, db
from app.models import QuickFix

def add_is_open_field():
    """Add is_open field to service_providers table"""
    app = create_app()
    with app.app_context():
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('service_providers')]
            
            if 'is_open' not in columns:
                # Add the column using raw SQL
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE service_providers ADD COLUMN is_open BOOLEAN DEFAULT 1'))
                    conn.commit()
                print("✓ Successfully added is_open column to service_providers table")
                
                # Update all existing providers to be open by default
                QuickFix.query.update({QuickFix.is_open: True})
                db.session.commit()
                print("✓ Set all existing providers to 'Open' status")
            else:
                print("✓ is_open column already exists")
                
        except Exception as e:
            print(f"✗ Error adding is_open field: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("Adding is_open field to service_providers table...")
    add_is_open_field()
    print("Migration completed!")
