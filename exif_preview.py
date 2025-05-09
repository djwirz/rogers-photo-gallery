#!/usr/bin/env python3

import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import logging
from collections import defaultdict
import re
import argparse
import piexif
from time import mktime
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_exif_data(image_path: Path) -> dict:
    """Extract EXIF data from an image."""
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
        logger.error(f"Error reading EXIF from {image_path}: {e}")
        return {}

def get_prefix(filename: str) -> str:
    """Determine the prefix based on the original filename."""
    filename_lower = filename.lower()
    if filename.startswith('scans_'):
        return 'SCAN_'
    elif filename.startswith('set_'):
        return 'SET_'
    elif filename.startswith('scandanavianinininini_'):
        return 'SCAN_'  # These are also scanned photos
    else:
        return 'PIC_'

def extract_year_from_filename(filename: str) -> tuple:
    """Extract year from filename patterns."""
    # For scans with explicit years
    if filename.startswith(('scans_', 'scandanavianinininini_')):
        # Look for year patterns in the filename
        year_patterns = [
            (r'19\d{2}', 1900, 1999),  # 1900-1999
            (r'18\d{2}', 1800, 1899),  # 1800-1899
            (r'20[0-2]\d', 2000, 2025)  # 2000-2025
        ]
        for pattern, min_year, max_year in year_patterns:
            match = re.search(pattern, filename)
            if match:
                year = int(match.group(0))
                if min_year <= year <= max_year:
                    return year, 'FILENAME_YEAR'
    return None, None

def is_valid_date(date_str: str, min_year=1800) -> bool:
    """Check if a date string represents a valid and reasonable date."""
    try:
        date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        # Only check minimum year, allow any future year since these are historical photos
        return date.year >= min_year
    except ValueError:
        return False

def extract_date_from_filename(filename: str) -> tuple:
    """Extract date information from filename patterns."""
    # For scanned photos, try to extract year from filename or use default
    if filename.startswith('scans_'):
        if '_2_' in filename:  # Second batch of scans are older
            return '18850101_000000', 'FILENAME_SCAN_2'
        return '19300101_000000', 'FILENAME_SCAN_1'
    
    # For Scandinavian photos
    if filename.startswith('scandanavianinininini_'):
        return '19200101_000000', 'FILENAME_SCANDINAVIAN'
    
    # For set photos
    if filename.startswith('set_'):
        set_num = re.search(r'set_(\d+)', filename)
        if set_num:
            # Estimate year based on set number (1-7)
            year = 1955 + int(set_num.group(1))
            return f'{year}0101_000000', 'FILENAME_SET'
    
    # For regular photos
    if filename.startswith('Picture_'):
        num = re.search(r'Picture_(\d+)', filename)
        if num:
            # Pictures are roughly chronological, estimate year based on number
            pic_num = int(num.group(1))
            if pic_num < 500:
                return '20080101_000000', 'FILENAME_PICTURE_EARLY'
            elif pic_num < 700:
                return '20090101_000000', 'FILENAME_PICTURE_MID'
            else:
                return '20100101_000000', 'FILENAME_PICTURE_LATE'
    
    return None, None

def extract_date(exif_data: dict, file_path: str) -> tuple:
    """Extract date information from EXIF data or file metadata."""
    filename = os.path.basename(file_path)
    
    # First check User Comment for year information
    if 'User Comment' in exif_data:
        try:
            comment_data = json.loads(exif_data['User Comment'])
            if 'year' in comment_data and comment_data['year']:
                year = str(comment_data['year'])
                # Use January 1st as default date if only year is known
                return f"{year}0101_000000", 'USER_COMMENT_YEAR'
        except (json.JSONDecodeError, ValueError):
            pass
    
    # Try EXIF dates, but skip scan dates (2009)
    date_fields = ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']
    for field in date_fields:
        if field in exif_data:
            date_str = str(exif_data[field])
            try:
                date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                # Skip 2009 dates as they are scan dates
                if date.year != 2009:
                    return date.strftime('%Y%m%d_%H%M%S'), f'EXIF_{field}'
            except ValueError:
                pass
    
    # Try to extract date from filename
    filename_date, source = extract_date_from_filename(filename)
    if filename_date:
        return filename_date, source
    
    # Use file modification time as last resort
    try:
        mtime = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(mtime)
        # Skip 2009 dates as they are scan dates
        if date.year != 2009:
            return date.strftime('%Y%m%d_%H%M%S'), 'FILE_MTIME'
    except Exception as e:
        logger.error(f"Error getting file modification time for {file_path}: {e}")
    
    # If no valid date found, use 1900 instead of None
    # This prevents Photoview from using 2025 as a fallback
    return '19000101_000000', 'DEFAULT_HISTORICAL'

