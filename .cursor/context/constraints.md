# Project Constraints Context

## Project Scale

- Total Photos: 3000
- Storage Limit: 1GB
- File Types: .jpg, .jpeg, .png only

## Technical Requirements

- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred

## Implementation Phases

Current Phase: 2
Allowed Features:

- Fly.io deployment
- Photoview setup
- Basic auth
- Simple sharing

Blocked Features:

- Complex auth
- Custom UI
- Advanced features
- Proprietary formats

## Deployment Constraints

Platform: Fly.io
Application: Photoview
Requirements:

- Persistent storage
- Basic auth
- Simple sharing

Storage Constraints:

- Max 1 volume per machine
- Max size: 500GB
- Min size: 1GB
- Snapshot retention: 5 days
- Hardware dependent
- Region bound

## Directory Structure

Required Directories:

- deduplicated_photos
- photos_to_process
- duplicate_photos

## Usage

This file serves as a quick reference for project constraints.
For detailed constraints, see `.cursor/constraints.json`.
