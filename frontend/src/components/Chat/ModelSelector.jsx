import { useState, useEffect } from 'react'
import { Check, AlertCircle, RefreshCw } from 'lucide-react'
import { providerApi } from '../../services/api'

const MODEL_INFO = {
  'claude': { name: 'Claude', color: 'bg-purple-500' },
  'chatgpt': { name: 'ChatGPT', color: 'bg-green-500' },
  'gemini': { name: 'Gemini', color: 'bg-blue-500' },
  'grok': { name: 'Grok', color: 'bg-gray-700' },
  'perplexity': { name: 'Perplexity', color: 'bg-teal-500' }
}

const ModelSelector = ({ selectedModels, onModelsChange }) => {
  const [providerHealth, setProviderHealth] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  // Fetch provider health status
  const fetchProviderHealth = async () => {
    try {
      setIsLoading(true)
      const response = await providerApi.getHealth()
      setProviderHealth(response.data)
    } catch (error) {
      console.error('Failed to fetch provider health:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchProviderHealth()
    // Refresh health status every 30 seconds
    const interval = setInterval(fetchProviderHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  const handleModelToggle = (model) => {
    if (selectedModels.includes(model)) {
      onModelsChange(selectedModels.filter(m => m !== model))
    } else {
      onModelsChange([...selectedModels, model])
    }
  }

  const handleSelectAll = () => {
    const availableModels = Object.keys(MODEL_INFO).filter(
      model => providerHealth[model]?.is_available !== false
    )
    onModelsChange(availableModels)
  }

  const handleSelectNone = () => {
    onModelsChange([])
  }

  return (
    <div className="border-b border-gray-200 bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-700">Select AI Models</h3>
          <div className="flex gap-2">
            <button
              onClick={handleSelectAll}
              className="text-xs text-blue-600 hover:text-blue-800"
            >
              Select All
            </button>
            <span className="text-gray-400">|</span>
            <button
              onClick={handleSelectNone}
              className="text-xs text-blue-600 hover:text-blue-800"
            >
              Clear
            </button>
            <span className="text-gray-400">|</span>
            <button
              onClick={fetchProviderHealth}
              className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
              disabled={isLoading}
            >
              <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
          {Object.entries(MODEL_INFO).map(([modelKey, modelInfo]) => {
            const health = providerHealth[modelKey]
            const isAvailable = health?.is_available !== false
            const isSelected = selectedModels.includes(modelKey)
            const status = health?.status || 'unknown'

            return (
              <label
                key={modelKey}
                className={`
                  flex items-center gap-2 p-2 rounded-lg border cursor-pointer
                  transition-all duration-200
                  ${isSelected 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-300 bg-white hover:border-gray-400'
                  }
                  ${!isAvailable ? 'opacity-50 cursor-not-allowed' : ''}
                `}
              >
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => handleModelToggle(modelKey)}
                  disabled={!isAvailable}
                  className="sr-only"
                />
                
                <div className="flex items-center gap-2 flex-1">
                  <div className={`w-2 h-2 rounded-full ${modelInfo.color}`} />
                  <span className="text-sm font-medium">{modelInfo.name}</span>
                </div>

                {/* Status indicator */}
                <div className="flex items-center">
                  {status === 'closed' && isAvailable && (
                    <Check className="w-4 h-4 text-green-500" />
                  )}
                  {status === 'open' && (
                    <AlertCircle className="w-4 h-4 text-red-500" />
                  )}
                  {status === 'half_open' && (
                    <AlertCircle className="w-4 h-4 text-yellow-500" />
                  )}
                </div>
              </label>
            )
          })}
        </div>

        {/* Status legend */}
        <div className="flex items-center gap-4 mt-3 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <Check className="w-3 h-3 text-green-500" />
            <span>Available</span>
          </div>
          <div className="flex items-center gap-1">
            <AlertCircle className="w-3 h-3 text-yellow-500" />
            <span>Testing</span>
          </div>
          <div className="flex items-center gap-1">
            <AlertCircle className="w-3 h-3 text-red-500" />
            <span>Unavailable</span>
          </div>
        </div>

        {selectedModels.length === 0 && (
          <p className="text-sm text-amber-600 mt-2">
            Please select at least one model to send your message to.
          </p>
        )}
      </div>
    </div>
  )
}

export default ModelSelector
