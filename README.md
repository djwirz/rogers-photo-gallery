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

## Implementation Plan

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed implementation steps and progress tracking.
