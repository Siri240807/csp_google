@echo off
REM Deployment script for Cloud Run on Windows

REM Set your Google Cloud project ID
set PROJECT_ID=your-google-cloud-project-id

REM Set the service name
set SERVICE_NAME=ai-customer-support-agent

REM Build the Docker image
echo Building Docker image...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/%SERVICE_NAME%

REM Deploy to Cloud Run
echo Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME% ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars GEMINI_API_KEY=%GEMINI_API_KEY%

echo Deployment completed!
echo Your service is available at: https://%SERVICE_NAME%-^<region^>-^<project-id^>.a.run.app