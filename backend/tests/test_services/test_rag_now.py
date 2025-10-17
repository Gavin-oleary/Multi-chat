"""
Quick test to verify RAG is working
Run this from the backend directory: python test_rag_now.py
"""

import requests
import json

API_BASE_URL = "http://localhost:8000/api/v1"

print("=" * 80)
print("TESTING RAG FUNCTIONALITY")
print("=" * 80)

# Test 1: Check if documents exist
print("\n1. Checking for uploaded documents...")
try:
    response = requests.get(f"{API_BASE_URL}/documents/")
    docs = response.json()
    print(f"   Found {len(docs)} documents in database")
    if docs:
        for doc in docs:
            print(f"   - Document {doc['id']}: {doc.get('doc_metadata', {}).get('filename', 'Unknown')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Test similarity search directly
print("\n2. Testing similarity search...")
try:
    response = requests.post(
        f"{API_BASE_URL}/documents/search",
        json={
            "query": "antenna frequency",
            "top_k": 3
        }
    )
    results = response.json()
    print(f"   Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"   Result {i}: similarity={result.get('similarity', 0):.4f}")
        print(f"   Text preview: {result.get('chunk_text', '')[:100]}...")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Send chat WITH RAG enabled
print("\n3. Testing chat endpoint WITH RAG...")
try:
    response = requests.post(
        f"{API_BASE_URL}/chat/",
        json={
            "prompt": "What antennas are mentioned in the document?",
            "use_rag": True,
            "top_k": 3
        }
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   RAG Context Used: {data.get('rag_context_used')}")
        print(f"   Context Chunks: {len(data.get('context_chunks', []))}")
        
        if data.get('context_chunks'):
            print(f"\n   Retrieved Context:")
            for i, chunk in enumerate(data['context_chunks'], 1):
                print(f"   Chunk {i} (similarity: {chunk.get('similarity', 0):.4f}):")
                print(f"   {chunk.get('content', '')[:150]}...")
        
        print(f"\n   Model Responses:")
        for resp in data.get('responses', []):
            provider = resp.get('provider')
            content = resp.get('content', '')[:200]
            print(f"   - {provider}: {content}...")
    else:
        print(f"   ERROR Response: {response.text}")
        
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Send chat WITHOUT RAG
print("\n4. Testing chat endpoint WITHOUT RAG...")
try:
    response = requests.post(
        f"{API_BASE_URL}/chat/",
        json={
            "prompt": "What antennas are mentioned in the document?",
            "use_rag": False
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   RAG Context Used: {data.get('rag_context_used')}")
        print(f"   Models should not have context...")
    else:
        print(f"   ERROR Response: {response.text}")
        
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print("\nCheck your backend logs for detailed debug output!")
print("Look for lines starting with:")
print("  - 'CHAT REQUEST RECEIVED:'")
print("  - '✓ RAG IS ENABLED'")
print("  - '✓ RAG search returned X results'")