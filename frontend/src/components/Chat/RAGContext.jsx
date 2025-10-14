import { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, Database } from 'lucide-react';

const RAGContext = ({ contextChunks, ragContextUsed }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!ragContextUsed || !contextChunks || contextChunks.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg">
      <div 
        className="p-4 cursor-pointer flex items-center justify-between"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-blue-600" />
          <span className="font-medium text-blue-900">
            Knowledge Base Context Used ({contextChunks.length} chunks)
          </span>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-blue-600" />
        ) : (
          <ChevronDown className="w-5 h-5 text-blue-600" />
        )}
      </div>
      
      {isExpanded && (
        <div className="px-4 pb-4 space-y-3">
          {contextChunks.map((chunk, index) => (
            <div key={chunk.chunk_id || index} className="bg-white p-3 rounded border border-blue-100">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">
                    Context {index + 1}
                  </span>
                </div>
                <span className="text-xs text-gray-500">
                  Similarity: {(chunk.similarity * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-sm text-gray-600 whitespace-pre-wrap">
                {chunk.text}
              </p>
              {chunk.metadata?.filename && (
                <p className="text-xs text-gray-400 mt-2">
                  Source: {chunk.metadata.filename}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RAGContext;
