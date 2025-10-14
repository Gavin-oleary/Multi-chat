/**
 * Input validation utilities for the frontend
 */

/**
 * Sanitize a string by trimming whitespace and removing dangerous characters
 * @param {string} str - The string to sanitize
 * @param {number} maxLength - Maximum allowed length
 * @returns {string} Sanitized string
 */
export const sanitizeString = (str, maxLength = null) => {
  if (!str) return ''
  
  // Remove null bytes and trim
  let sanitized = str.replace(/\0/g, '').trim()
  
  // Enforce max length if specified
  if (maxLength && sanitized.length > maxLength) {
    sanitized = sanitized.substring(0, maxLength)
  }
  
  return sanitized
}

/**
 * Validate prompt length and content
 * @param {string} prompt - The prompt to validate
 * @param {number} maxTokens - Maximum allowed tokens (default 2000)
 * @returns {{valid: boolean, error?: string}} Validation result
 */
export const validatePrompt = (prompt, maxTokens = 2000) => {
  if (!prompt || !prompt.trim()) {
    return { valid: false, error: 'Prompt cannot be empty' }
  }
  
  // Basic token estimation (4 chars per token on average)
  const estimatedTokens = Math.ceil(prompt.length / 4)
  
  if (estimatedTokens > maxTokens) {
    return { 
      valid: false, 
      error: `Prompt too long: approximately ${estimatedTokens} tokens (max ${maxTokens})` 
    }
  }
  
  // Check for excessive length
  if (prompt.length > 10000) {
    return { valid: false, error: 'Prompt exceeds maximum character limit (10,000)' }
  }
  
  return { valid: true }
}

/**
 * Validate conversation title
 * @param {string} title - The title to validate
 * @returns {{valid: boolean, error?: string}} Validation result
 */
export const validateTitle = (title) => {
  if (!title || !title.trim()) {
    return { valid: false, error: 'Title cannot be empty' }
  }
  
  if (title.length > 255) {
    return { valid: false, error: 'Title cannot exceed 255 characters' }
  }
  
  return { valid: true }
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
export const escapeHtml = (text) => {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
  }
  
  return text.replace(/[&<>"'/]/g, (char) => map[char])
}

/**
 * Validate that a value is a positive integer
 * @param {any} value - Value to validate
 * @returns {boolean} True if valid positive integer
 */
export const isValidId = (value) => {
  const num = Number(value)
  return Number.isInteger(num) && num > 0
}

/**
 * Model-specific token limits
 */
export const MODEL_TOKEN_LIMITS = {
  claude: 100000,
  chatgpt: 4096,
  gemini: 32768,
  grok: 8192,
  perplexity: 4096,
}

/**
 * Get token limit for a specific model
 * @param {string} model - Model name
 * @returns {number} Token limit
 */
export const getModelTokenLimit = (model) => {
  return MODEL_TOKEN_LIMITS[model.toLowerCase()] || 4096
}

/**
 * Validate prompt for specific models
 * @param {string} prompt - The prompt to validate
 * @param {string[]} models - Array of model names
 * @returns {{valid: boolean, error?: string}} Validation result
 */
export const validatePromptForModels = (prompt, models) => {
  if (!models || models.length === 0) {
    return { valid: false, error: 'No models selected' }
  }
  
  // Find the most restrictive token limit among selected models
  const minTokenLimit = Math.min(
    ...models.map(model => getModelTokenLimit(model))
  )
  
  return validatePrompt(prompt, minTokenLimit)
}

/**
 * Truncate text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength - 3) + '...'
}
