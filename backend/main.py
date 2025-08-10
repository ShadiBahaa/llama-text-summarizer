from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLaMA Text Summarizer API",
    description="A FastAPI backend for text summarization using LLaMA via Ollama",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "LLaMA Text Summarizer API is running!"}

@app.get("/health")
def health_check():
    """Check if the API and Ollama service are running"""
    try:
        # Test connection to Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "healthy", "ollama": "connected"}
        else:
            return {"status": "unhealthy", "ollama": "disconnected"}
    except requests.exceptions.RequestException:
        return {"status": "unhealthy", "ollama": "disconnected"}

@app.post("/summarize/")
def summarize(text: str = Form(...)):
    """Summarize the provided text using LLaMA model"""
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(text) < 50:
        raise HTTPException(status_code=400, detail="Text should be at least 50 characters long for meaningful summarization")
    
    try:
        logger.info(f"Attempting to summarize text of length: {len(text)}")
        
        # Prepare the prompt for better summarization
        prompt = f"""Please provide a concise summary of the following text. Focus on the main points and key information:

{text}

Summary:"""
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more focused summaries
                    "max_tokens": 500    # Limit response length
                }
            },
            timeout=60  # Set timeout to 60 seconds
        )
        
        if response.status_code != 200:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=502, detail="Error communicating with Ollama service")
        
        result = response.json()
        summary = result.get("response", "").strip()
        
        if not summary:
            raise HTTPException(status_code=500, detail="No summary generated")
        
        logger.info("Summary generated successfully")
        return {"summary": summary}
        
    except requests.exceptions.Timeout:
        logger.error("Timeout while waiting for Ollama response")
        raise HTTPException(status_code=504, detail="Request timeout - the model is taking too long to respond")
    
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama service")
        raise HTTPException(status_code=502, detail="Cannot connect to Ollama service. Make sure Ollama is running on localhost:11434")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)