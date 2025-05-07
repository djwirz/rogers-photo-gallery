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
- 🔄 Cloud hosting via Fly.io with persistent storage
- 🔄 Photoview-based interface for easy family access
- ⏳ Automated upload process for bulk photo handling

## Current Status

### Completed

- ✅ Image deduplication using perceptual hashing
- ✅ EXIF-based file organization
- ✅ Directory structure setup
- ✅ Metadata preservation

### In Progress

- 🔄 Fly.io deployment
- 🔄 Photoview configuration
- 🔄 Basic user access setup

### Upcoming

- ⏳ Bulk upload implementation
- ⏳ Timeline view testing
- ⏳ Final validation

## Project Structure

- `.cursor/` - Project context and constraints
  - `context.md` - Overall project context and rules
  - `constraints.json` - Technical constraints and phase boundaries
  - `phase-context/` - Phase-specific implementation details
- `deduplicated_photos/` - Processed photos ready for upload
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
  - `phase2.md` - Current gallery setup phase
  - `phase3.md` - Upcoming data migration phase

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

## Implementation Plan

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed implementation steps and progress tracking.

## Photoview Deployment

### Prerequisites

- Fly.io CLI installed (`flyctl`)
- Fly.io account set up
- Photos organized in the `deduplicated_photos` directory

### Deployment Steps

1. Login to Fly.io:

   ```bash
   flyctl auth login
   ```

2. Create volumes for persistent storage (create two volumes in different regions for redundancy):

   ```bash
   # Create primary volume in SJC (Silicon Valley)
   flyctl volumes create photoview_data_1 --size 1 --region sjc

   # Create backup volume in LAX (Los Angeles)
   flyctl volumes create photoview_data_2 --size 1 --region lax
   ```

   Note: The volume size is set to 1GB to accommodate the current photo collection (694MB) with room for future additions. We create two volumes for redundancy to avoid downtime.

3. Deploy the application:

   ```bash
   flyctl deploy
   ```

4. Configure Photoview:
   - Access the web interface at your Fly.io URL
   - Set up initial admin user
   - Configure photo library path to `/data/photos`
   - Enable timeline view and metadata display

### Access and Sharing

- The application will be available at `https://rogers-photo-gallery.fly.dev`
- Share access through the Photoview interface
- Use simple sharing links for family members
