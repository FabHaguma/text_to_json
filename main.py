import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict

from config import settings
from services.gemini_service import gemini_service

app = FastAPI(
    title="Universal Text-to-JSON API",
    description="An API to extract structured JSON data from raw text using Google Gemini."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExtractionRequest(BaseModel):
    text_content: str = Field(..., description="The raw text to extract data from.")
    target_schema: Dict[str, Any] = Field(..., description="A JSON object representing the target schema with example values.")

@app.post("/api/extract", response_model=Dict[str, Any])
async def extract_data(request: ExtractionRequest):
    """
    Extracts structured data from raw text based on a provided JSON schema.
    """
    try:
        return await gemini_service.extract_structured_data(
            request.text_content, 
            request.target_schema
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during extraction: {str(e)}")

@app.post("/api/prompt", response_model=Dict[str, str])
async def get_prompt(request: ExtractionRequest):
    """
    Returns the prompt that would be sent to the LLM.
    """
    prompt = gemini_service.build_prompt(request.text_content, request.target_schema)
    return {"prompt": prompt}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "api_key_configured": bool(settings.api_key)
    }

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
