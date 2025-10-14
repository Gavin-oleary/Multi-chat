import { create } from 'zustand'

const useConversationStore = create((set) => ({
  // List of all conversations
  conversations: [],
  
  // Loading state
  isLoading: false,
  
  // Actions
  setConversations: (conversations) => set({ conversations }),
  
  addConversation: (conversation) => set((state) => ({
    conversations: [conversation, ...state.conversations]
  })),
  
  updateConversation: (id, updates) => set((state) => ({
    conversations: state.conversations.map((conv) =>
      conv.id === id ? { ...conv, ...updates } : conv
    )
  })),
  
  deleteConversation: (id) => set((state) => ({
    conversations: state.conversations.filter((conv) => conv.id !== id)
  })),
  
  setIsLoading: (isLoading) => set({ isLoading }),
  
  reset: () => set({
    conversations: [],
    isLoading: false,
  }),
}))

export default useConversationStore