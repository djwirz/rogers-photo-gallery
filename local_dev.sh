#!/bin/bash

echo "Starting Photoview local development..."

# Stop any running containers
docker-compose down

# Start the containers
docker-compose up --build -d

# Wait for Photoview to start
echo "Waiting for Photoview to start..."
sleep 10

# Check if Photoview is running
if curl -s http://localhost:8081/api/v1/health > /dev/null; then
    echo "✅ Photoview is running!"
    echo "Access the gallery at: http://localhost:8081"
    echo "Login with:"
    echo "Username: admin"
    echo "Password: changeme123"
else
    echo "❌ Photoview failed to start. Check the logs with: docker-compose logs"
fi 