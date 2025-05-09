# Phase 3: Data Migration

## Design Decisions

### Local Development First

- Local testing with Docker before deployment
- Small batch verification
- Directory structure testing
- Incremental deployment approach

### Auto-Scanning Disabled

- Auto-scanning is intentionally disabled (PHOTOVIEW_SCAN_INTERVAL = "0")
- Only initial scan on deployment is performed (PHOTOVIEW_INITIAL_SCAN = "true")
- This is a deliberate choice because:
  1. Photos are static and included in deployment image
  2. No runtime file uploads or modifications
  3. Reduces unnecessary system load
  4. Matches the read-only, static nature of the gallery
- DO NOT re-enable auto-scanning as it's unnecessary overhead

## Current Status

### Phase 3A: Local Development

- [ ] Local Docker environment setup
- [ ] Directory structure testing
- [ ] Small batch verification
- [ ] EXIF data validation

### Phase 3B: Deployment Strategy

- [ ] Volume configuration
- [ ] Deployment process
- [ ] Monitoring setup
- [ ] Backup strategy

### Phase 3C: Migration Process

- [ ] Photo organization
- [ ] Deployment verification
- [ ] Full migration
- [ ] Final testing

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Local development environment needed
- Directory structure testing required
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
- Local development first approach

## Implementation Rules

1. Local Development

   - Set up Docker environment
   - Test directory structure
   - Verify EXIF data
   - Document all changes

2. Volume Management

   - Use single volume mounted at /data
   - Mount photos directory read-only
   - Let Photoview handle caching
   - No post-deployment file modifications

3. File Organization

   - Place files in /data/photos
   - Maintain original filenames
   - Preserve EXIF data
   - Test with small batches

4. Deployment Process
   - Test locally first
   - Deploy in small batches
   - Verify each deployment
   - Document all changes

## Testing Strategy

1. Local Testing

   - Set up Docker environment
   - Test directory structure
   - Verify EXIF data
   - Test with small batches

2. Deployment Testing

   - Test volume configuration
   - Verify persistence
   - Check metadata
   - Validate display

3. Final Testing
   - Test full photo set
   - Verify all features
   - Check performance
   - Document results

## Success Criteria

- Local development environment working
- Directory structure verified
- All photos visible in gallery
- Timeline view shows correct order
- EXIF data preserved and displayed
- Thumbnails generated correctly
- Original files unchanged

## Next Steps

1. Set up local development environment
2. Test directory structure
3. Verify EXIF data
4. Test with small batches
5. Document findings

## Error Handling

- If local setup fails: Check Docker configuration
- If photos don't appear: Verify directory structure
- If metadata missing: Check EXIF data
- If scanner fails: Check Photoview logs
- If persistence issues: Verify volume configuration

## Development Workflow

1. Local Development

   - Set up Docker environment
   - Test directory structure
   - Verify EXIF data
   - Document changes

2. Deployment

   - Test with small batches
   - Verify persistence
   - Check metadata
   - Document results

3. Maintenance
   - Monitor performance
   - Track storage usage
   - Maintain backups
   - Update documentation

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
