import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app, construct_detailed_prompt, validate_gpt_response
from gemini_client import GeminiService
import json

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "GPT Topic Explanation Service is running"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_construct_detailed_prompt():
    """Test prompt construction"""
    prompt = construct_detailed_prompt("Machine Learning", "intermediate", True)
    assert "Machine Learning" in prompt
    assert "intermediate" in prompt
    assert "JSON format" in prompt
    assert len(prompt) > 100

def test_validate_gpt_response_valid():
    """Test response validation with valid JSON"""
    valid_response = '''
    {
        "explanation": "This is a detailed explanation of the topic with sufficient length to meet requirements.",
        "test_case": {
            "input": "Sample input",
            "expected_output": "Expected result",
            "description": "Test description"
        }
    }
    '''
    
    result = validate_gpt_response(valid_response)
    assert "explanation" in result
    assert "test_case" in result
    assert "input" in result["test_case"]

def test_validate_gpt_response_invalid():
    """Test response validation with invalid JSON"""
    invalid_response = "This is not a JSON response"
    
    with pytest.raises(ValueError):
        validate_gpt_response(invalid_response)

def test_explain_topic_endpoint_validation():
    """Test the explain topic endpoint with invalid input"""
    # Test empty topic
    response = client.post("/explain-topic", json={"topic": ""})
    assert response.status_code == 422
    
    # Test topic too long
    long_topic = "a" * 501
    response = client.post("/explain-topic", json={"topic": long_topic})
    assert response.status_code == 422

def test_batch_explain_too_many():
    """Test batch endpoint with too many requests"""
    requests = [{"topic": f"Topic {i}"} for i in range(11)]
    response = client.post("/batch-explain", json=requests)
    assert response.status_code == 400
    assert "Maximum 10 topics" in response.json()["detail"]

# Mock test for the actual GPT integration (requires API key)
@pytest.mark.asyncio
async def test_gemini_service():
    """Test Gemini service with mocked response"""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        # Mock the Gemini response
        mock_response = MagicMock()
        mock_response.text = '''
        {
            "explanation": "This is a test explanation with sufficient length to meet the requirements for testing purposes.",
            "test_case": {
                "input": "Test input",
                "expected_output": "Test output",
                "description": "Test case description"
            }
        }
        '''
        
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        # Test the service
        service = GeminiService(api_key="test-key")
        result = await service.generate_completion("Test prompt")
        
        assert result["text"] is not None
        assert result["usage"]["total_tokens"] > 0

@patch('gemini_client.GeminiService')
def test_explain_topic_endpoint_mocked(mock_service_class):
    """Test the explain topic endpoint with mocked Gemini service"""
    # Setup mock
    mock_service = AsyncMock()
    mock_service.generate_completion.return_value = {
        "text": '''
        {
            "explanation": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task.",
            "test_case": {
                "input": "A dataset of house prices with features like size, location, and age",
                "expected_output": "A model that can predict house prices for new properties",
                "description": "Tests understanding of supervised learning with regression"
            }
        }
        ''',
        "model": "gemini-2.0-flash-exp",
        "usage": {"total_tokens": 150, "prompt_tokens": 75, "completion_tokens": 75},
        "finish_reason": "stop"
    }
    mock_service_class.return_value = mock_service
    
    response = client.post("/explain-topic", json={
        "topic": "Machine Learning",
        "complexity_level": "intermediate",
        "include_examples": True
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "test_case" in data
    assert data["topic"] == "Machine Learning"
