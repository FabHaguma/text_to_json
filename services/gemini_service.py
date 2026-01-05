import json
from google import genai
from google.genai import types
from typing import Any, Dict
from config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.api_key
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    async def extract_structured_data(self, text_content: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("Gemini API Key is not configured.")

        if not self.client:
            self.client = genai.Client(api_key=self.api_key)
        
        prompt = self.build_prompt(text_content, target_schema)
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=target_schema
            )
        )

        return response.parsed if response.parsed else json.loads(response.text)

    def build_prompt(self, text_content: str, target_schema: Dict[str, Any]) -> str:
        return f"""
Role: 
You are an information extraction and normalization engine.

Task: 
I will provide you with raw text copied from a website. The text may be incomplete, inconsistently formatted, duplicated, or poorly structured.
Your task is to extract and normalize the content into a clean, structured format using the schema defined below.

Instructions:
- Analyze the provided text carefully. 
- Extract the information into the specific JSON fields defined below.
- Handle Missing Data: If a specific field is not mentioned in the text, return the value as null. Do not guess.
- Clean Content: Remove any HTML tags or tracking URLs from the text, but keep the formatting (like bullet points) within the description strings using standard newline characters.

Rules

- Do not invent or infer information that is not explicitly present in the text.
- If a field is missing, return it as null.
- Preserve original wording as much as possible; do not rewrite unless needed for clarity.
- Lists must be returned as arrays.
- Dates must be returned in ISO 8601 format (YYYY-MM-DD) when possible.
- Output valid JSON only. No commentary or explanations.

Text Content:
{text_content}

Target JSON Schema:
{json.dumps(target_schema, indent=2)}

Return the JSON ONLY.
"""

gemini_service = GeminiService()
