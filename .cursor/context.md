# Rogers Photo Gallery - Cursor Context

## Project Overview

This is a family photo gallery project with specific implementation phases and constraints.

## Core Constraints

- Total photos: ~3,000 (~1GB)
- Must preserve EXIF/IPTC metadata
- Family-friendly interface required
- No proprietary lock-in
- Minimal maintenance
- Automated deduplication

## Implementation Phases

1. Local Preprocessing

   - Image deduplication
   - File organization
   - EXIF-based renaming

2. Gallery Setup

   - Fly.io deployment
   - Photoview configuration
   - User access setup

3. Data Migration
   - Bulk upload process
   - Metadata verification
   - Timeline view testing

## Context Rules

- All code must align with current phase
- No features outside implementation plan
- Maintain family-friendly focus
- Preserve existing metadata
- Follow deduplication results

## File Structure

- `deduplicated_photos/` - Processed photos
- `photos_to_process/` - Source photos
- `duplicate_photos/` - Identified duplicates
- Python scripts for processing
- Configuration files for deployment
