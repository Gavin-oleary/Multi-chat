import { useState } from 'react';
import { Upload, File, X, Check, AlertCircle, Loader } from 'lucide-react';

export default function DocumentUpload({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({});
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  };

  const handleFileInput = (e) => {
    const selectedFiles = Array.from(e.target.files);
    handleFiles(selectedFiles);
  };

  const handleFiles = (newFiles) => {
    const textFiles = newFiles.filter(file => 
      file.type.startsWith('text/') || 
      file.name.endsWith('.txt') ||
      file.name.endsWith('.md') ||
      file.name.endsWith('.json')
    );
    
    setFiles(prev => [...prev, ...textFiles]);
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
    setUploadStatus(prev => {
      const newStatus = { ...prev };
      delete newStatus[index];
      return newStatus;
    });
  };

  const uploadFiles = async () => {
    setUploading(true);
    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const formData = new FormData();
      formData.append('file', file);

      try {
        setUploadStatus(prev => ({ ...prev, [i]: 'uploading' }));

        const response = await fetch(`${API_BASE}/api/v1/documents/upload`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          setUploadStatus(prev => ({ ...prev, [i]: 'success' }));
        } else {
          setUploadStatus(prev => ({ ...prev, [i]: 'error' }));
        }
      } catch (error) {
        console.error('Upload error:', error);
        setUploadStatus(prev => ({ ...prev, [i]: 'error' }));
      }
    }

    setUploading(false);
    
    if (onUploadComplete) {
      onUploadComplete();
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'uploading':
        return <Loader className="w-4 h-4 animate-spin text-blue-500" />;
      case 'success':
        return <Check className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <File className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Upload Documents</h2>
      
      {/* Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <p className="text-lg mb-2 text-gray-700">
          Drag and drop files here, or click to select
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Supports: .txt, .md, .json and other text files
        </p>
        <input
          type="file"
          multiple
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
          accept=".txt,.md,.json,text/*"
        />
        <label
          htmlFor="file-upload"
          className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors"
        >
          Select Files
        </label>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">
            Selected Files ({files.length})
          </h3>
          <div className="space-y-2">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-center gap-3 flex-1">
                  {getStatusIcon(uploadStatus[index])}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                {!uploading && !uploadStatus[index] && (
                  <button
                    onClick={() => removeFile(index)}
                    className="p-1 hover:bg-gray-200 rounded transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Upload Button */}
          <button
            onClick={uploadFiles}
            disabled={uploading || files.length === 0}
            className="w-full mt-4 px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload All Documents'}
          </button>
        </div>
      )}

      {/* Success Message */}
      {Object.values(uploadStatus).filter(s => s === 'success').length > 0 && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 font-medium">
            Successfully uploaded {Object.values(uploadStatus).filter(s => s === 'success').length} document(s)!
          </p>
        </div>
      )}
    </div>
  );
}