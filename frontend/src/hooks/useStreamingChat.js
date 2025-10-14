import { useCallback, useRef, useState } from 'react'
import useChatStore from '../store/chatStore'
import useConversationStore from '../store/conversationStore'

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'

export const useStreamingChat = () => {
  const wsRef = useRef(null)
  const [isConnected, setIsConnected] = useState(false)
  const [streamingResponses, setStreamingResponses] = useState({})
  
  const {
    currentConversationId,
    setCurrentConversationId,
    addMessage,
    setIsSending,
  } = useChatStore()

  const { addConversation, updateConversation } = useConversationStore()

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    const ws = new WebSocket(`${WS_BASE_URL}/api/v1/stream/chat`)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      switch (data.type) {
        case 'conversation_info':
          if (!currentConversationId) {
            setCurrentConversationId(data.conversation_id)
          }
          break
          
        case 'model_start':
          setStreamingResponses(prev => ({
            ...prev,
            [data.provider]: {
              content: '',
              status: 'streaming',
              startTime: data.timestamp
            }
          }))
          break
          
        case 'model_thinking':
          setStreamingResponses(prev => ({
            ...prev,
            [data.provider]: {
              ...prev[data.provider],
              status: 'thinking'
            }
          }))
          break
          
        case 'model_chunk':
          setStreamingResponses(prev => ({
            ...prev,
            [data.provider]: {
              ...prev[data.provider],
              content: (prev[data.provider]?.content || '') + data.content,
              status: 'streaming'
            }
          }))
          break
          
        case 'model_complete':
          setStreamingResponses(prev => ({
            ...prev,
            [data.provider]: {
              ...prev[data.provider],
              status: 'complete',
              latency_ms: data.latency_ms
            }
          }))
          break
          
        case 'model_error':
          setStreamingResponses(prev => ({
            ...prev,
            [data.provider]: {
              content: '',
              error: data.error,
              status: 'error',
              latency_ms: data.latency_ms
            }
          }))
          break
          
        case 'all_complete':
          // Add completed responses to message history
          const completedMessages = Object.entries(streamingResponses)
            .filter(([_, response]) => response.status === 'complete' && response.content)
            .map(([provider, response]) => ({
              role: 'assistant',
              content: response.content,
              model_provider: provider,
              created_at: new Date().toISOString(),
            }))
          
          if (completedMessages.length > 0) {
            completedMessages.forEach(msg => addMessage(msg))
          }
          
          setIsSending(false)
          break
          
        case 'error':
          console.error('WebSocket error:', data.error)
          setIsSending(false)
          break
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setIsConnected(false)
      setIsSending(false)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
      setIsSending(false)
    }

    wsRef.current = ws
  }, [currentConversationId, setCurrentConversationId, addMessage, setIsSending, streamingResponses])

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])

  const sendStreamingMessage = useCallback(async (prompt, models = null) => {
    if (!prompt.trim()) return
    
    // Connect if not connected
    if (!isConnected) {
      connect()
      // Wait for connection
      await new Promise((resolve) => {
        const checkConnection = setInterval(() => {
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            clearInterval(checkConnection)
            resolve()
          }
        }, 100)
      })
    }

    setIsSending(true)
    setStreamingResponses({})

    // Add user message optimistically
    const userMessage = {
      role: 'user',
      content: prompt,
      created_at: new Date().toISOString(),
    }
    addMessage(userMessage)

    // Send message through WebSocket
    wsRef.current.send(JSON.stringify({
      prompt,
      conversation_id: currentConversationId,
      models
    }))

    // Update conversation if this is the first message
    if (!currentConversationId) {
      const title = prompt.slice(0, 50) + (prompt.length > 50 ? '...' : '')
      addConversation({
        id: Date.now(), // Temporary ID, will be updated
        title,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      })
    } else {
      updateConversation(currentConversationId, {
        updated_at: new Date().toISOString(),
      })
    }
  }, [
    isConnected,
    connect,
    currentConversationId,
    setIsSending,
    addMessage,
    addConversation,
    updateConversation,
  ])

  return {
    isConnected,
    connect,
    disconnect,
    sendStreamingMessage,
    streamingResponses
  }
}

export default useStreamingChat
