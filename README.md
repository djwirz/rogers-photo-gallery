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

- Local preprocessing for deduplication and organization
- Cloud hosting via Fly.io with persistent storage
- Photoview-based interface for easy family access
- Automated upload process for bulk photo handling

## Current Focus

- Setting up local development environment
- Implementing image deduplication using perceptual hashing
- Testing deduplication accuracy and performance
- Basic photo viewing interface

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
