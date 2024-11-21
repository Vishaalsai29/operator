# test_llm_math_ability.py

import pytest
from openai import OpenAI
from google.colab import userdata

client = OpenAI(api_key=userdata.get("DSBA_LLAMA3_KEY"))
client.base_url = (
    f"https://{WORKSPACE}--vllm-openai-compatible-serve.modal.run/v1"
)
model = "/models/NousResearch/Meta-Llama-3-8B-Instruct"

def generate_response(prompt):
    """Helper function to generate a response from the LLM."""
    messages = [
        {
            "role": "system",
            "content": "You are a mathematical assistant, skilled in solving arithmetic problems.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return response.strip()

def test_addition():
    """Test LLM's ability to perform addition."""
    prompt = "What is 2+2?"
    response = generate_response(prompt)
    assert response == "4", f"Expected '4', but got {response}"

def test_subtraction():
    """Test LLM's ability to perform subtraction."""
    prompt = "What is 5-3?"
    response = generate_response(prompt)
    assert response == "2", f"Expected '2', but got {response}"

def test_multiplication():
    """Test LLM's ability to perform multiplication."""
    prompt = "What is 6*7?"
    response = generate_response(prompt)
    assert response == "42", f"Expected '42', but got {response}"

def test_division():
    """Test LLM's ability to perform division."""
    prompt = "What is 12/4?"
    response = generate_response(prompt)
    assert response == "3", f"Expected '3', but got {response}"

def test_exponentiation():
    """Test LLM's ability to perform exponentiation."""
    prompt = "What is 2^3?"
    response = generate_response(prompt)
    assert response == "8", f"Expected '8', but got {response}"

# Run the tests
if __name__ == "__main__":
    pytest.main()
