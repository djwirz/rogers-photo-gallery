FROM photoview/photoview:latest

# The official image uses /app/photoview as the entrypoint
WORKDIR /app

# Switch to root to create directories
USER root

# Ensure data directory exists and has correct permissions
RUN mkdir -p /data && chown -R photoview:photoview /data

# Switch back to photoview user
USER photoview 