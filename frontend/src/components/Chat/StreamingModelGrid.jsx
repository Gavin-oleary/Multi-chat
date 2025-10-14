import { Loader2 } from 'lucide-react'

const StreamingModelResponse = ({ provider, response }) => {
  const modelConfig = {
    claude: { name: 'Claude', color: 'bg-purple-500' },
    chatgpt: { name: 'ChatGPT', color: 'bg-green-500' },
    gemini: { name: 'Gemini', color: 'bg-blue-500' },
    grok: { name: 'Grok', color: 'bg-gray-700' },
    perplexity: { name: 'Perplexity', color: 'bg-teal-500' },
  }

  const config = modelConfig[provider] || { name: provider, color: 'bg-gray-500' }
  const { content = '', status = 'waiting', error, latency_ms } = response || {}

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${config.color}`} />
          <h3 className="font-medium text-gray-900">{config.name}</h3>
        </div>
        <div className="flex items-center gap-2 text-sm">
          {status === 'thinking' && (
            <span className="text-gray-500 flex items-center gap-1">
              <Loader2 className="w-3 h-3 animate-spin" />
              Thinking...
            </span>
          )}
          {status === 'streaming' && (
            <span className="text-blue-500 flex items-center gap-1">
              <Loader2 className="w-3 h-3 animate-spin" />
              Streaming...
            </span>
          )}
          {status === 'complete' && latency_ms && (
            <span className="text-gray-500">{(latency_ms / 1000).toFixed(1)}s</span>
          )}
          {status === 'error' && (
            <span className="text-red-500">Error</span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {status === 'waiting' && (
          <div className="text-gray-400 text-sm">Waiting to start...</div>
        )}
        
        {(status === 'thinking' || status === 'streaming' || status === 'complete') && content && (
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap text-gray-800">{content}</p>
            {status === 'streaming' && (
              <span className="inline-block w-2 h-4 bg-gray-400 animate-pulse ml-1" />
            )}
          </div>
        )}
        
        {status === 'error' && (
          <div className="text-red-600 text-sm">
            <p className="font-medium">Failed to get response</p>
            <p className="text-red-500 mt-1">{error || 'Unknown error'}</p>
          </div>
        )}
      </div>
    </div>
  )
}

const StreamingModelGrid = ({ responses = {}, selectedModels = [] }) => {
  // Show all selected models, or all models if none selected
  const modelsToShow = selectedModels.length > 0 
    ? selectedModels 
    : ['claude', 'chatgpt', 'gemini', 'grok', 'perplexity']

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {modelsToShow.map((provider) => (
        <StreamingModelResponse
          key={provider}
          provider={provider}
          response={responses[provider]}
        />
      ))}
    </div>
  )
}

export default StreamingModelGrid
