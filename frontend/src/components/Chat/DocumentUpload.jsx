import { useState } from 'react';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import { documentApi } from '../../services/api';

export default function DocumentUpload({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({});
  const [uploadProgress, setUploadProgress] = useState({});

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
  };

  const uploadFile = async (file, index) => {
    try {
      setUploadStatus(prev => ({ ...prev, [index]: 'uploading' }));
      
      await documentApi.upload(file, (progress) => {
        setUploadProgress(prev => ({ ...prev, [index]: progress }));
      });
      
      setUploadStatus(prev => ({ ...prev, [index]: 'success' }));
      setUploadProgress(prev => ({ ...prev, [index]: 100 }));
      
      if (onUploadComplete) {
        onUploadComplete(file);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Upload failed';
      setUploadStatus(prev => ({ 
        ...prev, 
        [index]: { status: 'error', message: errorMessage }
      }));
    }
  };

  const uploadAllFiles = async () => {
    setUploading(true);
    
    for (let i = 0; i < files.length; i++) {
      const status = uploadStatus[i];
      if (!status || (typeof status === 'object' && status.status === 'error') || status === 'error') {
        await uploadFile(files[i], i);
      }
    }
    
    setUploading(false);
  };

  const getStatusIcon = (status) => {
    const statusValue = typeof status === 'object' ? status.status : status;
    switch (statusValue) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'uploading':
        return <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />;
      default:
        return <File className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Upload className="w-5 h-5 text-blue-600" />
          <h3 className="text-sm font-semibold text-gray-900">Upload Documents</h3>
        </div>
      </div>

      {/* File Input */}
      <div className="mb-4">
        <label className="block w-full">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors cursor-pointer">
            <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <p className="text-sm text-gray-600 mb-1">
              Click to upload or drag and drop
            </p>
            <p className="text-xs text-gray-500">
              TXT, PDF, DOCX, MD, CSV, JSON (Max 10MB)
            </p>
            <input
              type="file"
              multiple
              accept=".txt,.pdf,.doc,.docx,.md,.csv,.json,.log"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
        </label>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-2 mb-4">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div className="flex items-center gap-3 flex-1 min-w-0">
                {getStatusIcon(uploadStatus[index])}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                  {(uploadStatus[index] === 'uploading' || (typeof uploadStatus[index] === 'object' && uploadStatus[index].status === 'uploading')) && (
                    <div className="mt-1 w-full bg-gray-200 rounded-full h-1.5">
                      <div
                        className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress[index] || 0}%` }}
                      />
                    </div>
                  )}
                  {typeof uploadStatus[index] === 'object' && uploadStatus[index].status === 'error' && (
                    <p className="text-xs text-red-600 mt-1">{uploadStatus[index].message}</p>
                  )}
                </div>
              </div>
              
              {uploadStatus[index] !== 'uploading' && !(typeof uploadStatus[index] === 'object' && uploadStatus[index].status === 'uploading') && (
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
      )}

      {/* Upload Button */}
      {files.length > 0 && (
        <div className="flex gap-2">
          <button
            onClick={uploadAllFiles}
            disabled={uploading || files.every((_, i) => {
              const status = uploadStatus[i];
              return status === 'success' || (typeof status === 'object' && status.status === 'success');
            })}
            className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-sm font-medium"
          >
            {uploading ? 'Uploading...' : 'Upload All Documents'}
          </button>
        </div>
      )}

      {/* Success Message */}
      {Object.values(uploadStatus).filter(s => s === 'success' || (typeof s === 'object' && s.status === 'success')).length > 0 && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 font-medium">
            Successfully uploaded {Object.values(uploadStatus).filter(s => s === 'success' || (typeof s === 'object' && s.status === 'success')).length} document(s)!
          </p>
        </div>
      )}
    </div>
  );
}