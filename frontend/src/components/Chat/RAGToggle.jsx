import { useState } from 'react';
import { Database, Settings } from 'lucide-react';

export default function RAGToggle({ enabled, onChange, contextCount, onContextCountChange }) {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Database className={`w-5 h-5 ${enabled ? 'text-blue-600' : 'text-gray-400'}`} />
          <div>
            <h3 className="text-sm font-semibold text-gray-900">Knowledge Base</h3>
            <p className="text-xs text-gray-500">
              {enabled ? 'Using document context' : 'Disabled'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="RAG Settings"
          >
            <Settings className="w-4 h-4 text-gray-600" />
          </button>

          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={enabled}
              onChange={(e) => onChange(e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
          </label>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Context Chunks: {contextCount}
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={contextCount}
                onChange={(e) => onContextCountChange(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Less context</span>
                <span>More context</span>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-xs text-blue-800">
                <strong>How it works:</strong> When enabled, the AI will search your uploaded 
                documents for relevant information and use it to provide more accurate answers.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}