#!/bin/bash

echo "Starting Photoview local development..."

# Stop any running containers
docker-compose down --remove-orphans

# Start the containers
docker-compose up --build -d

# Wait for Photoview to start
echo "Waiting for Photoview to start..."
max_attempts=12
attempt=1

while [ $attempt -le $max_attempts ]; do
    # Check container status
    container_status=$(docker-compose ps --format json photoview | jq -r '.[0].State')
    health_status=$(docker-compose ps --format json photoview | jq -r '.[0].Health')
    
    echo "Attempt $attempt/$max_attempts:"
    echo "Container status: $container_status"
    echo "Health status: $health_status"
    
    # Try to access the service
    if curl -s http://localhost:8081/api/graphql > /dev/null; then
        echo "✅ Photoview is running and accessible!"
        echo "Access the gallery at: http://localhost:8081"
        echo "Login with:"
        echo "Username: admin"
        echo "Password: changeme123"
        exit 0
    else
        echo "Service not yet accessible..."
    fi
    
    # Check container logs for errors
    if [ "$container_status" = "exited" ] || [ "$container_status" = "dead" ]; then
        echo "❌ Container has stopped. Last logs:"
        docker-compose logs --tail=20 photoview
        exit 1
    fi
    
    # If we've reached max attempts, show logs and exit
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ Max attempts reached. Container logs:"
        docker-compose logs photoview
        exit 1
    fi
    
    echo "Waiting 10 seconds before next attempt..."
    sleep 10
    attempt=$((attempt + 1))
done 