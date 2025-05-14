#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from PIL import Image
import imagehash
import logging
from typing import List, Dict, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageDeduplicator:
    def __init__(self, input_dir: str):
        self.input_dir = Path(input_dir)
        self.deduplicated_dir = Path('deduplicated_photos')
        self.duplicate_dir = Path('duplicate_photos')
        
        # Create output directories if they don't exist
        self.deduplicated_dir.mkdir(parents=True, exist_ok=True)
        self.duplicate_dir.mkdir(parents=True, exist_ok=True)
        
        # Store hashes of processed images
        self.image_hashes: Dict[str, str] = {}
        
    def calculate_image_hash(self, image_path: Path) -> str:
        """Calculate perceptual hash of an image."""
        try:
            with Image.open(image_path) as img:
                # Use average hash for initial implementation
                return str(imagehash.average_hash(img))
        except Exception as e:
            logger.error(f"Error processing {image_path}: {str(e)}")
            return None

    def process_images(self):
        """Process all images in the input directory and its subdirectories."""
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png']:
            image_files.extend(self.input_dir.rglob(f'*{ext}'))
        
        total_files = len(image_files)
        logger.info(f"Found {total_files} image files to process")
        
        for i, image_path in enumerate(image_files, 1):
            logger.info(f"Processing {i}/{total_files}: {image_path.name}")
            
            # Calculate hash
            img_hash = self.calculate_image_hash(image_path)
            if not img_hash:
                continue
                
            # Check for duplicates
            if img_hash in self.image_hashes:
                logger.info(f"Found duplicate: {image_path.name} matches {self.image_hashes[img_hash]}")
                shutil.move(str(image_path), str(self.duplicate_dir / image_path.name))
            else:
                self.image_hashes[img_hash] = image_path.name
                shutil.move(str(image_path), str(self.deduplicated_dir / image_path.name))

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Deduplicate images using perceptual hashing')
    parser.add_argument('input_dir', help='Directory containing images to process')
    
    args = parser.parse_args()
    
    deduplicator = ImageDeduplicator(args.input_dir)
    deduplicator.process_images()

if __name__ == '__main__':
    main() 