def analyze_exif_data(image_files: list) -> dict:
    """Analyze what EXIF data is available across all images."""
    exif_stats = defaultdict(int)
    date_sources = defaultdict(int)
    date_years = defaultdict(int)
    date_quality = defaultdict(int)
    total_files = len(image_files)
    
    for image_path in image_files:
        exif_data = get_exif_data(image_path)
        for tag in exif_data:
            exif_stats[tag] += 1
        
        # Track date source and year
        date_str, date_source = extract_date(exif_data, str(image_path))
        date_sources[date_source] += 1
        
        try:
            if date_str != 'unknown_date':
                year = int(date_str[:4])
                if year != 2009:  # Skip scan dates
                    date_years[year] += 1
                    
                # Track date quality
                if '_VALID' in date_source:
                    date_quality['EXACT'] += 1
                elif '_DEFAULT_DATE' in date_source:
                    date_quality['YEAR_ONLY'] += 1
                elif '_NO_TIME' in date_source:
                    date_quality['DATE_ONLY'] += 1
                else:
                    date_quality['APPROXIMATE'] += 1
        except ValueError:
            pass
    
    return {
        'tags': {tag: (count, f"{(count/total_files)*100:.1f}%") 
                for tag, count in sorted(exif_stats.items(), key=lambda x: x[1], reverse=True)},
        'date_sources': {source: (count, f"{(count/total_files)*100:.1f}%")
                        for source, count in sorted(date_sources.items(), key=lambda x: x[1], reverse=True)},
        'years': dict(sorted(date_years.items())),
        'date_quality': {quality: (count, f"{(count/total_files)*100:.1f}%")
                        for quality, count in sorted(date_quality.items(), key=lambda x: x[1], reverse=True)}
    }

def generate_filename(exif_data: dict, original_name: str) -> tuple:
    """Generate a filename based on EXIF data."""
    # Get prefix based on original filename
    prefix = get_prefix(original_name)
    
    # Get date and its source
    date_str, date_source = extract_date(exif_data, original_name)
    
    # Get original extension
    ext = os.path.splitext(original_name)[1].lower()
    
    # Generate new filename
    if date_str is None:
        # If no date found, use original filename with prefix
        return f"{prefix}{os.path.splitext(original_name)[0]}{ext}", date_source
    
    return f"{prefix}{date_str}{ext}", date_source

