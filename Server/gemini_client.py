import os
import google.generativeai as genai
from typing import Dict, Any, List
import logging
import json

logger = logging.getLogger(__name__)


class GeminiService:
    """Service class for Google Gemini API interactions"""

    def __init__(self, api_key: str = None):
        # Import here to avoid circular imports
        from config import settings

        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError("Gemini API key is required")

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

    async def generate_completion(
            self,
            prompt: str,
            model: str = "gemini-2.0-flash-exp",
            temperature: float = 0.7,
            max_tokens: int = 1500,
            system_message: str = None
    ) -> Dict[str, Any]:
        """
        Generate a completion using Google Gemini API

        Args:
            prompt: The user prompt
            model: The Gemini model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_message: Optional system message

        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Initialize the model
            model_instance = genai.GenerativeModel(
                model_name=model,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )

            # Prepare the full prompt
            full_prompt = prompt
            if system_message:
                full_prompt = f"System: {system_message}\n\nUser: {prompt}"

            logger.info(f"Making Gemini API call with model: {model}")

            # Generate content
            response = model_instance.generate_content(full_prompt)

            # Extract text from response
            response_text = response.text if response.text else ""

            # Calculate approximate token usage (Gemini doesn't provide exact counts)
            prompt_tokens = len(full_prompt.split()) * 1.3  # Rough estimation
            completion_tokens = len(response_text.split()) * 1.3
            total_tokens = prompt_tokens + completion_tokens

            result = {
                "text": response_text,
                "model": model,
                "usage": {
                    "prompt_tokens": int(prompt_tokens),
                    "completion_tokens": int(completion_tokens),
                    "total_tokens": int(total_tokens)
                },
                "finish_reason": "stop"  # Gemini doesn't provide detailed finish reasons
            }

            logger.info(f"Gemini API call successful. Estimated tokens used: {result['usage']['total_tokens']}")
            return result

        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise Exception(f"Gemini API error: {str(e)}")

    async def generate_batch_completions(
            self,
            prompts: List[str],
            model: str = "gemini-2.0-flash-exp",
            temperature: float = 0.7,
            max_tokens: int = 1500,
            system_message: str = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple completions in batch

        Args:
            prompts: List of prompts to process
            model: The Gemini model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_message: Optional system message

        Returns:
            List of response dictionaries
        """
        results = []

        for i, prompt in enumerate(prompts):
            try:
                result = await self.generate_completion(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    system_message=system_message
                )
                results.append(result)
                logger.info(f"Batch completion {i + 1}/{len(prompts)} successful")

            except Exception as e:
                logger.error(f"Batch completion {i + 1}/{len(prompts)} failed: {str(e)}")
                results.append({
                    "error": str(e),
                    "text": None,
                    "usage": {"total_tokens": 0}
                })

        return results


# Global instance
gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global gemini_service
    if gemini_service is None:
        from config import settings
        gemini_service = GeminiService(api_key=settings.GEMINI_API_KEY)
    return gemini_service
