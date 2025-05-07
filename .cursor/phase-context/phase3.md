# Phase 3: Data Migration

## Current Status

- [x] Initial testing with small photo batch
- [x] Persistence verification (Single volume configured)
- [x] Volume configuration (2GB initial, auto-extend enabled)
- [x] Read-only media access configured
- [x] Auto-scanning enabled (hourly)
- [ ] Display quality validation
- [ ] Metadata verification
- [ ] Timeline view testing
- [ ] Full photo set migration
- [ ] Storage usage monitoring

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Single volume mounted at /data with Photoview configured
- Auto-scanning enabled (hourly)
- Read-only permissions verified
- Volume persistence confirmed
- Storage auto-extend configured (2GB initial, up to 5GB max)

## Constraint Context

Reference: `.cursor/context/constraints.md`

Key Constraints:

- Project Scale: 3000 photos, 1GB storage
- File Types: .jpg, .jpeg, .png only
- Media Access: Read-only required
- Volume-based persistence
- No runtime file uploads
- No post-deployment modifications
- Storage: 2GB initial, auto-extends to 5GB max

## Photoview Core Principles

1. File System as Source of Truth

   - Directory structure defines album organization
   - Photoview reflects filesystem structure
   - No runtime file modifications
   - Read-only access to media

2. Original Files Never Modified

   - Media directory is read-only
   - Thumbnails stored in separate cache
   - No modifications to original files
   - No runtime file uploads

3. Automatic Scanning
   - Hourly directory scanning
   - Automatic thumbnail generation
   - EXIF data extraction
   - No manual intervention required

## Implementation Rules

1. Volume Management

   - Use single volume mounted at /data
   - Mount photos directory read-only
   - Let Photoview handle caching
   - No post-deployment file modifications

2. File Organization

   - Place files in /data/photos
   - Maintain original filenames
   - Preserve EXIF data
   - Use flat structure for initial test

3. Deployment Process
   - Use image-based deployment with photos included
   - Create custom Dockerfile based on official Photoview image
   - Copy photos during image build
   - Ensure read-only permissions
   - Let auto-scanner handle indexing
   - No runtime file uploads

## Testing Strategy

1. Small Batch Testing

   - Use 5 test photos
   - Verify EXIF data
   - Include in deployment image
   - Let auto-scanner process
   - Validate display and metadata

2. Persistence Testing

   - Verify data persistence after restart
   - Check metadata retention
   - Validate timeline view
   - Test navigation

3. Display Testing
   - Verify thumbnail generation
   - Test full-screen view
   - Check zoom functionality
   - Validate loading performance

## Success Criteria

- All 5 test photos visible in gallery
- Timeline view shows correct order
- EXIF data preserved and displayed
- Thumbnails generated correctly
- Original files unchanged

## Next Steps

1. Create custom Dockerfile
2. Include test photos in image
3. Update fly.toml configuration
4. Deploy and verify auto-scan
5. Test display functionality
6. Document findings

## Error Handling

- If photos don't appear: Check image build and permissions
- If metadata missing: Verify EXIF data before image build
- If scanner fails: Check Photoview logs
- If persistence issues: Verify volume configuration

## Image-Based Deployment Rules

1. Dockerfile Requirements

   - Base image: Official Photoview image
   - Copy photos during build
   - Set correct permissions
   - Maintain volume mounts

2. Volume Usage

   - /data/photos: Read-only mount for media
   - /data/cache: Writable for thumbnails
   - /data/photoview.db: Database storage

3. Security Constraints
   - No runtime file modifications
   - Read-only media access
   - Secure volume mounts
   - Proper permission inheritance
