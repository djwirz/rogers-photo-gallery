# Project Constraints Context

## Project Scale

- Total Photos: 3000
- Storage Limit: 1GB
- File Types: .jpg, .jpeg, .png only

## Technical Requirements

- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred
- File System: Must be source of truth (Photoview principle)
- Media Access: Read-only access required

## Implementation Phases

Current Phase: 3
Allowed Features:

- Fly.io deployment
- Photoview setup
- Basic auth
- Simple sharing
- Read-only media access
- Volume-based persistence
- Image-based deployment with photos included

Blocked Features:

- Complex auth
- Custom UI
- Advanced features
- Proprietary formats
- Runtime file uploads
- Post-deployment file modifications
- SFTP or runtime file transfers

## Deployment Constraints

Platform: Fly.io
Application: Photoview
Requirements:

- Persistent storage
- Basic auth
- Simple sharing
- Read-only media access
- Volume-based persistence
- Image-based deployment

Storage Constraints:

- Initial size: 2GB
- Auto-extend threshold: 80%
- Auto-extend increment: 1GB
- Auto-extend limit: 5GB
- Max 1 volume per machine
- Hardware dependent
- Region bound

## Directory Structure

Required Directories:

- deduplicated_photos (for volume)
- photos_to_process
- duplicate_photos
- test_photos (for initial deployment)

## Photoview Principles

1. File System as Source of Truth

   - Directory structure defines organization
   - No runtime modifications
   - Read-only media access
   - Volume-based persistence
   - Image-based deployment

2. Original Files Never Modified

   - Read-only media access
   - Thumbnails in separate cache
   - No file modifications
   - No runtime uploads
   - Files included in deployment image

3. Automatic Scanning
   - Hourly directory scanning
   - Automatic thumbnail generation
   - No manual intervention
   - Volume-based persistence
   - Initial scan on deployment

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

## Usage

This file serves as a quick reference for project constraints.
For detailed constraints, see `.cursor/constraints.json`.
