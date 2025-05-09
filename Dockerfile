FROM photoview/photoview:latest

# The official image uses /app/photoview as the entrypoint
WORKDIR /app

# Ensure data directory exists and has correct permissions
RUN mkdir -p /data && chown -R photoview:photoview /data 