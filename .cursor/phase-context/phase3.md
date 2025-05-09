# Phase 3: Data Migration

## Current Phase Status

Phase: 3 of 3
Status: In Progress
Priority: High

## Version Lock

CRITICAL: DO NOT MODIFY THESE VERSIONS

- Photoview: photoview/photoview:latest
- Database: mariadb:10.5
- Paths:
  - Photos: /photos (read-only)
  - Cache: /app/cache
  - Database: MariaDB standard path

Changes to these versions or paths are BLOCKED.
Focus is on photo verification ONLY.

## Implementation Checklist

### Phase 3A: Local Development (Current Focus)

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

### Phase 3B: Deployment Strategy (Next)

- [ ] 1. Volume Configuration

  - [ ] Set up 2GB initial volume
  - [ ] Configure auto-extend
  - [ ] Test persistence
  - [ ] Document settings
  - [ ] Verify database volume
  - [ ] Test database migration
  - [ ] Validate database recovery

- [ ] 2. Deployment Process

  - [ ] Create deployment checklist
  - [ ] Test small batch deployment
  - [ ] Verify persistence
  - [ ] Document process
  - [ ] Confirm database deployment
  - [ ] Test database scaling
  - [ ] Validate database monitoring

- [ ] 3. Monitoring & Backup
  - [ ] Set up health checks
  - [ ] Configure monitoring
  - [ ] Plan backup strategy
  - [ ] Document procedures
  - [ ] Implement database monitoring
  - [ ] Test database backups
  - [ ] Verify database recovery

### Phase 3C: Migration Process (Final)

- [ ] 1. Photo Organization

  - [ ] Verify deduplication
  - [ ] Check EXIF data
  - [ ] Organize by date
  - [ ] Document structure
  - [ ] Validate database organization
  - [ ] Test database queries
  - [ ] Confirm database performance

- [ ] 2. Full Migration
  - [ ] Deploy in batches
  - [ ] Verify each batch
  - [ ] Test all features
  - [ ] Document results
  - [ ] Monitor database growth
  - [ ] Test database optimization
  - [ ] Validate database integrity

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
- Local development environment needed
- Directory structure testing required
- Volume persistence confirmed
- Storage auto-extend configured (2GB initial, up to 5GB max)
- Database verification pending
- Schema validation needed
- Data integrity checks required

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

## Photoview Core Principles

1. File System as Source of Truth

   - Directory structure defines album organization
   - Photoview reflects filesystem structure
   - No runtime file modifications
   - Read-only access to media
   - Database maintains integrity
   - Schema enforces constraints
   - Data remains consistent

2. Original Files Never Modified
   - Media directory is read-only
   - Thumbnails stored in separate cache
   - No modifications to original files
   - No runtime file uploads
   - Database preserves history
   - Schema maintains relationships
   - Data remains immutable

## Image-Based Deployment Rules

1. Dockerfile Requirements

   - Base image: Official Photoview image
   - Essential environment variables only
   - Maintain volume mounts
   - Keep configuration simple
   - Ensure database connectivity
   - Verify schema creation
   - Monitor data integrity

2. Volume Usage

   - /data/photos: Read-only mount for media
   - /data/cache: Writable for thumbnails
   - /data/photoview.db: Database storage
   - Database volume: Persistent storage
   - Backup volume: Recovery storage
   - Log volume: Monitoring storage

3. Security Constraints
   - No runtime file modifications
   - Read-only media access
   - Secure volume mounts
   - Proper permission inheritance
   - Database access control
   - Schema protection
   - Data encryption
