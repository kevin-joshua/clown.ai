from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import base64
import traceback
from llm import generate_response  # your function

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for your client domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_PATH = "output.png"

# Request model to parse JSON body
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: PromptRequest):
    """
    Generate response text and image based on prompt.
    """
    try:
        # Call your custom LLM/image generator function
        result = generate_response(request.prompt)

        if not isinstance(result, dict) or "response" not in result:
            return JSONResponse(status_code=500, content={"error": "generate_response() did not return expected data."}) 
        
        response_data = {
            "response": result["response"],
            "followup": result["followup"]  # Optional follow-up question
        }

        # Check if image exists and was generated
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                response_data["image"] = encoded_image  # Add image only if present

        return JSONResponse(response_data)

    except Exception as e:
        
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
