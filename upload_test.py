#!/usr/bin/env python3

import os
import shutil
import logging
from pathlib import Path
import time
from PIL import Image
from PIL.ExifTags import TAGS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cleanup_target_directory():
    """Remove all existing photos from the target directory."""
    target_dir = Path('local_test/photos')
    if target_dir.exists():
        logger.info(f"Cleaning up {target_dir}")
        for photo in target_dir.glob('*.jpg'):
            photo.unlink()
            logger.info(f"Removed {photo.name}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created target directory {target_dir}")

def get_exif_date(image_path):
    """Extract date from EXIF data."""
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if exif:
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        return exif[tag_id]
    except Exception as e:
        logger.warning(f"Could not read EXIF data for {image_path}: {e}")
    return None

def copy_test_photos():
    """Copy test photos to the local test directory and ensure proper permissions."""
    source_dir = Path('test_photos')
    target_dir = Path('local_test/photos')
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy each photo
    for photo in source_dir.glob('*.jpg'):
        target_path = target_dir / photo.name
        logger.info(f"Copying {photo.name} to {target_path}")
        shutil.copy2(photo, target_path)
        # Ensure proper permissions
        os.chmod(target_path, 0o644)
        
        # Verify EXIF data
        exif_date = get_exif_date(photo)
        if exif_date:
            logger.info(f"EXIF date for {photo.name}: {exif_date}")
        else:
            logger.warning(f"No EXIF date found for {photo.name}")
    
    logger.info("All test photos copied successfully")

def verify_photos():
    """Verify that photos exist in the target directory and have EXIF data."""
    target_dir = Path('local_test/photos')
    if not target_dir.exists():
        logger.error(f"Target directory {target_dir} does not exist")
        return False
    
    photos = list(target_dir.glob('*.jpg'))
    if not photos:
        logger.error("No photos found in target directory")
        return False
    
    logger.info(f"Found {len(photos)} photos in target directory")
    for photo in photos:
        exif_date = get_exif_date(photo)
        logger.info(f"Verified: {photo.name} ({photo.stat().st_size} bytes)")
        if exif_date:
            logger.info(f"  EXIF date: {exif_date}")
        else:
            logger.warning(f"  No EXIF date found")
    return True

def main():
    try:
        # Check if we have photos to process
        if not Path('test_photos').exists():
            logger.error("test_photos directory not found")
            return
        
        # Clean up target directory
        cleanup_target_directory()
        
        # Copy photos to local test directory
        copy_test_photos()
        
        # Verify the photos were copied correctly
        if not verify_photos():
            logger.error("Photo verification failed")
            return
        
        logger.info("Test photos have been copied to local_test/photos")
        logger.info("Next steps:")
        logger.info("1. Review the photos in local_test/photos")
        logger.info("2. Use 'fly deploy' to deploy the changes")
        logger.info("3. Wait for Photoview to scan the new photos (up to 1 hour)")
        logger.info("4. View the photos at https://rogers-photo-gallery.fly.dev")
        
    except Exception as e:
        logger.error(f"Error during upload test: {e}")

if __name__ == "__main__":
    main() 