from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import json
import re
import logging
from config import settings
from gemini_client import get_gemini_service, GeminiService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request and response
class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500, description="The topic to explain")
    complexity_level: Optional[str] = Field("intermediate", description="Complexity level: beginner, intermediate, or advanced")
    include_examples: Optional[bool] = Field(True, description="Whether to include practical examples")

class TestCase(BaseModel):
    input: str = Field(..., description="Test input")
    expected_output: str = Field(..., description="Expected output")
    description: str = Field(..., description="Test case description")

class ExplanationResponse(BaseModel):
    topic: str = Field(..., description="The original topic")
    explanation: str = Field(..., description="Detailed explanation from GPT")
    test_case: TestCase = Field(..., description="Test case to validate the explanation")
    complexity_level: str = Field(..., description="Complexity level used")
    metadata: dict = Field(..., description="Additional metadata about the response")

def construct_detailed_prompt(topic: str, complexity_level: str, include_examples: bool) -> str:
    """Construct a detailed prompt for the GPT model"""
    
    complexity_instructions = {
        "beginner": "Explain in simple terms that a beginner can understand. Use basic vocabulary and avoid jargon.",
        "intermediate": "Provide a balanced explanation with some technical details. Assume basic familiarity with the subject.",
        "advanced": "Give a comprehensive, technical explanation with advanced concepts and terminology."
    }
    
    examples_instruction = "Include practical examples and use cases." if include_examples else "Focus on theoretical concepts without specific examples."
    
    prompt = f"""
You are an expert educator and technical writer. Your task is to provide a comprehensive explanation of the given topic and create a corresponding test case.

Topic: {topic}
Complexity Level: {complexity_level}
Instructions: {complexity_instructions.get(complexity_level, complexity_instructions["intermediate"])}
Examples: {examples_instruction}

Please provide your response in the following JSON format:
{{
    "explanation": "Your detailed explanation of the topic here. Make it comprehensive and well-structured.",
    "test_case": {{
        "input": "A specific input or scenario to test understanding",
        "expected_output": "The expected result or answer",
        "description": "Brief description of what this test case validates"
    }}
}}

Requirements:
1. The explanation should be accurate, well-structured, and appropriate for the specified complexity level
2. The test case should directly relate to the explanation and test key concepts
3. Ensure the JSON is properly formatted and valid
4. The explanation should be at least 100 words but not exceed 1000 words
5. The test case should be practical and verifiable

Topic to explain: {topic}
"""
    
    return prompt

def validate_gpt_response(response_text: str) -> dict:
    """Validate and parse the GPT response"""
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in response")
        
        json_str = json_match.group()
        parsed_response = json.loads(json_str)
        
        # Validate required fields
        required_fields = ["explanation", "test_case"]
        for field in required_fields:
            if field not in parsed_response:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate test_case structure
        test_case = parsed_response["test_case"]
        required_test_fields = ["input", "expected_output", "description"]
        for field in required_test_fields:
            if field not in test_case:
                raise ValueError(f"Missing required test case field: {field}")
        
        # Validate content length
        explanation = parsed_response["explanation"]
        if len(explanation.split()) < 20:
            raise ValueError("Explanation is too short")
        
        if len(explanation.split()) > 1000:
            raise ValueError("Explanation is too long")
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in response: {str(e)}")
    except Exception as e:
        raise ValueError(f"Response validation failed: {str(e)}")


@app.post("/explain-topic", response_model=ExplanationResponse)
async def explain_topic(
    request: TopicRequest,
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    """
    Generate an explanation and test case for a given topic using GPT
    """
    try:
        # Validate Gemini configuration
        if not settings.validate_gemini_config():
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        # Construct the detailed prompt
        prompt = construct_detailed_prompt(
            request.topic, 
            request.complexity_level, 
            request.include_examples
        )
        
        # Call Gemini API through service
        result = await gemini_service.generate_completion(
            prompt=prompt,
            model=settings.GEMINI_MODEL,
            temperature=settings.GEMINI_TEMPERATURE,
            max_tokens=settings.GEMINI_MAX_TOKENS,
            system_message="You are an expert educator and technical writer."
        )
        
        # Check for API errors
        if result.get("error"):
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {result['error']}")
        
        # Validate and parse the response
        validated_response = validate_gpt_response(result["text"])
        
        # Create the response object
        response_obj = ExplanationResponse(
            topic=request.topic,
            explanation=validated_response["explanation"],
            test_case=TestCase(**validated_response["test_case"]),
            complexity_level=request.complexity_level,
            metadata={
                "prompt_length": len(prompt),
                "response_length": len(result["text"]),
                "model_used": result["model"],
                "processing_successful": True,
                "tokens_used": result["usage"]["total_tokens"],
                "prompt_tokens": result["usage"]["prompt_tokens"],
                "completion_tokens": result["usage"]["completion_tokens"]
            }
        )
        
        logger.info(f"Successfully processed topic: {request.topic}")
        return response_obj
        
    except ValueError as e:
        logger.error(f"Response validation error for topic '{request.topic}': {str(e)}")
        raise HTTPException(status_code=422, detail=f"Response validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Internal server error for topic '{request.topic}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
