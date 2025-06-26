import os
from openai import AsyncOpenAI
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service class for OpenAI API interactions"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def generate_completion(
        self,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1500,
        system_message: str = None
    ) -> Dict[str, Any]:
        """
        Generate a completion using OpenAI's chat completion API
        
        Args:
            prompt: The user prompt
            model: The OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            system_message: Optional system message
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            logger.info(f"Making OpenAI API call with model: {model}")
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = {
                "text": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                "finish_reason": response.choices[0].finish_reason
            }
            
            logger.info(f"OpenAI API call successful. Tokens used: {result['usage']['total_tokens']}")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_batch_completions(
        self,
        prompts: List[str],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1500,
        system_message: str = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple completions in batch
        
        Args:
            prompts: List of prompts to process
            model: The OpenAI model to use
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
                logger.info(f"Batch completion {i+1}/{len(prompts)} successful")
                
            except Exception as e:
                logger.error(f"Batch completion {i+1}/{len(prompts)} failed: {str(e)}")
                results.append({
                    "error": str(e),
                    "text": None,
                    "usage": {"total_tokens": 0}
                })
        
        return results

# Global instance
openai_service = None

def get_openai_service() -> OpenAIService:
    """Get or create OpenAI service instance"""
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service
