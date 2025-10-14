import { useState } from 'react'
import { Send, AlertCircle } from 'lucide-react'
import Button from '../common/Button'
import { validatePrompt, sanitizeString } from '../../utils/validation'

const ChatInput = ({ onSend, disabled = false, selectedModels = [] }) => {
  const [input, setInput] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (disabled) return
    
    // Validate input
    const validation = validatePrompt(input)
    if (!validation.valid) {
      setError(validation.error)
      return
    }
    
    // Clear error and send
    setError('')
    const sanitized = sanitizeString(input, 10000)
    onSend(sanitized)
    setInput('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-2 items-end max-w-4xl mx-auto">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => {
              setInput(e.target.value)
              // Clear error when user types
              if (error) setError('')
            }}
            onKeyDown={handleKeyDown}
            placeholder="Ask all models a question..."
            disabled={disabled}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            rows="3"
          />
        </div>
        <Button
          type="submit"
          disabled={disabled || !input.trim()}
          className="flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          Send
        </Button>
      </div>
      {error && (
        <div className="flex items-center gap-2 mt-2 text-sm text-red-600 justify-center">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}
      <p className="text-xs text-gray-500 mt-2 text-center">
        Press Enter to send, Shift+Enter for new line
      </p>
    </form>
  )
}

export default ChatInput