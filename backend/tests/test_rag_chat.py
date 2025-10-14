"""
Test script for RAG-enhanced chat functionality.
Tests the chat endpoint with and without RAG enabled.
"""

import requests
import json
from typing import Optional, List


API_BASE_URL = "http://localhost:8000/api/v1"


def send_chat_message(
    prompt: str,
    use_rag: bool = False,
    top_k: int = 3,
    conversation_id: Optional[int] = None,
    models: Optional[List[str]] = None
):
    """
    Send a chat message to the API.
    
    Args:
        prompt: The user's question/prompt
        use_rag: Whether to enable RAG context retrieval
        top_k: Number of context chunks to retrieve (if RAG enabled)
        conversation_id: Optional conversation ID to continue existing chat
        models: Optional list of specific models to use
    """
    url = f"{API_BASE_URL}/chat/"
    
    payload = {
        "prompt": prompt,
        "use_rag": use_rag,
        "top_k": top_k
    }
    
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    if models:
        payload["models"] = models
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response: {e.response.text}")
        return None


def print_response(response_data: dict, rag_enabled: bool):
    """Pretty print the chat response."""
    if not response_data:
        return
    
    print(f"\nConversation ID: {response_data.get('conversation_id')}")
    print(f"User Message ID: {response_data.get('user_message_id')}")
    
    if rag_enabled:
        print(f"RAG Context Used: {response_data.get('rag_context_used', False)}")
        
        if response_data.get('context_chunks'):
            print(f"\nRetrieved Context Chunks ({len(response_data['context_chunks'])}):")
            for i, chunk in enumerate(response_data['context_chunks'], 1):
                print(f"\n  Chunk {i}:")
                print(f"  Similarity: {chunk.get('similarity', 0):.4f}")
                print(f"  Text: {chunk.get('text', '')[:100]}...")
    
    print(f"\nModel Responses ({len(response_data.get('responses', []))}):")
    print("-" * 60)
    
    for resp in response_data.get('responses', []):
        provider = resp.get('provider', 'Unknown')
        content = resp.get('content', '')
        error = resp.get('error')
        latency = resp.get('latency_ms')
        
        print(f"\n{provider.upper()}:")
        if error:
            print(f"  ✗ Error: {error}")
        else:
            print(f"  ✓ Response: {content[:200]}...")
            if latency:
                print(f"  ⏱ Latency: {latency:.2f}ms")


def test_without_rag():
    """Test chat without RAG enabled."""
    print("=" * 60)
    print("Test 1: Chat WITHOUT RAG")
    print("=" * 60)
    
    prompt = "What is the capital of France?"
    print(f"\nPrompt: {prompt}")
    
    response = send_chat_message(
        prompt=prompt,
        use_rag=False
    )
    
    print_response(response, rag_enabled=False)
    
    return response.get('conversation_id') if response else None


def test_with_rag(conversation_id: Optional[int] = None):
    """Test chat with RAG enabled."""
    print("\n" + "=" * 60)
    print("Test 2: Chat WITH RAG")
    print("=" * 60)
    
    prompt = "What is the capital of France?"
    print(f"\nPrompt: {prompt}")
    print(f"RAG Enabled: True")
    print(f"Top K: 3")
    
    response = send_chat_message(
        prompt=prompt,
        use_rag=True,
        top_k=3,
        conversation_id=conversation_id
    )
    
    print_response(response, rag_enabled=True)
    
    return response.get('conversation_id') if response else None


def test_custom_query(prompt: str, use_rag: bool = True, top_k: int = 5):
    """Test with a custom query."""
    print("\n" + "=" * 60)
    print("Test 3: Custom Query")
    print("=" * 60)
    
    print(f"\nPrompt: {prompt}")
    print(f"RAG Enabled: {use_rag}")
    print(f"Top K: {top_k}")
    
    response = send_chat_message(
        prompt=prompt,
        use_rag=use_rag,
        top_k=top_k
    )
    
    print_response(response, rag_enabled=use_rag)


def main():
    """Main test function."""
    print("\n🔍 RAG-Enhanced Chat Test Suite\n")
    
    # Test 1: Without RAG
    conv_id = test_without_rag()
    
    # Test 2: With RAG (continue same conversation)
    test_with_rag(conversation_id=conv_id)
    
    # Test 3: Custom queries (uncomment to test)
    # test_custom_query(
    #     prompt="Tell me about Python programming",
    #     use_rag=True,
    #     top_k=5
    # )
    
    # Test 4: Query about moon orbits
    # test_custom_query(
    #     prompt="How long does it take for the moon to orbit Earth?",
    #     use_rag=True,
    #     top_k=3
    # )
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()