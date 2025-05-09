#!/bin/bash

echo "Verifying Photoview scanning process..."

# Function to check database state
check_db_state() {
    echo "Checking database state..."
    docker-compose exec db mysql -u photoview -pphotoview photoview -e "
        SELECT COUNT(*) as media_count FROM media;
        SELECT COUNT(*) as exif_count FROM media_exif;
        SELECT COUNT(*) as url_count FROM media_urls;
    " | cat
}

# Function to check scan status
check_scan_status() {
    echo "Checking scan status..."
    docker-compose logs --tail=50 photoview | grep -i "scan" | cat
}

# Initial state
echo "Initial database state:"
check_db_state

# Trigger scan through API
echo "Triggering scan..."
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"changeme123"}' \
     http://localhost:8081/api/auth/login

# Wait for scan to start
echo "Waiting for scan to start..."
sleep 5

# Monitor scan progress
echo "Monitoring scan progress..."
for i in {1..12}; do
    echo "Check $i of 12:"
    check_scan_status
    check_db_state
    sleep 10
done

# Final state
echo "Final database state:"
check_db_state 