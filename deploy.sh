#!/bin/bash

# Deployment script for Cloud Run

# Set your Google Cloud project ID
PROJECT_ID="your-google-cloud-project-id"

# Set the service name
SERVICE_NAME="ai-customer-support-agent"

# Build the Docker image
echo "Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY

echo "Deployment completed!"
echo "Your service is available at: https://$SERVICE_NAME-<region>-<project-id>.a.run.app"