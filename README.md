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
- ⏳ Image-based deployment for photo inclusion

## Current Status

### Completed

- ✅ Image deduplication using perceptual hashing
- ✅ EXIF-based file organization
- ✅ Directory structure setup
- ✅ Metadata preservation
- ✅ Fly.io deployment with persistent storage
- ✅ Photoview configuration and basic setup
- ✅ User authentication and access control

### In Progress

- 🔄 Deployment image preparation
- 🔄 Timeline view testing
- 🔄 Sharing configuration testing

### Upcoming

- ⏳ Family member onboarding
- ⏳ Usage monitoring and optimization
- ⏳ Backup strategy implementation

## Project Structure

- `.cursor/` - Project context and constraints
  - `context.md` - Overall project context and rules
  - `constraints.json` - Technical constraints and phase boundaries
  - `phase-context/` - Phase-specific implementation details
- `deduplicated_photos/` - Processed photos ready for deployment
- `photos_to_process/` - Source photos
- `duplicate_photos/` - Identified duplicates
- Python scripts for processing
- Configuration files for deployment

## Development Workflow

This project uses a context-based development workflow to maintain focus and prevent scope creep. All development should:

1. Follow the current phase constraints in `.cursor/constraints.json`
2. Reference the appropriate phase context in `.cursor/phase-context/`
3. Maintain the project's core goals defined in `.cursor/context.md`
4. Document all changes according to the phase requirements

## Documentation

The project's implementation details and constraints are maintained in the `.cursor` directory:

- `.cursor/context.md` - Overall project context and rules
- `.cursor/constraints.json` - Technical constraints and phase boundaries
- `.cursor/phase-context/` - Phase-specific implementation details
  - `phase1.md` - Completed local preprocessing phase
  - `phase2.md` - Completed gallery setup phase
  - `phase3.md` - Current data migration phase

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
11. `Picture_004(rev 1).jpg` ↔ `Leonne_and_Chuck_004(rev 0).jpg`
12. `Picture_180(rev 1).jpg` ↔ `Leonne_and_Chuck_180(rev 0).jpg`
13. `Picture_224(rev 1).jpg` ↔ `Leonne_and_Chuck_224(rev 0).jpg`
14. `Picture_001(rev 0).jpg` ↔ `Leonne_and_Chuck_001(rev 0).jpg`

## Photoview Deployment

### Current Setup

- ✅ Deployed on Fly.io with persistent storage
- ✅ Basic authentication enabled
- ✅ Timeline view configured
- ✅ Metadata display enabled
- ✅ Auto-scanning configured (hourly)

### Access Information

- URL: https://rogers-photo-gallery.fly.dev
- Admin credentials are stored securely in Fly.io configuration
- Photos are stored in the persistent volume at `/data`

### Deployment Strategy

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

### Maintenance

- The application automatically scans for new photos hourly
- Storage automatically extends up to 5GB as needed
- Health checks ensure service availability
- Regular backups are maintained through the local photo collection

### Next Steps

1. Create deployment image with photos
2. Test sharing functionality with family members
3. Monitor usage and optimize performance
4. Document family member onboarding process

## Implementation Plan

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed implementation steps and progress tracking.
