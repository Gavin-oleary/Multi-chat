import { useState, useEffect } from 'react';
import { Save, RotateCcw, Copy, Settings, AlertCircle, CheckCircle } from 'lucide-react';

const MODEL_DISPLAY_NAMES = {
  claude: 'Claude',
  chatgpt: 'ChatGPT',
  gemini: 'Gemini',
  grok: 'Grok',
  perplexity: 'Perplexity'
};

const MODEL_COLORS = {
  claude: 'bg-orange-100 border-orange-300',
  chatgpt: 'bg-green-100 border-green-300',
  gemini: 'bg-blue-100 border-blue-300',
  grok: 'bg-gray-100 border-gray-300',
  perplexity: 'bg-teal-100 border-teal-300'
};

export default function SystemPromptSettings() {
  const [prompts, setPrompts] = useState({});
  const [sharedPrompt, setSharedPrompt] = useState('');
  const [useSharedPrompt, setUseSharedPrompt] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState({});
  const [saveStatus, setSaveStatus] = useState({});
  const [activeTab, setActiveTab] = useState('individual');

  const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/api/v1/system-prompts/`);
      const data = await response.json();
      
      const promptMap = {};
      data.prompts.forEach(prompt => {
        promptMap[prompt.model_provider] = prompt.prompt_template;
      });
      
      setPrompts(promptMap);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load prompts:', error);
      setLoading(false);
    }
  };

  const savePrompt = async (model) => {
    try {
      setSaving(prev => ({ ...prev, [model]: true }));
      setSaveStatus(prev => ({ ...prev, [model]: 'saving' }));

      const response = await fetch(`${API_BASE}/api/v1/system-prompts/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_provider: model,
          name: `${MODEL_DISPLAY_NAMES[model]} Custom`,
          description: 'User customized system prompt',
          prompt_template: prompts[model],
          is_active: true
        })
      });

      if (response.ok) {
        setSaveStatus(prev => ({ ...prev, [model]: 'success' }));
        setTimeout(() => {
          setSaveStatus(prev => ({ ...prev, [model]: null }));
        }, 3000);
      } else {
        throw new Error('Failed to save');
      }
    } catch (error) {
      console.error('Failed to save prompt:', error);
      setSaveStatus(prev => ({ ...prev, [model]: 'error' }));
      setTimeout(() => {
        setSaveStatus(prev => ({ ...prev, [model]: null }));
      }, 3000);
    } finally {
      setSaving(prev => ({ ...prev, [model]: false }));
    }
  };

  const resetPrompt = async (model) => {
    if (!confirm(`Reset ${MODEL_DISPLAY_NAMES[model]} to default prompt?`)) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/v1/system-prompts/initialize-defaults`, {
        method: 'POST'
      });

      if (response.ok) {
        await loadPrompts();
        alert('Prompt reset to default');
      }
    } catch (error) {
      console.error('Failed to reset prompt:', error);
      alert('Failed to reset prompt');
    }
  };

  const copyToAll = (sourceModel) => {
    const sourcePrompt = prompts[sourceModel];
    const newPrompts = {};
    
    Object.keys(MODEL_DISPLAY_NAMES).forEach(model => {
      newPrompts[model] = sourcePrompt;
    });
    
    setPrompts(newPrompts);
  };

  const applySharedToAll = () => {
    const newPrompts = {};
    Object.keys(MODEL_DISPLAY_NAMES).forEach(model => {
      newPrompts[model] = sharedPrompt;
    });
    setPrompts(newPrompts);
  };

  const saveAllPrompts = async () => {
    for (const model of Object.keys(prompts)) {
      await savePrompt(model);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-2">
          <Settings className="w-8 h-8" />
          System Prompt Settings
        </h1>
        <p className="text-gray-600">
          Configure how each AI model should behave and respond to queries.
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('individual')}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${
              activeTab === 'individual'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Individual Models
          </button>
          <button
            onClick={() => setActiveTab('shared')}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${
              activeTab === 'shared'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Shared Prompt (Apply to All)
          </button>
        </div>
      </div>

      {/* Individual Model Prompts */}
      {activeTab === 'individual' && (
        <div className="space-y-6">
          {Object.entries(MODEL_DISPLAY_NAMES).map(([model, displayName]) => (
            <div key={model} className={`border-2 rounded-lg p-6 ${MODEL_COLORS[model]}`}>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">{displayName}</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => copyToAll(model)}
                    className="px-3 py-1.5 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 flex items-center gap-1"
                    title="Copy this prompt to all models"
                  >
                    <Copy className="w-4 h-4" />
                    Copy to All
                  </button>
                  <button
                    onClick={() => resetPrompt(model)}
                    className="px-3 py-1.5 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 flex items-center gap-1"
                  >
                    <RotateCcw className="w-4 h-4" />
                    Reset
                  </button>
                  <button
                    onClick={() => savePrompt(model)}
                    disabled={saving[model]}
                    className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 flex items-center gap-1"
                  >
                    {saving[model] ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Saving...
                      </>
                    ) : saveStatus[model] === 'success' ? (
                      <>
                        <CheckCircle className="w-4 h-4" />
                        Saved!
                      </>
                    ) : saveStatus[model] === 'error' ? (
                      <>
                        <AlertCircle className="w-4 h-4" />
                        Error
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4" />
                        Save
                      </>
                    )}
                  </button>
                </div>
              </div>
              
              <textarea
                value={prompts[model] || ''}
                onChange={(e) => setPrompts(prev => ({ ...prev, [model]: e.target.value }))}
                className="w-full h-48 p-4 border border-gray-300 rounded-lg font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder={`Enter system prompt for ${displayName}...`}
              />
              
              <p className="mt-2 text-xs text-gray-600">
                Use <code className="bg-white px-1 rounded">{'{rag_context}'}</code> as a placeholder for document context when RAG is enabled.
              </p>
            </div>
          ))}

          <div className="flex justify-end">
            <button
              onClick={saveAllPrompts}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium flex items-center gap-2"
            >
              <Save className="w-5 h-5" />
              Save All Prompts
            </button>
          </div>
        </div>
      )}

      {/* Shared Prompt */}
      {activeTab === 'shared' && (
        <div className="space-y-6">
          <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Shared System Prompt</h2>
            <p className="text-sm text-gray-600 mb-4">
              Create a prompt that will be applied to all AI models. This is useful when you want consistent behavior across all models.
            </p>
            
            <textarea
              value={sharedPrompt}
              onChange={(e) => setSharedPrompt(e.target.value)}
              className="w-full h-64 p-4 border border-gray-300 rounded-lg font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter a shared prompt that will apply to all models..."
            />
            
            <div className="mt-4 flex justify-end gap-3">
              <button
                onClick={() => setSharedPrompt('')}
                className="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-50"
              >
                Clear
              </button>
              <button
                onClick={applySharedToAll}
                className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium"
              >
                Apply to All Models
              </button>
            </div>
            
            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-yellow-800">
                After applying the shared prompt to all models, remember to click "Save All Prompts" in the Individual Models tab to persist the changes.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}