import { useState } from 'react';
import { Search, FileText, Clock, TrendingUp } from 'lucide-react';

export default function SemanticSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setSearched(true);

    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(
        `${API_BASE}/api/v1/documents/search`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: query,
            top_k: 10
          })
        }
      );

      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Search failed');
        setResults([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const highlightQuery = (text, query) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, i) => 
      regex.test(part) ? (
        <mark key={i} className="bg-yellow-200 font-semibold">{part}</mark>
      ) : (
        part
      )
    );
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Semantic Search</h2>
          <p className="text-gray-600">
            Search across all your documents and conversations using AI-powered semantic understanding
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-6">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question or search for information..."
              className="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="mt-3 w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Search Knowledge Base'}
          </button>
        </form>

        {/* Results */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
            <p className="mt-4 text-gray-600">Searching through your knowledge base...</p>
          </div>
        )}

        {!loading && searched && results.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 text-lg">No results found</p>
            <p className="text-gray-500 text-sm mt-2">Try different keywords or upload more documents</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Found {results.length} relevant results
              </h3>
            </div>

            {results.map((result, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow bg-white"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <span className="text-sm font-semibold text-green-600">
                      {(result.similarity_score * 100).toFixed(1)}% Match
                    </span>
                  </div>
                  {result.metadata?.filename && (
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      {result.metadata.filename}
                    </span>
                  )}
                </div>

                <p className="text-gray-800 leading-relaxed mb-3">
                  {highlightQuery(result.chunk_text, query)}
                </p>

                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <div className="flex items-center gap-1">
                    <FileText className="w-3 h-3" />
                    <span>Document #{result.document_id}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>Chunk #{result.chunk_id}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!searched && (
          <div className="text-center py-12 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg">
            <Search className="w-16 h-16 mx-auto text-blue-500 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Powerful Semantic Search
            </h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Unlike traditional keyword search, semantic search understands the meaning 
              and context of your query to find the most relevant information.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}