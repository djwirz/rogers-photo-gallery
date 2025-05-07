# Phase 3: Data Migration

## Current Status

- [ ] Initial testing with small photo batch
- [ ] Persistence verification
- [ ] Display quality validation
- [ ] Bulk upload implementation
- [ ] Metadata verification
- [ ] Timeline view testing

## Constraint Context

Reference: `.cursor/constraints.json`

Key Constraints:

- Project Scale: 3000 photos, 1GB storage
- Metadata: Must preserve EXIF/IPTC
- Interface: Family-friendly, minimal complexity
- Maintenance: Minimal, automation preferred
- File Types: .jpg, .jpeg, .png only
- Deployment: Fly.io with single volume (max 500GB)

## Testing Strategy

1. Small Batch Testing

   - Select 5-10 photos for initial testing
   - Verify EXIF data before upload
   - Test upload process
   - Validate display and metadata
   - Document any issues

2. Persistence Testing

   - Verify data persistence after service restart
   - Check metadata retention
   - Validate timeline view consistency
   - Test navigation persistence

3. Display Testing
   - Verify thumbnail generation
   - Test full-screen view
   - Check zoom functionality
   - Validate loading performance
   - Test different photo formats

## Technical Constraints

1. Upload Process

   - Must comply with project scale (3000 photos)
   - Must preserve EXIF/IPTC metadata
   - Must use allowed file types (.jpg, .jpeg, .png)
   - Must maintain minimal complexity

2. Metadata Preservation

   - Must preserve EXIF/IPTC as required
   - Must verify date accuracy
   - Must validate image quality
   - Must confirm file integrity

3. Timeline View

   - Must maintain family-friendly interface
   - Must keep complexity minimal
   - Must validate navigation
   - Must ensure proper sorting

4. Storage Constraints
   - Must use single Fly.io volume
   - Must respect 500GB maximum
   - Must handle hardware/region dependencies
   - Must use 5-day snapshot retention

## Implementation Rules

- No data loss during upload
- Maintain upload logs
- Verify each batch
- Test with sample sets
- Document any issues

## Dependencies

- Phase 1 completion
- Phase 2 deployment
- Photoview configuration
- Storage setup complete

## Validation Steps

- Check deduplication results
- Verify gallery functionality
- Test sharing features
- Validate timeline view
- Confirm metadata display

## Next Steps

1. Select and verify test photo batch
2. Run initial upload test
3. Verify persistence
4. Test display functionality
5. Document findings
6. Proceed with bulk upload implementation
7. Scale testing with larger batches
