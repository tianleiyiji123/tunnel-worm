#!/bin/bash
set -e

echo "🚀 Starting SuiSuiChong..."

# Ensure data directory exists
mkdir -p /app/data /app/data/uploads

# Start Uvicorn directly (no Nginx)
echo "✅ Starting Uvicorn on port 7895..."
cd /app/server
exec uvicorn main:app --host 0.0.0.0 --port 7895 --timeout-keep-alive 120
