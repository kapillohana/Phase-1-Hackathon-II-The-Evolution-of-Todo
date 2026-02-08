# Deployment Instructions

## Backend Deployment to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose "Docker" as the SDK
3. Connect your GitHub repository containing the backend code
4. Add the following secrets in the Space settings:
   - `DATABASE_URL`: Your database connection string (e.g., PostgreSQL)
   - `SECRET_KEY`: A random secret key for JWT tokens
5. The Space will automatically build and deploy using the provided Dockerfile

## Frontend Deployment to Vercel

1. Go to [Vercel](https://vercel.com) and create a new project
2. Import your GitHub repository containing the frontend code
3. During project setup, configure the following environment variable:
   - `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend (from Hugging Face Spaces)
4. Click "Deploy" and Vercel will automatically build and deploy your Next.js application

## Important Notes

- Make sure your backend is deployed first, so you have the URL to configure in the frontend
- The backend must be accessible via HTTPS for production use
- Both deployments will take a few minutes to complete initially
- After initial deployment, any updates to the GitHub repository will trigger automatic redeployment