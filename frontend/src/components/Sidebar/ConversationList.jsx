import { Plus, Settings, FileText } from 'lucide-react'
import ConversationItem from './ConversationItem'
import Loading from '../common/Loading'
import Button from '../common/Button'
import useConversations from '../../hooks/useConversations'
import useChatStore from '../../store/chatStore'
import { useNavigate, useLocation } from 'react-router-dom'

const ConversationList = ({ onNewChat }) => {
  const { conversations, isLoading, renameConversation, removeConversation } = useConversations()
  const { currentConversationId } = useChatStore()
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <Button
          onClick={onNewChat}
          variant="primary"
          className="w-full flex items-center justify-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </Button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-2">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loading size="sm" text="Loading conversations..." />
          </div>
        ) : conversations.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs mt-1">Start a new chat to begin</p>
          </div>
        ) : (
          <div className="space-y-1">
            {conversations.map((conversation) => (
              <ConversationItem
                key={conversation.id}
                conversation={conversation}
                isActive={conversation.id === currentConversationId}
                onClick={() => navigate(`/conversation/${conversation.id}`)}
                onDelete={removeConversation}
                onRename={renameConversation}
              />
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200">
        <div className="p-2 space-y-1">
          <button
            onClick={() => navigate('/documents')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              location.pathname === '/documents'
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span className="text-sm font-medium">Documents</span>
          </button>
          <button
            onClick={() => navigate('/system-prompts')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              location.pathname === '/system-prompts'
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <Settings className="w-4 h-4" />
            <span className="text-sm font-medium">System Prompts</span>
          </button>
        </div>
        <div className="p-4 text-xs text-gray-500">
          <p className="font-medium">Multi-Model Chat</p>
          <p>Compare AI responses</p>
        </div>
      </div>
    </div>
  )
}

export default ConversationList