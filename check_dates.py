#!/usr/bin/env python3

from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime

def get_exif_data(image_path):
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if exif is None:
                return {}
            
            exif_data = {}
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                if isinstance(data, bytes):
                    try:
                        data = data.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            data = data.decode('utf-16')
                        except UnicodeDecodeError:
                            data = None
                exif_data[tag] = data
            return exif_data
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")
        return {}

def main():
    photos_dir = '/data/photos'
    for root, _, files in os.walk(photos_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                path = os.path.join(root, file)
                print(f"\nChecking {path}:")
                
                # Get file modification time
                mtime = os.path.getmtime(path)
                mtime_date = datetime.fromtimestamp(mtime)
                print(f"File mtime: {mtime_date}")
                
                # Get EXIF dates
                exif_data = get_exif_data(path)
                date_fields = ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']
                for field in date_fields:
                    if field in exif_data:
                        print(f"{field}: {exif_data[field]}")

if __name__ == '__main__':
    main() 