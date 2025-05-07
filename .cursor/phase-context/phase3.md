# Phase 3: Data Migration

## Current Status

- [x] Initial testing with small photo batch
- [x] Persistence verification (Single volume configured)
- [ ] Display quality validation
- [ ] Bulk upload implementation
- [ ] Metadata verification
- [ ] Timeline view testing

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Single volume mounted at /data with Photoview configured
- Auto-scanning enabled (hourly)

## Constraint Context

Reference: `.cursor/constraints.json`

Key Constraints:

- Project Scale: 3000 photos, 1GB storage
- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred
- File Types: .jpg, .jpeg, .png only
- Deployment: Fly.io with single volume (max 5GB)

## Photoview Principles

1. File System as Source of Truth

   - Directory structure defines album organization
   - Files must be organized in filesystem first
   - Photoview reflects filesystem structure

2. Original Files Never Modified

   - Media directory is read-only
   - Thumbnails stored in separate cache
   - No modifications to original files

3. Automatic Scanning
   - Hourly directory scanning
   - Automatic thumbnail generation
   - EXIF data extraction

## Testing Strategy

1. Small Batch Testing

   - Select 5-10 photos for initial testing
   - Verify EXIF data before upload
   - Place files in correct directory structure
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

1. Upload Process

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

- No data loss during upload
- Maintain upload logs
- Verify each batch
- Test with sample sets
- Document any issues
- Use Photoview's auto-scanning for file detection
- Place files in correct directory structure
- Never modify original files
- Use cache for thumbnails
- Maintain filesystem as source of truth
- If auto-scan fails, verify file permissions and directory structure
- If photos don't appear, check Photoview logs
- If metadata issues occur, verify EXIF data before copy

## Dependencies

- Phase 1 completion
- Phase 2 deployment
- Photoview configuration
- Storage setup complete

## Validation Steps

- Verify photos appear in timeline view within 1 hour of copy
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
2. Create appropriate directory structure in /data/photos
3. Copy files to correct location
4. Wait for auto-scan to complete
5. Verify persistence
6. Test display functionality
7. Document findings
8. Proceed with bulk upload implementation
9. Scale testing with larger batches
