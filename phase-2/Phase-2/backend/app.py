from src.main import app

# This file is used by Hugging Face Spaces to run your application
# The variable 'app' should be the FastAPI instance you want to serve

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)