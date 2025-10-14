/**
 * API service with RAG support
 * Enhanced API client for Multi-Model Chat with document management
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== Conversations ====================

export const conversationApi = {
  list: async (skip = 0, limit = 100) => {
    const response = await api.get('/conversations', {
      params: { skip, limit },
    });
    return response.data;
  },

  get: async (conversationId) => {
    const response = await api.get(`/conversations/${conversationId}`);
    return response.data;
  },

  create: async (title) => {
    const response = await api.post('/conversations', { title });
    return response.data;
  },

  update: async (conversationId, data) => {
    const response = await api.put(`/conversations/${conversationId}`, data);
    return response.data;
  },

  delete: async (conversationId) => {
    const response = await api.delete(`/conversations/${conversationId}`);
    return response.data;
  },
};

// ==================== Chat (RAG-Enhanced) ====================

export const chatApi = {
  /**
   * Send a chat message with optional RAG
   */
  send: async ({ prompt, conversationId = null, models = null, useRAG = false, topK = 3 }) => {
    const response = await api.post('/chat', {
      prompt,
      conversation_id: conversationId,
      models,
      use_rag: useRAG,
      top_k: topK,
    });
    return response.data;
  },

  /**
   * Search across conversations semantically
   */
  searchConversations: async (query, topK = 5) => {
    const response = await api.post('/chat/search-conversations', null, {
      params: { query, top_k: topK },
    });
    return response.data;
  },
};

// ==================== Documents (RAG) ====================

export const documentApi = {
  /**
   * Upload a document file
   */
  upload: async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });
    return response.data;
  },

  /**
   * Create a document from text
   */
  create: async (content, metadata = {}) => {
    const response = await api.post('/documents', {
      content,
      metadata,
    });
    return response.data;
  },

  /**
   * Get a specific document
   */
  get: async (documentId) => {
    const response = await api.get(`/documents/${documentId}`);
    return response.data;
  },

  /**
   * List all documents
   */
  list: async (skip = 0, limit = 100) => {
    const response = await api.get('/documents', {
      params: { skip, limit },
    });
    return response.data;
  },

  /**
   * Delete a document
   */
  delete: async (documentId) => {
    const response = await api.delete(`/documents/${documentId}`);
    return response.data;
  },

  /**
   * Semantic search across documents
   */
  search: async (query, topK = 10, model = 'text-embedding-ada-002') => {
    const response = await api.post('/documents/search', {
      query,
      top_k: topK,
      model,
    });
    return response.data;
  },
};

// ==================== Messages ====================

export const messageApi = {
  list: async (conversationId) => {
    const response = await api.get(`/conversations/${conversationId}/messages`);
    return response.data;
  },

  get: async (messageId) => {
    const response = await api.get(`/messages/${messageId}`);
    return response.data;
  },
};

// ==================== Error Handling ====================

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.detail || error.response.statusText;
      console.error('API Error:', message);
      throw new Error(message);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
      throw new Error('Network error - please check your connection');
    } else {
      // Something else happened
      console.error('Error:', error.message);
      throw error;
    }
  }
);

// ==================== Provider API ====================

export const providerApi = {
  async getHealth() {
    try {
      const response = await api.get('/providers/health');
      return response;
    } catch (error) {
      console.error('Failed to fetch provider health:', error);
      // Return empty data structure on error to prevent crashes
      return { data: {} };
    }
  }
};

// ==================== System Prompts ====================

export const systemPromptsApi = {
  list: async () => {
    const response = await api.get('/system-prompts');
    return response.data;
  },

  get: async (modelProvider) => {
    const response = await api.get(`/system-prompts/${modelProvider}`);
    return response.data;
  },

  create: async (promptData) => {
    const response = await api.post('/system-prompts', promptData);
    return response.data;
  },

  update: async (promptId, updateData) => {
    const response = await api.put(`/system-prompts/${promptId}`, updateData);
    return response.data;
  },

  delete: async (promptId) => {
    const response = await api.delete(`/system-prompts/${promptId}`);
    return response.data;
  },

  initializeDefaults: async () => {
    const response = await api.post('/system-prompts/initialize-defaults');
    return response.data;
  }
};

// ==================== Export ====================

export default {
  conversation: conversationApi,
  chat: chatApi,
  document: documentApi,
  message: messageApi,
  provider: providerApi,
  systemPrompts: systemPromptsApi,
};