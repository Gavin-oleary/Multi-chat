import ModelResponse from './ModelResponse'

const ModelGrid = ({ responses, isLoading = false }) => {
  const models = ['claude', 'chatgpt', 'gemini', 'grok', 'perplexity']

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {models.map((provider) => {
        const response = responses?.find((r) => r.provider === provider)
        return (
          <ModelResponse
            key={provider}
            response={response || { provider }}
            isLoading={isLoading && !response}
          />
        )
      })}
    </div>
  )
}

export default ModelGrid