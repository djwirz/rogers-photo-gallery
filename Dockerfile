FROM photoview/photoview:latest

# Switch to root to create directories
USER root

# Create staging directory for photos
RUN mkdir -p /app/photos-staging

# Copy organized photos into staging directory
COPY Photos/ /app/photos-staging/

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create data directory and set permissions
RUN mkdir -p /data && \
  chown -R photoview:photoview /data

# Set environment variables
ENV PHOTOVIEW_INITIAL_SCAN=true
ENV PHOTOVIEW_DATABASE_PATH=/data/photoview.db
ENV PHOTOVIEW_MEDIA_PATH=/data/photos
ENV PHOTOVIEW_CACHE_PATH=/app/cache

# Do not switch to photoview user here
# Set entrypoint to startup script
ENTRYPOINT ["/app/start.sh"] 