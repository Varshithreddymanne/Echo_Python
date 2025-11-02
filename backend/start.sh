#!/bin/bash
set -e

# Ensure frontend build exists
if [ ! -d "../frontend/build" ]; then
  echo "Building frontend..."
  cd ../frontend
  npm install
  npm run build
  cd ../backend
fi

# Start FastAPI
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT
