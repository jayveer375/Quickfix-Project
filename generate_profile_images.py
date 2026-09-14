"""
Generate profile images for all dummy providers
Creates colorful avatar images with initials
Usage: python generate_profile_images.py
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, QuickFix

# Color palette for avatars
COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788',
    '#E63946', '#F77F00', '#06AED5', '#073B4C', '#118AB2',
    '#EF476F', '#FFD166', '#06FFA5', '#073B4C', '#1B9AAA'
]

def get_initials(name):
    """Get initials from name"""
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return "?"

def create_avatar(name, size=200):
    """Create a circular avatar with initials"""
    # Create image
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # Random background color
    bg_color = random.choice(COLORS)
    
    # Draw circle
    draw.ellipse([0, 0, size, size], fill=bg_color)
    
    # Get initials
    initials = get_initials(name)
    
    # Try to use a nice font, fallback to default
    try:
        # Try different font paths
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            'C:\\Windows\\Fonts\\arial.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size // 2)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Draw text
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - 10)
    draw.text(position, initials, fill='white', font=font)
    
    return img

def generate_profile_images():
    """Generate profile images for all providers without images"""
    app = create_app('development')
    
    with app.app_context():
        print("🎨 Generating profile images for providers...")
        print("=" * 60)
        
        # Create uploads directory if it doesn't exist
        upload_folder = app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Get all provider users
        providers = User.query.filter_by(role='provider').all()
        
        generated_count = 0
        skipped_count = 0
        
        for provider in providers:
            # Check if already has a custom profile image
            if provider.profile_image and provider.profile_image != 'default.png':
                image_path = os.path.join(upload_folder, provider.profile_image)
                if os.path.exists(image_path):
                    skipped_count += 1
                    continue
            
            # Generate filename
            filename = f"provider_{provider.id}_{provider.name.replace(' ', '_').lower()}.png"
            filepath = os.path.join(upload_folder, filename)
            
            # Create avatar
            avatar = create_avatar(provider.name)
            avatar.save(filepath)
            
            # Update user profile image
            provider.profile_image = filename
            
            # Update QuickFix profile image if exists
            if provider.provider_profile:
                provider.provider_profile.profile_image = filename
            
            generated_count += 1
            
            if generated_count % 10 == 0:
                print(f"✅ Generated {generated_count} profile images...")
        
        # Commit changes
        db.session.commit()
        
        print("=" * 60)
        print(f"✨ Generated {generated_count} new profile images")
        print(f"⏭️  Skipped {skipped_count} providers (already have images)")
        print(f"📁 Images saved to: {upload_folder}")
        print("=" * 60)
        print("🎉 Profile image generation completed!")

if __name__ == '__main__':
    generate_profile_images()
