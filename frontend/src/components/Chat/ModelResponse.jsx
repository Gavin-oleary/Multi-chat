import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { AlertCircle, Clock } from 'lucide-react'
import Loading from '../common/Loading'

const MODEL_INFO = {
  claude: { name: 'Claude', color: 'claude' },
  chatgpt: { name: 'ChatGPT', color: 'chatgpt' },
  gemini: { name: 'Gemini', color: 'gemini' },
  grok: { name: 'Grok', color: 'grok' },
  perplexity: { name: 'Perplexity', color: 'perplexity' },
}

const ModelResponse = ({ response, isLoading = false }) => {
  const modelInfo = MODEL_INFO[response?.provider] || { name: 'Unknown', color: 'gray' }

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className={`px-4 py-3 border-b border-gray-200 bg-${modelInfo.color}-50`}>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">{modelInfo.name}</h3>
          {response?.latency_ms && (
            <div className="flex items-center gap-1 text-xs text-gray-600">
              <Clock className="w-3 h-3" />
              <span>{Math.round(response.latency_ms)}ms</span>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {isLoading ? (
          <Loading size="sm" text="Generating response..." />
        ) : response?.error ? (
          <div className="flex items-start gap-2 text-red-600">
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Error</p>
              <p className="text-sm text-red-500">{response.error}</p>
            </div>
          </div>
        ) : response?.content ? (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '')
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
              }}
            >
              {response.content}
            </ReactMarkdown>
          </div>
        ) : (
          <p className="text-gray-400 text-sm">No response</p>
        )}
      </div>
    </div>
  )
}

export default ModelResponse