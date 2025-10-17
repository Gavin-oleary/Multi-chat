/**
 * Chat store with improved state management
 * Location: frontend/src/store/chatStore.js
 */

import { create } from 'zustand'

const useChatStore = create((set, get) => ({
  currentConversationId: null,
  messages: [],
  currentResponses: [],
  isSending: false,
  isLoading: false,
  selectedModels: null,
  ragContextUsed: false,
  contextChunks: null,
  
  // Getters
  get conversationId() {
    return get().currentConversationId
  },
  
  // Setters
  setCurrentConversationId: (id) => {
    console.log('ChatStore: Setting conversation ID to', id)
    set({ currentConversationId: id })
  },
  
  setConversationId: (id) => {
    console.log('ChatStore: Setting conversation ID to', id)
    set({ currentConversationId: id })
  },
  
  setMessages: (messages) => set({ messages }),
  
  addMessage: (message) => {
    console.log('ChatStore: Adding message', message)
    set((state) => ({ 
      messages: [...state.messages, message] 
    }))
  },
  
  addMessages: (newMessages) => {
    console.log('ChatStore: Adding messages', newMessages.length)
    set((state) => ({
      messages: [...state.messages, ...newMessages]
    }))
  },
  
  setCurrentResponses: (responses) => set({ currentResponses: responses }),
  
  setResponses: (responses) => set({ currentResponses: responses }),
  
  setIsSending: (isSending) => set({ isSending }),
  
  setIsLoading: (isLoading) => set({ isLoading }),
  
  setRagContext: (ragContextUsed, contextChunks) => set({ ragContextUsed, contextChunks }),
  
  reset: () => {
    console.log('ChatStore: Resetting all state')
    set({
      currentConversationId: null,
      messages: [],
      currentResponses: [],
      isSending: false,
      isLoading: false,
      ragContextUsed: false,
      contextChunks: null,
    })
  },
}))

export default useChatStore