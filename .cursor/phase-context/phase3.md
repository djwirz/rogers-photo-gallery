# Phase 3: Data Migration

## Current Phase Status

Phase: 3 of 3
Status: In Progress
Priority: High

## Implementation Checklist

### Phase 3A: Local Development (Current Focus)

- [ ] 1. Local Docker Environment

  - [ ] Set up Docker environment
  - [ ] Configure Photoview container
  - [ ] Test with test_photos directory
  - [ ] Document setup process

- [ ] 2. Directory Structure Testing

  - [ ] Verify /data/photos mount
  - [ ] Test read-only permissions
  - [ ] Validate cache directory
  - [ ] Document structure

- [ ] 3. EXIF Data Validation
  - [ ] Test with 5 sample photos
  - [ ] Verify metadata display
  - [ ] Check timeline ordering
  - [ ] Document results

### Phase 3B: Deployment Strategy (Next)

- [ ] 1. Volume Configuration

  - [ ] Set up 2GB initial volume
  - [ ] Configure auto-extend
  - [ ] Test persistence
  - [ ] Document settings

- [ ] 2. Deployment Process

  - [ ] Create deployment checklist
  - [ ] Test small batch deployment
  - [ ] Verify persistence
  - [ ] Document process

- [ ] 3. Monitoring & Backup
  - [ ] Set up health checks
  - [ ] Configure monitoring
  - [ ] Plan backup strategy
  - [ ] Document procedures

### Phase 3C: Migration Process (Final)

- [ ] 1. Photo Organization

  - [ ] Verify deduplication
  - [ ] Check EXIF data
  - [ ] Organize by date
  - [ ] Document structure

- [ ] 2. Full Migration
  - [ ] Deploy in batches
  - [ ] Verify each batch
  - [ ] Test all features
  - [ ] Document results

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

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Local development environment needed
- Directory structure testing required
- Volume persistence confirmed
- Storage auto-extend configured (2GB initial, up to 5GB max)

## Success Criteria

- Local development environment working
- Directory structure verified
- All photos visible in gallery
- Timeline view shows correct order
- EXIF data preserved and displayed
- Thumbnails generated correctly
- Original files unchanged

## Error Handling

- If local setup fails: Check Docker configuration
- If photos don't appear: Verify directory structure
- If metadata missing: Check EXIF data
- If scanner fails: Check Photoview logs
- If persistence issues: Verify volume configuration

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
