# Implementation Plan

## Phase 1: Local Preprocessing

### 1.1 Image Deduplication

- [x] Set up and test deduplication script
- [x] Process photos and verify results
- [x] Organize output into clean/archive directories

### 1.2 File Organization

- [x] Implement EXIF-based renaming
- [x] Set up directory structure for upload

## Phase 2: Gallery Setup

### 2.1 Fly.io Setup

- [ ] Deploy Photoview instance
- [ ] Configure storage and networking

### 2.2 Gallery Configuration

- [ ] Set up user access
- [ ] Configure sharing options
- [ ] Test basic functionality

## Phase 3: Data Migration

### 3.1 Upload Process

- [ ] Implement bulk upload
- [ ] Verify metadata preservation
- [ ] Test timeline view

### 3.2 Final Validation

- [ ] Check deduplication results
- [ ] Verify gallery functionality
- [ ] Test sharing features

## Notes

- Each phase can be worked on independently
- Testing should be performed at each step
- EXIF date extraction now handles:
  - Historical photos (1800s-1970s)
  - Scan dates (skipping 2009)
  - Multiple date sources (EXIF, filename patterns, file metadata)
  - Appropriate fallback dates for different photo sets
