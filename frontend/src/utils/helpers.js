/**
 * Format a date string to a readable format
 */
export const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInMs = now - date
    const diffInMinutes = Math.floor(diffInMs / 60000)
    const diffInHours = Math.floor(diffInMinutes / 60)
    const diffInDays = Math.floor(diffInHours / 24)
  
    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInHours < 24) return `${diffInHours}h ago`
    if (diffInDays < 7) return `${diffInDays}d ago`
    
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
    })
  }
  
  /**
   * Truncate text to a maximum length
   */
  export const truncate = (text, maxLength = 50) => {
    if (text.length <= maxLength) return text
    return text.slice(0, maxLength) + '...'
  }
  
  /**
   * Copy text to clipboard
   */
  export const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      return true
    } catch (err) {
      console.error('Failed to copy:', err)
      return false
    }
  }
  
  /**
   * Get model color based on provider
   */
  export const getModelColor = (provider) => {
    const colors = {
      claude: 'bg-orange-100 text-orange-800 border-orange-200',
      chatgpt: 'bg-green-100 text-green-800 border-green-200',
      gemini: 'bg-blue-100 text-blue-800 border-blue-200',
      grok: 'bg-gray-100 text-gray-800 border-gray-200',
      perplexity: 'bg-teal-100 text-teal-800 border-teal-200',
    }
    return colors[provider] || 'bg-gray-100 text-gray-800 border-gray-200'
  }
  
  /**
   * Debounce function
   */
  export const debounce = (func, wait) => {
    let timeout
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout)
        func(...args)
      }
      clearTimeout(timeout)
      timeout = setTimeout(later, wait)
    }
  }
  
  /**
   * Check if code block
   */
  export const isCodeBlock = (text) => {
    return text.includes('```')
  }
  
  /**
   * Extract code from markdown code blocks
   */
  export const extractCode = (text) => {
    const codeBlockRegex = /```[\w]*\n([\s\S]*?)```/g
    const matches = []
    let match
  
    while ((match = codeBlockRegex.exec(text)) !== null) {
      matches.push(match[1])
    }
  
    return matches
  }