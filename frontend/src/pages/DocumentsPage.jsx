// frontend/src/pages/DocumentsPage.jsx
import DocumentUpload from '../components/Document/DocumentUpload';
import SemanticSearch from '../components/Document/SemanticSearch';

export default function DocumentsPage() {
  return (
    <div className="container mx-auto py-8">
      <DocumentUpload />
      <div className="mt-8">
        <SemanticSearch />
      </div>
    </div>
  );
}