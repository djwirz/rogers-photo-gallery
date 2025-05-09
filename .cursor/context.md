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
- Local development first approach
- MUST use photoview/photoview:latest (DO NOT change version)
- Only one persistent volume may be mounted per Fly.io machine (see Fly.io docs and project constraints)
- Both the photo library and the Photoview database must reside on the same volume
- Use `/data/photos` for all media files and `/data/photoview.db` for the database

## Implementation Rules

- All version changes are BLOCKED
- All image tags must use :latest
- No custom Dockerfile modifications
- Follow official Photoview paths:
  - Photos: /photos (read-only)
  - Cache: /app/cache
  - Database: MariaDB 10.5
- Never modify these paths
- Never change versions
- Never solve cache permission issues with user mapping or complex permissions. If cache errors occur, delete and recreate the cache volume; cache is disposable.
- All deployment, configuration, and documentation must reflect the single-volume constraint
- Do NOT attempt to mount a second volume for `/photos` or any other path
- All scripts and configuration files must use `/data/photos` and `/data/photoview.db`

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
   - Local development and testing
   - Directory structure verification
   - Small batch deployment
   - Full photo set migration
   - Timeline view testing

## Context Rules

- All code must align with current phase
- No features outside implementation plan
- Maintain family-friendly focus
- Preserve existing metadata
- Follow deduplication results
- Test locally before deployment
- Document all changes
- Keep configuration simple
- Use default settings where possible

## File Structure

- `deduplicated_photos/` - Processed photos
- `photos_to_process/` - Source photos
- `duplicate_photos/` - Identified duplicates
- `test_photos/` - Test photo sets
- Python scripts for processing
- Configuration files for deployment

## Development Workflow

1. Local Development

   - Test with Docker locally
   - Verify directory structure
   - Test with small photo sets
   - Document all changes

2. Deployment Process

   - Verify local testing
   - Deploy in small batches
   - Test each deployment
   - Document results

3. Maintenance
   - Monitor performance
   - Track storage usage
   - Maintain backups
   - Update documentation

## Photoview Configuration

- Use default Photoview settings where possible
- Configure only essential environment variables
- Maintain read-only media access
- Let Photoview handle scanning automatically
- Keep configuration simple and minimal

## Important Note on Dev vs Production Storage

- The local dev environment mounts ./Photos to /photos, which is NOT available in production.
- In production (Fly.io), you must manually upload or create /data/photos on the persistent volume.
- The main production challenge is getting images into /data/photos, not gallery UI or database setup.
- Use dev only for UI/database validation, not for storage or upload workflows.
