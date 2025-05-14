# Phase 3: Data Migration

## Current Phase Status

Phase: 3 of 3
Status: In Progress
Priority: High
Current Focus: Production Volume Setup and Photo Migration
Blocked: No - Initial deployment working, investigating metadata preservation

## Version Lock

CRITICAL: DO NOT MODIFY THESE VERSIONS

- Photoview: photoview/photoview:latest
- Database: mariadb:10.5
- Paths:
  - Photos: /data/photos (read-only)
  - Cache: /app/cache
  - Database: SQLite at /data/photoview.db

Changes to these versions or paths are BLOCKED.
Focus is on photo verification ONLY.

## Implementation Checklist

### Phase 3A: Production Volume Setup (Current Focus)

- [x] 1. Volume Configuration

  - [x] Set up 2GB initial volume at `/data`
  - [x] Fix photo copy permissions in start.sh
  - [x] Remove sudo dependency
  - [x] Implement proper file copy mechanism
  - [x] Verify photo persistence
  - [x] Document volume setup process

- [ ] 2. Photo Migration

  - [x] Implement staging to volume copy
  - [ ] Verify photo integrity
  - [x] Test with sample photos
  - [x] Document migration process
  - [ ] Validate metadata preservation

- [ ] 3. Production Verification
  - [x] Verify volume persistence
  - [x] Test photo access
  - [ ] Validate metadata display
  - [x] Document verification process

### Phase 3B: Local Development (On Hold)

- [ ] 1. Local Docker Environment

  - [ ] Set up basic Docker environment
  - [ ] Configure Photoview container
  - [ ] Test with test_photos directory
  - [ ] Document setup process
  - [ ] Verify database initialization
  - [ ] Confirm database schema creation
  - [ ] Validate database connectivity
  - [ ] Test database persistence

- [ ] 2. Directory Structure Testing

  - [ ] Verify /data/photos mount
  - [ ] Test read-only permissions
  - [ ] Validate cache directory
  - [ ] Document structure
  - [ ] Confirm database table structure
  - [ ] Verify database indexes
  - [ ] Test database constraints

- [ ] 3. EXIF Data Validation
  - [ ] Test with 5 sample photos
  - [ ] Verify metadata display
  - [ ] Check timeline ordering
  - [ ] Document results
  - [ ] Validate database metadata storage
  - [ ] Confirm database query performance
  - [ ] Test database backup/restore

## Implementation Issues and Solutions

### Current Issues (2025-05-11)

1. **Photo Copy Permission Issues**

   - Problem: Photos not being copied from staging to `/data/photos`
   - Root Cause: Permission issues during copy operation
   - Attempted Solutions:
     1. Direct copy (Failed: Permission denied)
     2. chown after copy (Failed: Authentication failure)
   - Current Status: Blocked
   - Required Action: Implement proper sudo-based copy in start.sh

2. **Environment Variables**

   - Problem: Missing critical Photoview configuration
   - Root Cause: Environment variables removed from Dockerfile
   - Required Variables:
     ```
     PHOTOVIEW_INITIAL_SCAN=true
     PHOTOVIEW_DATABASE_PATH=/data/photoview.db
     PHOTOVIEW_MEDIA_PATH=/data/photos
     PHOTOVIEW_CACHE_PATH=/app/cache
     ```
   - Current Status: Blocked
   - Required Action: Restore environment variables in Dockerfile

3. **Volume Mount Implementation**
   - Problem: Photos not persisting in volume
   - Root Cause: Copy operation failing during container startup
   - Implementation History:
     1. Direct mount at `/data` (Failed: Volume mount issues)
     2. Staging approach (Failed: Copy operation issues)
   - Current Status: In Progress
   - Required Action: Fix copy operation and verify persistence

### Implementation Loops

1. **Permission Management Loop**

   - First Iteration: Direct copy failed
   - Second Iteration: Added chown after copy
   - Third Iteration: Authentication failure
   - Next Step: Implement sudo-based copy with proper error handling

2. **Configuration Management Loop**

   - First Iteration: Hardcoded in Dockerfile
   - Second Iteration: Removed from Dockerfile
   - Third Iteration: Missing critical variables
   - Next Step: Restore and document environment variables

3. **Volume Mount Loop**
   - First Iteration: Direct mount
   - Second Iteration: Staging approach
   - Third Iteration: Copy operation failing
   - Next Step: Fix copy operation and verify persistence

### Required Actions

