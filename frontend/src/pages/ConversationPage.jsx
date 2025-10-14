import { useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import ConversationList from '../components/Sidebar/ConversationList'
import ChatInput from '../components/Chat/ChatInput'
import MessageBubble from '../components/Chat/MessageBubble'
import ModelGrid from '../components/Chat/ModelGrid'
import Loading from '../components/common/Loading'
import Button from '../components/common/Button'
import useChat from '../hooks/useChat'
import useConversations from '../hooks/useConversations'
import useChatStore from '../store/chatStore'

const ConversationPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { loadConversation } = useConversations()
  const { sendMessage } = useChat()
  const { 
    messages, 
    currentResponses, 
    isSending, 
    isLoading,
    reset,
  } = useChatStore()

  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentResponses])

  useEffect(() => {
    const load = async () => {
      try {
        await loadConversation(parseInt(id))
      } catch (error) {
        console.error('Failed to load conversation:', error)
        alert('Failed to load conversation')
        navigate('/')
      }
    }
    
    load()
  }, [id, loadConversation, navigate])

  const handleSendMessage = async (prompt) => {
    try {
      await sendMessage(prompt)
    } catch (error) {
      console.error('Failed to send message:', error)
      alert('Failed to send message. Please try again.')
    }
  }

  const handleNewChat = () => {
    reset()
    navigate('/')
  }

  // Group messages by user prompts and their corresponding model responses
  const groupedMessages = []
  let currentGroup = null

  messages.forEach((msg) => {
    if (msg.role === 'user') {
      if (currentGroup) {
        groupedMessages.push(currentGroup)
      }
      currentGroup = {
        userMessage: msg,
        modelResponses: [],
      }
    } else if (msg.role === 'assistant' && currentGroup) {
      currentGroup.modelResponses.push(msg)
    }
  })

  if (currentGroup) {
    groupedMessages.push(currentGroup)
  }

  return (
    <div className="flex h-screen">
      <ConversationList onNewChat={handleNewChat} />
      
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-gray-200 bg-white px-4 py-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to New Chat
          </Button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto scrollbar-thin bg-gray-50">
          {isLoading ? (
            <div className="flex items-center justify-center h-full">
              <Loading size="lg" text="Loading conversation..." />
            </div>
          ) : (
            <div className="max-w-6xl mx-auto px-4 py-6">
              <div className="space-y-8">
                {groupedMessages.map((group, index) => (
                  <div key={index} className="space-y-4">
                    {/* User message */}
                    <MessageBubble message={group.userMessage} />
                    
                    {/* Model responses */}
                    {group.modelResponses.length > 0 && (
                      <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-gray-900">
                          Model Responses
                        </h3>
                        <ModelGrid
                          responses={group.modelResponses.map((msg) => ({
                            provider: msg.model_provider,
                            content: msg.content,
                          }))}
                        />
                      </div>
                    )}
                  </div>
                ))}

                {/* Current responses being generated */}
                {currentResponses.length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Model Responses
                    </h3>
                    <ModelGrid responses={currentResponses} isLoading={isSending} />
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <ChatInput onSend={handleSendMessage} disabled={isSending || isLoading} />
      </div>
    </div>
  )
}

export default ConversationPage