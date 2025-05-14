#!/bin/sh

echo "Starting photo gallery initialization..."

# Create required directories
mkdir -p /data/photos
echo "Created required directories"

# Debug: List contents of staging directory
echo "Contents of /app/photos-staging:"
ls -la /app/photos-staging

# If photos directory is empty, copy from staging
if [ ! "$(ls -A /data/photos)" ]; then
  echo "Seeding /data/photos from /app/photos-staging..."
  cp -rv /app/photos-staging/* /data/photos/
  chown -R photoview:photoview /data/photos
  echo "Copy complete. Contents of /data/photos:"
  ls -la /data/photos
else
  echo "/data/photos is not empty, skipping copy"
fi

# Ensure cache directory is writable
mkdir -p /app/cache
chown -R photoview:photoview /app/cache

echo "Starting Photoview as photoview user..."
exec su photoview -c /app/photoview 