1. Update `start.sh`:

   ```bash
   # Add sudo-based copy with error handling
   sudo cp -rv /app/photos-staging/* /data/photos/
   ```

2. Update Dockerfile:

   ```dockerfile
   # Restore environment variables
   ENV PHOTOVIEW_INITIAL_SCAN=true
   ENV PHOTOVIEW_DATABASE_PATH=/data/photoview.db
   ENV PHOTOVIEW_MEDIA_PATH=/data/photos
   ENV PHOTOVIEW_CACHE_PATH=/app/cache
   ```

3. Document all changes in this file and update constraints if needed.

### Issue Update (2025-05-12)

4. **Entrypoint Privilege Escalation Failure**
   - Problem: Deployments fail with `/app/start.sh: 17: sudo: not found` and `ERROR: Failed to copy photos`.
   - Root Cause: The official photoview image does not include `sudo`, and the container runs as the `photoview` user by default. The copy operation to `/data/photos` requires root privileges if the volume is mounted with restrictive permissions.
   - Attempted Solutions:
     1. Use `sudo` in `start.sh` (Failed: sudo not found)
     2. Run copy as photoview user (Failed: Permission denied)
   - Current Status: Blocked
   - Required Action: Remove `sudo` from `start.sh`, run the script as root, and only drop privileges to `photoview` when starting the Photoview process.

### Updated Required Actions

1. Update `start.sh`:
   - Remove all `sudo` commands.
   - Run the script as root.
   - At the end, use `exec su photoview -c /app/photoview` to start Photoview as the correct user.
2. Update Dockerfile:
   - Do not switch to `USER photoview` at the end. Let the container start as root so the script can copy files, then drop privileges in the script.
3. Document all changes in this file and update constraints if needed.

## Production Image Upload (Critical Difference from Dev)

- The local dev environment mounts ./Photos to /photos, which is NOT available in production.
- In production (Fly.io), you must manually upload or create /data/photos on the persistent volume.
- The main challenge in production is getting images into /data/photos, not gallery UI or database setup.
- The dev environment should only be used to validate UI and database logic, NOT storage or upload workflows.

### How to Upload Images to /data/photos on Fly.io

**Critical:** Do NOT upload zip files to production. The Fly.io instance does not include unzip or similar tools. You must extract all images locally before upload. Only extracted .jpg, .jpeg, and .png files are supported in /data/photos.

**Note:** The SFTP upload step (`flyctl ssh sftp shell`) is interactive and cannot be automated. Do not attempt to script or automate this step; it will hang. For automation, use `scp` or upload manually.

1. Prepare your photos locally. Ensure all images are extracted and organized.
2. Use SFTP to upload the extracted files directly to /data/photos:
   ```sh
   flyctl ssh sftp shell -a rogers-photo-gallery
   put -r Photos/* /data/photos
   exit
   ```
   (If you already uploaded a zip, download and extract it locally, then re-upload the files.)
3. Once images are uploaded, add `/data/photos` as the library path in the Photoview UI.
4. Photoview will scan and index your images from `/data/photos`.

**Note:** The dev environment's `/photos` path is not available in production. Always use `/data/photos` in production.

### Alternative: Seeding the Volume from the Image (Recommended for Initial Deploys)

If you want to avoid SFTP/manual upload for initial deployment or redeployment, you can include your photos in a staging directory in the image (e.g., /app/photos-staging). On app startup, use an entrypoint script to copy the contents of /app/photos-staging to /data/photos **if and only if /data/photos is empty**. This will seed the volume with your photos automatically.

**Example entrypoint logic:**

```sh
if [ -d /app/photos-staging ] && [ ! "$(ls -A /data/photos)" ]; then
  echo "Seeding /data/photos from /app/photos-staging..."
  cp -r /app/photos-staging/* /data/photos/
fi
```

- This approach is recommended for initial data seeding or redeployment.
- It will not overwrite existing photos in /data/photos.
- For ongoing uploads or user-contributed photos, use SFTP or another file transfer method as described above.

## Design Decisions

### Local Development First

- Local testing with Docker before deployment
- Small batch verification
- Directory structure testing
- Incremental deployment approach
- Database-first verification
- Schema validation
- Data integrity checks

### Photoview Configuration

- Use default Photoview settings where possible
- Configure only essential environment variables
- Maintain read-only media access
- Let Photoview handle scanning automatically
- Ensure database connectivity
- Verify database schema
- Monitor database health

## Current State

