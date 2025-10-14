/**
 * useChat hook with RAG support
 * Location: frontend/src/hooks/useChat.js
 */

import { useState } from 'react'
import { chatApi } from '../services/api'
import useChatStore from '../store/chatStore'

const useChat = () => {
  const { 
    conversationId, 
    addMessage, 
    setResponses, 
    setIsSending,
    setConversationId,
    setRagContext 
  } = useChatStore()

  const sendMessage = async (prompt, selectedModels = null, ragEnabled = false, contextCount = 3) => {
    try {
      setIsSending(true)

      // Add user message to UI immediately
      addMessage({
        role: 'user',
        content: prompt,
      })

      // Send to API with RAG options
      const response = await chatApi.send({
        prompt,
        conversationId,
        models: selectedModels,
        useRAG: ragEnabled,        // Pass RAG flag
        topK: contextCount          // Pass context count
      })

      // Update conversation ID if it's a new conversation
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id)
      }

      // Set model responses
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