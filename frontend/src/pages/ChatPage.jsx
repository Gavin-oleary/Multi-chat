import { useEffect, useRef, useState } from 'react'
import ConversationList from '../components/Sidebar/ConversationList'
import ChatInput from '../components/Chat/ChatInput'
import MessageBubble from '../components/Chat/MessageBubble'
import ModelGrid from '../components/Chat/ModelGrid'
import StreamingModelGrid from '../components/Chat/StreamingModelGrid'
import ModelSelector from '../components/Chat/ModelSelector'
import RAGToggle from '../components/Chat/RAGToggle'  // NEW: Import RAG toggle
import RAGContext from '../components/Chat/RAGContext'  // Import RAG context display
import useChat from '../hooks/useChat'
import useStreamingChat from '../hooks/useStreamingChat'
import useChatStore from '../store/chatStore'
import DocumentUpload from '../components/Chat/DocumentUpload'

const ChatPage = () => {
  const { sendMessage } = useChat()
  const { sendStreamingMessage, streamingResponses, isConnected, connect } = useStreamingChat()
  const { 
    messages, 
    currentResponses, 
    isSending,
    reset,
    ragContextUsed,
    contextChunks,
  } = useChatStore()
  
  // State for selected models and streaming preference
  const [selectedModels, setSelectedModels] = useState(['claude', 'chatgpt', 'gemini', 'grok', 'perplexity'])
  const [useStreaming, setUseStreaming] = useState(true)
  
  // RAG state
  const [ragEnabled, setRagEnabled] = useState(false)
  const [contextCount, setContextCount] = useState(3)

  const messagesEndRef = useRef(null)

  // Document upload panel
  const [showUpload, setShowUpload] = useState(false)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentResponses, streamingResponses])
  
  // Connect to WebSocket on mount if streaming is enabled
  useEffect(() => {
    if (useStreaming && !isConnected) {
      connect()
    }
  }, [useStreaming, isConnected, connect])

  const handleSendMessage = async (prompt) => {
    if (selectedModels.length === 0) {
      alert('Please select at least one model before sending a message.')
      return
    }
    
    try {
      if (useStreaming) {
        // Note: Streaming doesn't support RAG yet, you may need to add this feature
        await sendStreamingMessage(prompt, selectedModels)
      } else {
        // MODIFIED: Pass RAG options to sendMessage
        await sendMessage(prompt, selectedModels, ragEnabled, contextCount)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      alert('Failed to send message. Please try again.')
    }
  }

  const handleNewChat = () => {
    reset()
  }

  return (
    <div className="flex h-screen">
      <ConversationList onNewChat={handleNewChat} />
      
      <div className="flex-1 flex flex-col">
        {/* Model Selector */}
        <ModelSelector 
          selectedModels={selectedModels} 
          onModelsChange={setSelectedModels} 
        />
        

        <div className="px-4 py-3 bg-white border-b border-gray-200">
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            {showUpload ? 'Hide' : 'Show'} Document Upload
          </button>
  
          {showUpload && (
            <div className="mt-3">
              <DocumentUpload onUploadComplete={() => console.log('Upload complete')} />
            </div>
          )}
      </div>

        {/*RAG Toggle Component */}
        <div className="px-4 py-3 bg-white border-b border-gray-200">
          <RAGToggle 
            enabled={ragEnabled}
            onChange={setRagEnabled}
            contextCount={contextCount}
            onContextCountChange={setContextCount}
          />
        </div>
        
        {/* Streaming Toggle */}
        <div className="px-4 py-2 bg-gray-50 border-b border-gray-200">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={useStreaming}
              onChange={(e) => setUseStreaming(e.target.checked)}
              className="rounded text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">Enable streaming responses</span>
            {useStreaming && (
              <span className={`text-xs ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
                ({isConnected ? 'Connected' : 'Disconnected'})
              </span>
            )}
          </label>
        </div>
        
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto scrollbar-thin bg-gray-50">
          <div className="max-w-6xl mx-auto px-4 py-6">
            {messages.length === 0 && currentResponses.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Multi-Model Chat
                  </h1>
                  <p className="text-xl text-gray-600 mb-8">
                    Select AI models above and ask your question
                  </p>
                  <div className="grid grid-cols-5 gap-4 max-w-2xl mx-auto">
                    {['Claude', 'ChatGPT', 'Gemini', 'Grok', 'Perplexity'].map((model) => (
                      <div
                        key={model}
                        className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm"
                      >
                        <p className="font-medium text-sm text-gray-900">{model}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-8">
                {/* Display conversation messages */}
                {messages.map((message, index) => (
                  <div key={index}>
                    <MessageBubble message={message} />
                  </div>
                ))}

                {/* Display RAG Context if used */}
                {ragContextUsed && contextChunks && (
                  <RAGContext 
                    ragContextUsed={ragContextUsed}
                    contextChunks={contextChunks}
                  />
                )}

                {/* Display current model responses */}
                {(currentResponses.length > 0 || Object.keys(streamingResponses).length > 0) && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Model Responses
                    </h3>
                    {useStreaming && Object.keys(streamingResponses).length > 0 ? (
                      <StreamingModelGrid 
                        responses={streamingResponses} 
                        selectedModels={selectedModels}
                      />
                    ) : (
                      <ModelGrid responses={currentResponses} isLoading={isSending} />
                    )}
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <ChatInput onSend={handleSendMessage} disabled={isSending} />
      </div>
    </div>
  )
}

export default ChatPage