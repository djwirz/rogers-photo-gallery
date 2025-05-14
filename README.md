# Rogers Photo Gallery

A simple photo gallery solution for sharing family photos with extended family.

## Goals

- ✅ Handle ~3,000 photos (~1GB total)
- ✅ Preserve and display existing EXIF/IPTC metadata
- ✅ Simple, family-friendly interface
- ✅ No proprietary lock-in or destructive transformations
- ✅ Minimal maintenance requirements
- ✅ Automated image deduplication to clean up scanned photos

## Technical Approach

- ✅ Local preprocessing for deduplication and organization
- ✅ Cloud hosting via Fly.io with persistent storage
- ✅ Photoview-based interface for easy family access
- ✅ Local development and testing
- ✅ Image-based deployment with photos included

## Current Status

### Completed

- ✅ Image deduplication using perceptual hashing
- ✅ EXIF-based file organization
- ✅ Directory structure setup
- ✅ Metadata preservation
- ✅ Fly.io deployment with persistent storage
- ✅ Photoview configuration and basic setup
- ✅ User authentication and access control
- ✅ Local development environment setup
- ✅ Directory structure testing
- ✅ Small batch verification
- ✅ Deployment strategy implementation

### In Progress

- 🔄 Full photo set migration
- 🔄 Family member onboarding
- 🔄 Usage monitoring and optimization
  - Set up Fly.io resource monitoring
  - Configure storage usage alerts
  - Track database growth
  - Monitor application performance
- 🔄 Backup strategy implementation

## Project Structure

### Core Directories

- `deduplicated_photos/` - Processed photos (not in version control)
- `photos_to_process/` - Source photos (not in version control)
- `duplicate_photos/` - Identified duplicates (not in version control)
- `test_photos/` - Test photo sets (not in version control)
- `Photos/` - Organized photos ready for deployment (not in version control)

### Development and Testing

- `local_test/` - Local testing environment (not in version control)
- `monitoring/` - Monitoring scripts and logs (not in version control)

### Configuration and Scripts

- Python scripts for processing
- Configuration files for deployment
- Shell scripts for development and testing

### Documentation

- `.cursor/` - Project context and constraints
  - `context.md` - Overall project context and rules
  - `constraints.json` - Technical constraints and phase boundaries
  - `phase-context/` - Phase-specific implementation details

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

## Important Notes

### Production vs Development

- Production uses `/data/photos` for all media files
- Development uses local directory mounts
- All photo processing must be done locally before deployment
- No runtime photo uploads in production

### Version Control

- No photo files are included in version control
- All photo directories are gitignored
- Only configuration and scripts are versioned
- Monitoring data and logs are excluded

### Deployment

- Uses Dockerfile with staging directory
- Photos copied from staging on first run
- Single volume mounted at `/data`
- SQLite database for simplicity

## Deduplication Results

The initial deduplication run processed 3,390 images and identified 14 pairs of duplicate photos. The duplicates were found between files with similar naming patterns, primarily between `Picture_XXX` and `Leonne_and_Chuck_XXX` series. This suggests these are likely the same photos with different naming conventions from different sources.

### Identified Duplicates

1. `Picture_093(rev 0).jpg` ↔ `Leonne_and_Chuck_093(rev 0).jpg`
2. `Picture_164(rev 0).jpg` ↔ `Leonne_and_Chuck_164(rev 0).jpg`
3. `Picture_955(rev 1).jpg` ↔ `Picture_952(rev 0).jpg`
4. `PD_0704(rev 1).jpg` ↔ `PD_0044-5(rev 0).jpg`
5. `Picture_691(rev 0).jpg` ↔ `Picture_951(rev 1).jpg`
6. `PD_0021-1(rev 1).jpg` ↔ `scandanavianinininini_166(rev 1).jpg`
7. `Picture_413(rev 0).jpg` ↔ `Leonne_and_Chuck_413(rev 0).jpg`
8. `scandanavianinininini_019-1(rev 0).jpg` ↔ `scandanavianinininini_019(rev 0).jpg`
9. `Picture_313(rev 0).jpg` ↔ `Leonne_and_Chuck_313(rev 0).jpg`
10. `Picture_110(rev 1).jpg` ↔ `Leonne_and_Chuck_110(rev 0).jpg`
