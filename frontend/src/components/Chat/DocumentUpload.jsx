import { useState } from 'react';
import { Upload, File, X, CheckCircle, AlertCircle, Loader, Clock } from 'lucide-react';
import { documentApi } from '../../services/api';

export default function DocumentUpload({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({});
  const [uploadProgress, setUploadProgress] = useState({});
  const [uploadMessages, setUploadMessages] = useState({});

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(prev => [...prev, ...selectedFiles]);
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
    setUploadStatus(prev => {
      const newStatus = { ...prev };
      delete newStatus[index];
      return newStatus;
    });
    setUploadMessages(prev => {
      const newMessages = { ...prev };
      delete newMessages[index];
      return newMessages;
    });
  };

  const uploadFile = async (file, index) => {
    try {
      setUploadStatus(prev => ({ ...prev, [index]: 'uploading' }));
      setUploadMessages(prev => ({ 
        ...prev, 
        [index]: file.name.endsWith('.pdf') ? 'Extracting text from PDF...' : 'Processing file...'
      }));
      
      // Simulate initial progress
      setUploadProgress(prev => ({ ...prev, [index]: 10 }));
      
      await documentApi.upload(file, (progress) => {
        setUploadProgress(prev => ({ ...prev, [index]: progress }));
        
        // Update message based on progress
        if (progress < 50) {
          setUploadMessages(prev => ({ 
            ...prev, 
            [index]: 'Uploading...'
          }));
        } else if (progress < 90) {
          setUploadMessages(prev => ({ 
            ...prev, 
            [index]: 'Processing text...'
          }));
        } else {
          setUploadMessages(prev => ({ 
            ...prev, 
            [index]: 'Creating embeddings...'
          }));
        }
      });
      
      setUploadStatus(prev => ({ ...prev, [index]: 'success' }));
      setUploadProgress(prev => ({ ...prev, [index]: 100 }));
      setUploadMessages(prev => ({ 
        ...prev, 
        [index]: 'Upload complete!'
      }));
      
      if (onUploadComplete) {
        onUploadComplete(file);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Upload failed';
      setUploadStatus(prev => ({ 
        ...prev, 
        [index]: 'error'
      }));
      setUploadMessages(prev => ({ 
        ...prev, 
        [index]: errorMessage
      }));
    }
  };

  const uploadAllFiles = async () => {
    setUploading(true);
    
    for (let i = 0; i < files.length; i++) {
      const status = uploadStatus[i];
      if (!status || status === 'error') {
        await uploadFile(files[i], i);
      }
    }
    
    setUploading(false);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'uploading':
        return <Loader className="w-4 h-4 animate-spin text-blue-500" />;
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <File className="w-4 h-4 text-gray-400" />;
    }
  };

  const getEstimatedTime = (fileSize) => {
    // Rough estimation: 1MB takes about 5 seconds
    const sizeMB = fileSize / (1024 * 1024);
    const estimatedSeconds = Math.ceil(sizeMB * 5);
    return estimatedSeconds > 60 
      ? `~${Math.ceil(estimatedSeconds / 60)} min` 
      : `~${estimatedSeconds} sec`;
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Upload Documents</h2>
      
      {/* Drop Zone */}
      <div className="border-2 border-dashed rounded-lg p-8 text-center transition-colors border-gray-300 hover:border-gray-400">
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <p className="text-lg mb-2 text-gray-700">
          Drag and drop files here, or click to select
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Supports: TXT, PDF, DOCX, MD, CSV, JSON (Max 10MB)
        </p>
        <input
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
          accept=".txt,.pdf,.doc,.docx,.md,.csv,.json,.log"
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
                className="p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3 flex-1">
                    {getStatusIcon(uploadStatus[index])}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.name}
                      </p>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>{(file.size / 1024).toFixed(2)} KB</span>
                        {!uploadStatus[index] && file.size > 1024 * 1024 && (
                          <>
                            <span>•</span>
                            <Clock className="w-3 h-3 inline" />
                            <span>{getEstimatedTime(file.size)}</span>
                          </>
                        )}
                      </div>
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
                
                {/* Progress Bar */}
                {uploadStatus[index] === 'uploading' && uploadProgress[index] !== undefined && (
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress[index]}%` }}
                      />
                    </div>
                  </div>
                )}
                
                {/* Status Message */}
                {uploadMessages[index] && (
                  <p className={`text-xs mt-2 ${
                    uploadStatus[index] === 'error' ? 'text-red-600' :
                    uploadStatus[index] === 'success' ? 'text-green-600' :
                    'text-blue-600'
                  }`}>
                    {uploadMessages[index]}
                  </p>
                )}
              </div>
            ))}
          </div>

          {/* Upload Button */}
          <button
            onClick={uploadAllFiles}
            disabled={uploading || files.length === 0}
            className="w-full mt-4 px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                <span>Upload {files.length} {files.length === 1 ? 'File' : 'Files'}</span>
              </>
            )}
          </button>
          
          {/* Info Note */}
          {files.some(f => f.size > 1024 * 1024) && (
            <p className="text-xs text-gray-500 mt-2 text-center">
              Large files may take longer to process. Please be patient.
            </p>
          )}
        </div>
      )}
    </div>
  );
}