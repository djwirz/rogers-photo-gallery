#!/usr/bin/env python3

import os
import shutil
import logging
from pathlib import Path
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def copy_test_photos():
    """Copy test photos to the local test directory."""
    source_dir = Path('test_photos')
    target_dir = Path('local_test/photos')
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy each photo
    for photo in source_dir.glob('*.jpg'):
        target_path = target_dir / photo.name
        logger.info(f"Copying {photo.name} to {target_path}")
        shutil.copy2(photo, target_path)
    
    logger.info("All test photos copied successfully")

def main():
    try:
        # Check if we have test photos
        if not Path('test_photos').exists():
            logger.error("test_photos directory not found")
            return
        
        # Copy photos to local test directory
        copy_test_photos()
        
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