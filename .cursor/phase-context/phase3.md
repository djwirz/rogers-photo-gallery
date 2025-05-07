# Phase 3: Data Migration

## Current Status

- [x] Initial testing with small photo batch
- [x] Persistence verification (Single volume configured)
- [ ] Display quality validation
- [ ] Deployment image preparation
- [ ] Metadata verification
- [ ] Timeline view testing

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Single volume mounted at /data with Photoview configured
- Auto-scanning enabled (hourly)

## Deployment Strategy

1. Image-Based Deployment

   - Photos included in deployment image
   - No runtime file uploads
   - Read-only access to media
   - Automatic scanning on startup

2. Volume Usage

   - /data/photos: Read-only mount for media
   - /data/cache: Writable for thumbnails
   - /data/photoview.db: Database storage

3. File System Principles
   - Filesystem as source of truth
   - No post-deployment modifications
   - Original files never modified
   - Automatic scanning only

## Constraint Context

Reference: `.cursor/constraints.json`

Key Constraints:

- Project Scale: 3000 photos, 1GB storage
- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred
- File Types: .jpg, .jpeg, .png only
- Deployment: Fly.io with single volume (max 5GB)
- File System: Must use filesystem as source of truth (Photoview principle)
- File Access: Must maintain read-only access to media files
- No Post-Deployment Uploads: Files must be included in deployment

## Photoview Principles

1. File System as Source of Truth

   - Directory structure defines album organization
   - Files must be organized in filesystem first
   - Photoview reflects filesystem structure
   - No post-deployment file modifications
   - Files must be included in deployment image

2. Original Files Never Modified

   - Media directory is read-only
   - Thumbnails stored in separate cache
   - No modifications to original files
   - No runtime file uploads needed

3. Automatic Scanning
   - Hourly directory scanning
   - Automatic thumbnail generation
   - EXIF data extraction
   - No manual intervention required

## Testing Strategy

1. Small Batch Testing

   - Select 5-10 photos for initial testing
   - Verify EXIF data before deployment
   - Include files in deployment image
   - Let auto-scanning process files
   - Validate display and metadata
   - Document any issues

2. Persistence Testing

   - Verify data persistence after service restart
   - Check metadata retention
   - Validate timeline view consistency
   - Test navigation persistence

3. Display Testing
   - Verify thumbnail generation
   - Test full-screen view
   - Check zoom functionality
   - Validate loading performance
   - Test different photo formats

## Technical Constraints

1. Deployment Process

   - Must comply with project scale (3000 photos)
   - Must preserve EXIF/IPTC metadata
   - Must use allowed file types (.jpg, .jpeg, .png)
   - Must maintain minimal complexity
   - Must use Photoview's auto-scanning feature
   - Must place files in /data/photos directory
   - Must maintain read-only access to media
   - Must use flat structure in /data/photos for initial test
   - Must maintain original filenames with dates (YYYY*MM_DD*\*)
   - Must verify file permissions (read-only)
   - Must include photos in deployment image
   - No runtime file uploads required
   - No post-deployment file modifications

2. Metadata Preservation

   - Must preserve EXIF/IPTC as required
   - Must verify date accuracy
   - Must validate image quality
   - Must confirm file integrity
   - Must maintain original file structure

3. Timeline View

   - Must maintain family-friendly interface
   - Must keep complexity minimal
   - Must validate navigation
   - Must ensure proper sorting
   - Must respect filesystem organization

4. Storage Constraints
   - Must use single Fly.io volume
   - Must respect 5GB maximum
   - Must handle hardware/region dependencies
   - Must use 1-day snapshot retention
   - Must maintain read-only media access

## Implementation Rules

- No data loss during deployment
- Maintain deployment logs
- Verify each deployment
- Test with sample sets
- Document any issues
- Use Photoview's auto-scanning for file detection
- Place files in correct directory structure
- Never modify original files
- Use cache for thumbnails
- Maintain filesystem as source of truth
- If auto-scan fails, verify file permissions and directory structure
- If photos don't appear, check Photoview logs
- If metadata issues occur, verify EXIF data before deployment

## Dependencies

- Phase 1 completion
- Phase 2 deployment
- Photoview configuration
- Storage setup complete

## Validation Steps

- Verify photos appear in timeline view within 1 hour of deployment
- Confirm EXIF dates match timeline sorting
- Check thumbnail generation in gallery view
- Verify original files remain unmodified
- Test basic navigation (next/previous, zoom)
- Verify filesystem organization
- Check thumbnail generation
- Validate read-only access

## Success Criteria

- All 5 test photos visible in gallery within 1 hour
- Timeline view shows correct chronological order
- EXIF data preserved and displayed
- Thumbnails generated correctly
- Original files unchanged

## Next Steps

1. Select and verify test photo batch
2. Create deployment image with photos
3. Deploy to Fly.io
4. Wait for auto-scan to complete
5. Verify persistence
6. Test display functionality
7. Document findings
8. Scale testing with larger batches