def organize_and_rename_photos():
    src_dir = Path('deduplicated_photos')
    dest_dir = Path('Photos')
    if not src_dir.exists():
        logger.error(f"Source directory {src_dir} does not exist!")
        return
    
    image_files = [f for f in src_dir.glob('*') 
                  if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    moved_count = 0
    for image_path in image_files:
        exif_data = get_exif_data(image_path)
        new_filename, _ = generate_filename(exif_data, image_path.name)
        prefix = get_prefix(image_path.name)
        # Clean up prefix for folder naming
        if prefix == 'SCAN_':
            if image_path.name.startswith('scandanavianinininini_'):
                group = 'Scandinavian Scans'
            else:
                group = 'Scans'
        elif prefix == 'SET_':
            group = 'Sets'
        elif prefix == 'PIC_':
            group = 'Pictures'
        else:
            group = prefix.rstrip('_')
        # Extract year from new filename (format: PREFIXYYYYMMDD_HHMMSS.ext)
        year = None
        try:
            year = int(new_filename[len(prefix):len(prefix)+4])
        except Exception:
            year = None
        if year and 1800 <= year <= 2100:
            decade = f"{year//10*10}s"
        else:
            decade = 'Unknown'
        target_folder = dest_dir / group / decade
        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / new_filename
        # Handle name collisions by appending a unique suffix
        if target_path.exists():
            stem = target_path.stem
            suffix = target_path.suffix
            i = 1
            while True:
                alt_target_path = target_folder / f"{stem}_{i}{suffix}"
                if not alt_target_path.exists():
                    target_path = alt_target_path
                    break
                i += 1
        try:
            image_path.rename(target_path)
            moved_count += 1
            logger.info(f"Moved {image_path.name} -> {target_path}")
        except Exception as e:
            logger.error(f"Failed to move {image_path.name}: {e}")
    # Final summary
    remaining = len([f for f in src_dir.glob('*') if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    print(f"\nMoved and renamed {moved_count} photos into organized folders under {dest_dir}/")
    print(f"{remaining} photos remain in {src_dir}/ (should be 0 if all moved)")

def fix_dates_in_photos():
    src_dir = Path('Photos')
    image_files = list(src_dir.rglob('*'))
    image_files = [f for f in image_files if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg']]
    fixed_count = 0
    for image_path in image_files:
        exif_data = get_exif_data(image_path)
        intended_date_str, _ = extract_date(exif_data, str(image_path))
        # Format: YYYYMMDD_HHMMSS
        try:
            dt = datetime.strptime(intended_date_str, '%Y%m%d_%H%M%S')
        except Exception:
            logger.warning(f"Could not parse intended date for {image_path.name}, skipping.")
            continue
        # Set mtime
        ts = mktime(dt.timetuple())
        try:
            os.utime(image_path, (ts, ts))
        except Exception as e:
            logger.error(f"Failed to set mtime for {image_path.name}: {e}")
        # Set EXIF DateTimeOriginal if missing or wrong
        try:
            exif_dict = piexif.load(str(image_path))
            exif_dt = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
            exif_dt_str = dt.strftime('%Y:%m:%d %H:%M:%S')
            needs_update = (
                not exif_dt or
                (isinstance(exif_dt, bytes) and exif_dt.decode(errors='ignore') != exif_dt_str)
            )
            if needs_update:
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = exif_dt_str.encode()
                exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = exif_dt_str.encode()
                exif_dict['0th'][piexif.ImageIFD.DateTime] = exif_dt_str.encode()
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, str(image_path))
                logger.info(f"Updated EXIF date for {image_path.name} -> {exif_dt_str}")
                fixed_count += 1
        except Exception as e:
            logger.error(f"Failed to update EXIF for {image_path.name}: {e}")
    print(f"\nFixed dates for {fixed_count} images in {src_dir}/ (EXIF and mtime)")

def main():
    input_dir = Path('Photos')
    if not input_dir.exists():
        logger.error(f"Directory {input_dir} does not exist!")
        return

    # Get all image files recursively
    image_files = [f for f in input_dir.rglob('*') 
                  if f.is_file() 
                  and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    # Analyze EXIF data availability
    print("\nEXIF Data Analysis:")
    print("-" * 80)
    analysis = analyze_exif_data(image_files)
    
    print("\nDate Quality:")
    print("-" * 40)
    for quality, (count, percentage) in analysis['date_quality'].items():
        print(f"{quality:<20} {count:>5} files ({percentage:>6})")
    
    print("\nDate Sources:")
    print("-" * 40)
    for source, (count, percentage) in analysis['date_sources'].items():
        print(f"{source:<30} {count:>5} files ({percentage:>6})")
    
    print("\nYear Distribution:")
    print("-" * 40)
    years = analysis['years']
    if years:
        print(f"Earliest Year: {min(years.keys())}")
        print(f"Latest Year: {max(years.keys())}")
        print("\nPhotos per decade:")
        for decade in range(min(years.keys()) // 10 * 10, (max(years.keys()) // 10 + 1) * 10, 10):
            decade_count = sum(count for year, count in years.items() 
                             if decade <= year < decade + 10)
            if decade_count > 0:
                print(f"{decade}s: {decade_count:>4} photos")
    
    print("\nAvailable EXIF Tags:")
    print("-" * 40)
    for tag, (count, percentage) in analysis['tags'].items():
        print(f"{tag:<30} {count:>5} files ({percentage:>6})")
    print("-" * 80)
    
    # Show proposed filename changes
    print("\nProposed filename changes:")
    print("-" * 100)
    print(f"{'Original Filename':<40} {'Proposed Filename':<40} {'Date Source':<20}")
    print("-" * 100)
    
    for image_path in sorted(image_files):
        exif_data = get_exif_data(image_path)
        new_name, date_source = generate_filename(exif_data, str(image_path))
        print(f"{image_path.name:<40} {new_name:<40} {date_source:<20}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EXIF preview and photo organizer')
    parser.add_argument('--organize', action='store_true', help='Organize and rename photos into Photos/<Group>/<Decade>/')
    parser.add_argument('--fix-dates', action='store_true', help='Fix EXIF and mtime dates for all images in Photos/')
    args = parser.parse_args()
    if args.organize:
        organize_and_rename_photos()
    elif args.fix_dates:
        fix_dates_in_photos()
    else:
        main() 