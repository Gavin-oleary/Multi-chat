import { useState } from 'react'
import { MessageSquare, Trash2, Edit2, Check, X } from 'lucide-react'
import { validateTitle, sanitizeString } from '../../utils/validation'

const ConversationItem = ({ 
  conversation, 
  isActive, 
  onClick, 
  onDelete, 
  onRename 
}) => {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(conversation.title)

  const handleSave = () => {
    const validation = validateTitle(editTitle)
    if (!validation.valid) {
      alert(validation.error)
      return
    }
    
    const sanitized = sanitizeString(editTitle, 255)
    if (sanitized && sanitized !== conversation.title) {
      onRename(conversation.id, sanitized)
    }
    setIsEditing(false)
  }

  const handleCancel = () => {
    setEditTitle(conversation.title)
    setIsEditing(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSave()
    } else if (e.key === 'Escape') {
      handleCancel()
    }
  }

  return (
    <div
      className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
        isActive
          ? 'bg-blue-100 text-blue-900'
          : 'hover:bg-gray-100 text-gray-700'
      }`}
      onClick={!isEditing ? onClick : undefined}
    >
      <MessageSquare className="w-4 h-4 flex-shrink-0" />
      
      {isEditing ? (
        <div className="flex-1 flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
          <button
            onClick={handleSave}
            className="p-1 hover:bg-green-100 rounded"
          >
            <Check className="w-4 h-4 text-green-600" />
          </button>
          <button
            onClick={handleCancel}
            className="p-1 hover:bg-red-100 rounded"
          >
            <X className="w-4 h-4 text-red-600" />
          </button>
        </div>
      ) : (
        <>
          <span className="flex-1 text-sm truncate">{conversation.title}</span>
          <div className="hidden group-hover:flex items-center gap-1">
            <button
              onClick={(e) => {
                e.stopPropagation()
                setIsEditing(true)
              }}
              className="p-1 hover:bg-gray-200 rounded"
            >
              <Edit2 className="w-3 h-3" />
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onDelete(conversation.id)
              }}
              className="p-1 hover:bg-red-100 rounded"
            >
              <Trash2 className="w-3 h-3 text-red-600" />
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default ConversationItem