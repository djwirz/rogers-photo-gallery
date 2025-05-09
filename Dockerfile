FROM photoview/photoview:latest

# Set environment variables
ENV PHOTOVIEW_ADMIN_USERNAME=admin
ENV PHOTOVIEW_ADMIN_PASSWORD=changeme123
ENV PHOTOVIEW_MEDIA_PATH=/data/photos
ENV PHOTOVIEW_INITIAL_SCAN=true

# Create necessary directories as root
USER root
RUN mkdir -p /data/photos /data/cache && \
  chown -R photoview:photoview /data

# Expose the Photoview port
EXPOSE 8080

# Switch to photoview user
USER photoview

# Start Photoview
CMD ["photoview"]
