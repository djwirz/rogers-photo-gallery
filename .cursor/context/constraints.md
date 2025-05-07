# Project Constraints Context

## Project Scale

- Total Photos: 3000
- Storage Limit: 1GB
- File Types: .jpg, .jpeg, .png only

## Technical Requirements

- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred
- Deployment: Image-based with photos included
- File System: Must be source of truth (Photoview principle)

## Implementation Phases

Current Phase: 3
Allowed Features:

- Fly.io deployment
- Photoview setup
- Basic auth
- Simple sharing
- Image-based deployment
- Read-only media access

Blocked Features:

- Complex auth
- Custom UI
- Advanced features
- Proprietary formats
- Runtime file uploads
- Post-deployment file modifications

## Deployment Constraints

Platform: Fly.io
Application: Photoview
Requirements:

- Persistent storage
- Basic auth
- Simple sharing
- Image-based deployment
- Read-only media access

Storage Constraints:

- Max 1 volume per machine
- Max size: 500GB
- Min size: 1GB
- Snapshot retention: 5 days
- Hardware dependent
- Region bound

## Directory Structure

Required Directories:

- deduplicated_photos (for deployment)
- photos_to_process
- duplicate_photos

## Photoview Principles

1. File System as Source of Truth

   - Directory structure defines organization
   - No runtime modifications
   - Files included in deployment

2. Original Files Never Modified

   - Read-only media access
   - Thumbnails in separate cache
   - No file modifications

3. Automatic Scanning
   - Hourly directory scanning
   - Automatic thumbnail generation
   - No manual intervention

## Usage

This file serves as a quick reference for project constraints.
For detailed constraints, see `.cursor/constraints.json`.
