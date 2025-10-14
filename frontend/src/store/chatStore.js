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
  setCurrentConversationId: (id) => set({ currentConversationId: id }),
  setConversationId: (id) => set({ currentConversationId: id }), // Alias for compatibility
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),
  addMessages: (newMessages) => set((state) => ({
    messages: [...state.messages, ...newMessages]
  })),
  setCurrentResponses: (responses) => set({ currentResponses: responses }),
  setResponses: (responses) => set({ currentResponses: responses }), // Alias for compatibility
  setIsSending: (isSending) => set({ isSending }),
  setIsLoading: (isLoading) => set({ isLoading }),
  setRagContext: (ragContextUsed, contextChunks) => set({ ragContextUsed, contextChunks }),
  
  reset: () => set({
    currentConversationId: null,
    messages: [],
    currentResponses: [],
    isSending: false,
    isLoading: false,
    ragContextUsed: false,
    contextChunks: null,
  }),
}))

export default useChatStore