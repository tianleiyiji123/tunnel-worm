#!/bin/bash
set -e

echo "🚀 Starting SuiSuiChong..."

# Ensure data directory exists
mkdir -p /app/data /app/data/uploads

# Start services directly — setup wizard handles first-time config
echo "✅ Starting services..."

# Start Nginx and Uvicorn
nginx
cd /app/server
exec uvicorn main:app --host 0.0.0.0 --port 8000
