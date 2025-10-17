/**
 * useChat hook with RAG support - FIXED VERSION
 * Location: frontend/src/hooks/useChat.js
 */

import { chatApi } from '../services/api'
import useChatStore from '../store/chatStore'

const useChat = () => {
  const { 
    conversationId, 
    addMessage, 
    setResponses, 
    setIsSending,
    setConversationId,
    setRagContext,
    addMessages  // Add this for batch adding messages
  } = useChatStore()

  const sendMessage = async (prompt, selectedModels = null, ragEnabled = false, contextCount = 3) => {
    try {
      setIsSending(true)

      // Add user message to UI immediately
      addMessage({
        role: 'user',
        content: prompt,
        created_at: new Date().toISOString()
      })

      // Send to API with RAG options
      const response = await chatApi.send({
        prompt,
        conversation_id: conversationId,  // This should be sent even if null
        models: selectedModels,
        use_rag: ragEnabled,        // Fixed: snake_case for backend
        top_k: contextCount          // Fixed: snake_case for backend
      })

      // CRITICAL FIX: Update conversation ID if it's a new conversation
      // This ensures follow-up messages work correctly
      if (!conversationId && response.conversation_id) {
        console.log('Setting new conversation ID:', response.conversation_id)
        setConversationId(response.conversation_id)
      }

      // Add assistant responses to messages
      // The backend returns responses array with model responses
      if (response.responses && response.responses.length > 0) {
        const assistantMessages = response.responses
          .filter(r => !r.error && r.content)  // Only add successful responses
          .map(r => ({
            role: 'assistant',
            content: r.content,
            model_provider: r.provider,
            created_at: new Date().toISOString(),
            latency_ms: r.latency_ms
          }))
        
        // Add all assistant messages at once
        addMessages(assistantMessages)
      }

      // Set current responses for display (includes errors)
      setResponses(response.responses)
      
      // Set RAG context if used
      if (response.rag_context_used) {
        setRagContext(response.rag_context_used, response.context_chunks)
      } else {
        setRagContext(false, null)
      }

      return response
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Show error details
      if (error.response) {
        console.error('Response error:', error.response.data)
      }
      
      throw error
    } finally {
      setIsSending(false)
    }
  }

  return {
    sendMessage,
  }
}

export default useChat