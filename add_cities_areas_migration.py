"""
Migration script to add City and Area tables
Run this script to create the cities and areas tables in the database
"""
from app import create_app, db
from app.models import City, Area

def migrate():
    """Create City and Area tables"""
    app = create_app()
    with app.app_context():
        print("Creating City and Area tables...")
        
        # Create tables
        db.create_all()
        
        # Add default cities and areas (Ahmedabad example)
        print("Adding default city and areas...")
        
        # Check if Ahmedabad already exists
        ahmedabad = City.query.filter_by(name='Ahmedabad').first()
        if not ahmedabad:
            ahmedabad = City(name='Ahmedabad', state='Gujarat')
            db.session.add(ahmedabad)
            db.session.commit()
            print(f"Added city: Ahmedabad")
            
            # Add default areas for Ahmedabad
            default_areas = [
                'Maninagar',
                'Bopal',
                'Satellite',
                'Vastrapur',
                'Navrangpura',
                'Paldi',
                'Thaltej',
                'Ghatlodia',
                'Chandkheda',
                'Naranpura'
            ]
            
            for area_name in default_areas:
                area = Area(name=area_name, city_id=ahmedabad.id)
                db.session.add(area)
            
            db.session.commit()
            print(f"Added {len(default_areas)} areas to Ahmedabad")
        else:
            print("Ahmedabad already exists in database")
        
        print("\nMigration completed successfully!")
        print(f"Total cities: {City.query.count()}")
        print(f"Total areas: {Area.query.count()}")

if __name__ == '__main__':
    migrate()
