/**
 * Frontend application constants
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const API_VERSION = 'v1'
export const API_ENDPOINTS = {
  chat: `/api/${API_VERSION}/chat`,
  stream: `/api/${API_VERSION}/stream/chat`,
  conversations: `/api/${API_VERSION}/conversations`,
  messages: `/api/${API_VERSION}/messages`,
  providers: `/api/${API_VERSION}/providers`,
}

// WebSocket Configuration
export const WS_BASE_URL = API_BASE_URL.replace(/^http/, 'ws')
export const WS_RECONNECT_DELAY = 3000 // 3 seconds
export const WS_MAX_RECONNECT_ATTEMPTS = 5

// Model Configuration
export const MODEL_DISPLAY_NAMES = {
  claude: 'Claude',
  chatgpt: 'ChatGPT',
  gemini: 'Gemini',
  grok: 'Grok',
  perplexity: 'Perplexity',
}

export const MODEL_COLORS = {
  claude: '#6B46C1',  // Purple
  chatgpt: '#10A37F', // Green
  gemini: '#4285F4',  // Blue
  grok: '#000000',    // Black
  perplexity: '#20B2AA', // Light Sea Green
}

// UI Configuration
export const MAX_MESSAGE_LENGTH = 10000
export const MIN_MESSAGE_LENGTH = 1
export const DEBOUNCE_DELAY = 300 // milliseconds

// Error Messages
export const ERROR_MESSAGES = {
  network: 'Network error. Please check your connection.',
  server: 'Server error. Please try again later.',
  validation: 'Please enter a valid message.',
  tooLong: 'Message is too long. Please shorten it.',
  empty: 'Message cannot be empty.',
  wsConnection: 'Connection lost. Attempting to reconnect...',
  wsReconnectFailed: 'Unable to connect to server. Please refresh the page.',
}

// Local Storage Keys
export const STORAGE_KEYS = {
  selectedModels: 'chat_selected_models',
  theme: 'chat_theme',
  conversationId: 'chat_conversation_id',
}
