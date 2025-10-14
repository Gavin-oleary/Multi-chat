import { Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import ConversationPage from './pages/ConversationPage'
import ErrorBoundary from './components/common/ErrorBoundary'
import DocumentsPage from './pages/DocumentsPage'
import SystemPromptsPage from './pages/SystemPromptsPage';

function App() {
  return (
    <ErrorBoundary>
      <div className="h-screen w-screen overflow-hidden bg-gray-50">
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/conversation/:id" element={<ConversationPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/system-prompts" element={<SystemPromptsPage />} />
        </Routes>
      </div>
    </ErrorBoundary>
  )
}

export default App