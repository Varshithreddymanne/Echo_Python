#!/bin/bash
cd backend

# Activate virtual environment if needed
# source .venv/bin/activate

# Ensure frontend build exists
if [ ! -d "../frontend/build" ]; then
  echo "Building frontend..."
  cd ../frontend
  npm install
  npm run build
  cd ../backend
fi

# Start FastAPI
cd app
exec uvicorn main:app --host 0.0.0.0 --port $PORT
