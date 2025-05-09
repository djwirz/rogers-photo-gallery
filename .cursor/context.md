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
