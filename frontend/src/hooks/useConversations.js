import { useCallback, useEffect } from 'react'
import { conversationApi } from '../services/api'
import useConversationStore from '../store/conversationStore'
import useChatStore from '../store/chatStore'

export const useConversations = () => {
  const {
    conversations,
    isLoading,
    setConversations,
    addConversation,
    updateConversation,
    deleteConversation,
    setIsLoading,
  } = useConversationStore()

  const { setCurrentConversationId, setMessages } = useChatStore()

  // Load all conversations
  const loadConversations = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await conversationApi.list(0, 100)
      setConversations(response)
    } catch (error) {
      console.error('Error loading conversations:', error)
    } finally {
      setIsLoading(false)
    }
  }, [setConversations, setIsLoading])

  // Load a specific conversation with messages
  const loadConversation = useCallback(async (id) => {
    setIsLoading(true)
    try {
      const response = await conversationApi.get(id)
      const conversation = response
      
      setCurrentConversationId(id)
      setMessages(conversation.messages || [])
      
      return conversation
    } catch (error) {
      console.error('Error loading conversation:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [setCurrentConversationId, setMessages, setIsLoading])

  // Create a new conversation
  const createConversation = useCallback(async (title) => {
    try {
      const response = await conversationApi.create(title)
      const newConversation = response
      
      addConversation(newConversation)
      return newConversation
    } catch (error) {
      console.error('Error creating conversation:', error)
      throw error
    }
  }, [addConversation])

  // Rename a conversation
  const renameConversation = useCallback(async (id, title) => {
    try {
      const response = await conversationApi.update(id, { title })
      updateConversation(id, response)
      return response
    } catch (error) {
      console.error('Error renaming conversation:', error)
      throw error
    }
  }, [updateConversation])

  // Delete a conversation
  const removeConversation = useCallback(async (id) => {
    try {
      await conversationApi.delete(id)
      deleteConversation(id)
      
      // If deleting current conversation, clear chat
      const { currentConversationId, reset } = useChatStore.getState()
      if (currentConversationId === id) {
        reset()
      }
    } catch (error) {
      console.error('Error deleting conversation:', error)
      throw error
    }
  }, [deleteConversation])

  // Load conversations on mount
  useEffect(() => {
    loadConversations()
  }, [loadConversations])

  return {
    conversations,
    isLoading,
    loadConversations,
    loadConversation,
    createConversation,
    renameConversation,
    removeConversation,
  }
}

export default useConversations