import { useState, useEffect } from 'react';
import { Settings, Save, RotateCcw, AlertCircle, Check } from 'lucide-react';
import { systemPromptsApi } from '../services/api';

const MODEL_INFO = {
  'claude': { name: 'Claude', color: 'bg-purple-500' },
  'chatgpt': { name: 'ChatGPT', color: 'bg-green-500' },
  'gemini': { name: 'Gemini', color: 'bg-blue-500' },
  'grok': { name: 'Grok', color: 'bg-gray-700' },
  'perplexity': { name: 'Perplexity', color: 'bg-teal-500' }
};

const SystemPromptsPage = () => {
  const [prompts, setPrompts] = useState([]);
  const [selectedModel, setSelectedModel] = useState('claude');
  const [currentPrompt, setCurrentPrompt] = useState(null);
  const [editedPrompt, setEditedPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  // Load all system prompts
  const loadPrompts = async () => {
    try {
      setLoading(true);
      const response = await systemPromptsApi.list();
      setPrompts(response.prompts);
      
      // Select the first model's prompt
      if (response.prompts.length > 0) {
        const prompt = response.prompts.find(p => p.model_provider === selectedModel);
        if (prompt) {
          setCurrentPrompt(prompt);
          setEditedPrompt(prompt.prompt_template);
        }
      }
    } catch (error) {
      console.error('Failed to load system prompts:', error);
      showMessage('Failed to load system prompts', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Load prompts on mount
  useEffect(() => {
    loadPrompts();
  }, []);

  // Update current prompt when model selection changes
  useEffect(() => {
    const prompt = prompts.find(p => p.model_provider === selectedModel);
    if (prompt) {
      setCurrentPrompt(prompt);
      setEditedPrompt(prompt.prompt_template);
    }
  }, [selectedModel, prompts]);

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleSave = async () => {
    if (!currentPrompt) return;

    try {
      setSaving(true);
      await systemPromptsApi.update(currentPrompt.id, {
        prompt_template: editedPrompt
      });
      
      // Reload prompts
      await loadPrompts();
      showMessage('System prompt saved successfully!');
    } catch (error) {
      console.error('Failed to save system prompt:', error);
      showMessage('Failed to save system prompt', 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    if (currentPrompt) {
      setEditedPrompt(currentPrompt.prompt_template);
    }
  };

  const handleInitializeDefaults = async () => {
    try {
      setSaving(true);
      await systemPromptsApi.initializeDefaults();
      await loadPrompts();
      showMessage('Default prompts initialized successfully!');
    } catch (error) {
      console.error('Failed to initialize defaults:', error);
      showMessage('Failed to initialize defaults', 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Settings className="w-6 h-6 text-gray-600" />
            <h1 className="text-2xl font-bold text-gray-900">System Prompts Configuration</h1>
          </div>
          <button
            onClick={handleInitializeDefaults}
            className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            disabled={saving}
          >
            Initialize Defaults
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Model Selector Sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-3">Select Model</h2>
          <div className="space-y-2">
            {Object.entries(MODEL_INFO).map(([key, info]) => (
              <button
                key={key}
                onClick={() => setSelectedModel(key)}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${
                  selectedModel === key
                    ? 'bg-blue-50 border border-blue-200'
                    : 'hover:bg-gray-50 border border-gray-200'
                }`}
              >
                <div className={`w-3 h-3 rounded-full ${info.color}`} />
                <span className="font-medium">{info.name}</span>
              </button>
            ))}
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-xs text-blue-800">
              <strong>Tip:</strong> Use <code className="bg-blue-100 px-1 rounded">{'{rag_context}'}</code> 
              in your prompt to include retrieved context from the knowledge base.
            </p>
          </div>
        </div>

        {/* Editor Area */}
        <div className="flex-1 p-6">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Loading system prompts...</p>
              </div>
            </div>
          ) : currentPrompt ? (
            <div className="h-full flex flex-col">
              <div className="mb-4">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  {currentPrompt.name}
                </h2>
                {currentPrompt.description && (
                  <p className="text-gray-600">{currentPrompt.description}</p>
                )}
              </div>

              <div className="flex-1 flex flex-col">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  System Prompt Template
                </label>
                <textarea
                  value={editedPrompt}
                  onChange={(e) => setEditedPrompt(e.target.value)}
                  className="flex-1 w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  placeholder="Enter system prompt template..."
                />
              </div>

              <div className="flex items-center justify-between mt-6">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="includeRag"
                    checked={currentPrompt.include_rag_context}
                    className="rounded text-blue-600"
                    disabled
                  />
                  <label htmlFor="includeRag" className="text-sm text-gray-700">
                    Include RAG context when available
                  </label>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={handleReset}
                    className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2"
                    disabled={editedPrompt === currentPrompt.prompt_template}
                  >
                    <RotateCcw className="w-4 h-4" />
                    Reset
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:bg-blue-300"
                    disabled={saving || editedPrompt === currentPrompt.prompt_template}
                  >
                    <Save className="w-4 h-4" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No system prompt found for this model.</p>
                <button
                  onClick={handleInitializeDefaults}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Initialize Default Prompts
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Success/Error Message */}
      {message && (
        <div className={`fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 ${
          message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {message.type === 'success' ? (
            <Check className="w-5 h-5" />
          ) : (
            <AlertCircle className="w-5 h-5" />
          )}
          <span>{message.text}</span>
        </div>
      )}
    </div>
  );
};

export default SystemPromptsPage;