- 5 test photos prepared in test_photos/ with verified EXIF data
- Photos span 1956-1968 with clear date metadata
- Local development environment completed
- Directory structure verified
- Volume persistence confirmed
- Storage auto-extend configured (2GB initial, up to 5GB max)
- Database verification completed
- Schema validation completed
- Data integrity checks in progress
- Investigating metadata preservation in production

## Success Criteria

- Local development environment working
- Directory structure verified
- All photos visible in gallery
- Timeline view shows correct order
- EXIF data preserved and displayed
- Thumbnails generated correctly
- Original files unchanged
- Database properly initialized
- Schema correctly created
- Data integrity maintained
- Database performance verified
- Backup/restore tested

## Error Handling

- If local setup fails: Check Docker configuration
- If photos don't appear: Verify directory structure
- If metadata missing: Check EXIF data
- If scanner fails: Check Photoview logs
- If persistence issues: Verify volume configuration
- If database fails: Check connection and schema
- If data corrupts: Verify backup/restore
- If performance degrades: Monitor database metrics

### Database Connection Issues

1. Initial Connection Failure

   - Symptom: Photoview fails to connect to database with error "dial tcp 172.19.0.2:3306: connect: connection refused"
   - Cause: Photoview container starting before database is ready
   - Solution: Add service_healthy condition to depends_on in docker-compose.yml

   ```yaml
   depends_on:
     db:
       condition: service_healthy
   ```

   - Verification: Database container shows as "Healthy" before Photoview starts

2. Connection String Format

   - Symptom: Database connection timeout despite healthy database
   - Cause: Incorrect connection string format in PHOTOVIEW_MYSQL_URL
   - Solution: Include port number in connection string

   ```yaml
   PHOTOVIEW_MYSQL_URL=photoview:photoview@tcp(db:3306)/photoview
   ```

   - Verification: Photoview logs show successful database initialization

3. Initial Scan Not Starting
   - Symptom: Database connected but no photos appearing in gallery
   - Cause: Initial scan disabled by default
   - Solution: Enable initial scan with environment variable
   ```yaml
   PHOTOVIEW_INITIAL_SCAN=true
   ```
   - Verification: Check media table for photo entries after container restart

### Cache Directory Issues

1. Permission Denied Errors

   - Symptom: "could not make album image cache directory: mkdir /app/cache/X: permission denied"
   - Cause: Cache volume permissions not properly configured
   - Solution: Use standard Docker volume without custom permissions

   ```yaml
   volumes:
     - photoview_cache:/app/cache
   ```

   - Verification: Photoview can create cache directories and store thumbnails

2. Cache Directory Configuration

   - Path must remain as `/app/cache` per version lock
   - Use standard Docker volume management
   - No custom permissions needed
   - Let Photoview handle cache directory creation

3. Cache Reset Procedure (IMPORTANT)
   - If cache permission errors occur:
     1. Stop all containers: `docker-compose down`
     2. Remove the cache volume: `docker volume rm rogers-photo-gallery_photoview_cache`
     3. Restart containers: `docker-compose up -d`

## Investigation: Missing Images in Gallery (2025-05-11)

- **Observed Issue:** Albums are created in Photoview, but all albums are empty and the timeline shows only placeholders. No images are visible in the gallery UI.
- **What is NOT the issue:**
  - The files are present in `/data/photos` with correct names and structure.
  - EXIF/timeline metadata was previously validated in dev and is assumed intact.
  - The problem is NOT due to EXIF loss during transfer.
- **Current Focus:**
  - Investigating Photoview's import/scan process and configuration.
  - Checking for errors in Photoview logs related to scanning, EXIF parsing, or album creation.
  - Verifying that the media path is set correctly and that a scan is triggered in the UI.
  - Querying the database to confirm albums exist but are empty.
- **Next Steps:**
  1. Review Photoview logs for scan/import errors.
  2. Confirm library path and trigger scan in UI if needed.
  3. Document findings and update troubleshooting steps.

## Log Monitoring Workflow

See the global log monitoring workflow in `.cursor/constraints.json` under the `log_monitoring_workflow` key for all Fly.io log review and troubleshooting procedures. The workflow now uses the `--no-tail` flag for reliable, non-streaming log review. Previous approaches without `--no-tail` may hang or fail to show current logs. This supersedes any previous phase-specific instructions.

## Next Steps

1. Verify metadata preservation during deployment
2. Complete remaining production verification tasks
3. Begin full photo set migration
4. Implement monitoring and backup strategy
