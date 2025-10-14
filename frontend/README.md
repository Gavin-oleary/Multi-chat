# Multi-Model Chat Frontend

React + Vite frontend for the Multi-Model Chat application. Compare responses from Claude, ChatGPT, Gemini, Grok, and Perplexity side-by-side.

## Features

✨ **Multi-Model Comparison** - Send one prompt, get 5 AI responses  
💬 **Conversation Management** - Save and organize your chats  
🎨 **Clean UI** - Tailwind CSS with responsive design  
⚡ **Fast** - Vite for lightning-fast dev experience  
📝 **Markdown Support** - Rich text formatting and code highlighting  

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Zustand** - Lightweight state management
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS
- **React Markdown** - Markdown rendering
- **Lucide React** - Icon library

## Setup

### Prerequisites

- Node.js 18+ and npm
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── Chat/       # Chat-related components
│   │   ├── Sidebar/    # Sidebar components
│   │   └── common/     # Reusable components
│   ├── hooks/          # Custom React hooks
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── store/          # Zustand state stores
│   ├── styles/         # Global styles
│   ├── utils/          # Utility functions
│   ├── App.jsx         # Root component
│   └── main.jsx        # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Components

### Chat Components

- **ChatInput** - Message input with send button
- **MessageBubble** - Individual message display
- **ModelResponse** - Single AI model response card
- **ModelGrid** - Grid layout for all model responses

### Sidebar Components

- **ConversationList** - List of saved conversations
- **ConversationItem** - Individual conversation with edit/delete

### Common Components

- **Button** - Reusable button with variants
- **Loading** - Loading spinner
- **ErrorBoundary** - Error handling wrapper

## State Management

### Stores

**chatStore** - Current conversation state
- Current conversation ID
- Messages in active conversation
- Loading states
- Model responses

**conversationStore** - All conversations
- List of all conversations
- CRUD operations

### Hooks

**useChat** - Chat operations
- Send messages
- Handle responses
- Manage conversation state

**useConversations** - Conversation management
- Load conversations
- Create/update/delete
- Rename conversations

## Environment Variables

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## API Integration

The frontend communicates with the backend via:

- `GET /api/v1/conversations/` - List conversations
- `GET /api/v1/conversations/:id` - Get conversation with messages
- `POST /api/v1/conversations/` - Create conversation
- `PATCH /api/v1/conversations/:id` - Update conversation
- `DELETE /api/v1/conversations/:id` - Delete conversation
- `POST /api/v1/chat/` - Send message to all models

## Styling

Uses Tailwind CSS with custom colors for each AI model:

- Claude: Orange tones
- ChatGPT: Green tones
- Gemini: Blue tones
- Grok: Gray/Black tones
- Perplexity: Teal tones

Custom scrollbar styling is applied throughout.

## Features in Detail

### Conversation Management

- Create new conversations automatically when sending first message
- View conversation history in sidebar
- Rename conversations inline
- Delete conversations with confirmation
- Auto-scroll to latest message

### Message Display

- User messages on the right (blue)
- AI responses in individual cards
- Markdown rendering with syntax highlighting
- Code blocks with proper formatting
- Links open in new tabs

### Model Responses

- All 5 models queried in parallel
- Individual loading states
- Error handling per model
- Response time display
- Grid layout for easy comparison

## Development Tips

### Hot Reload

Vite provides instant hot module replacement. Changes appear immediately without full page reload.

### Component Development

Use the component structure:
```jsx
import { useState } from 'react'
import Button from '../common/Button'

const MyComponent = () => {
  const [state, setState] = useState(null)
  
  return (
    <div>
      <Button onClick={() => setState('clicked')}>
        Click me
      </Button>
    </div>
  )
}
```

### State Access

```javascript
// In a component
import useChatStore from '../store/chatStore'

const MyComponent = () => {
  const { messages, addMessage } = useChatStore()
  // Use state...
}
```

## Troubleshooting

### Port Already in Use

Change port in `vite.config.js`:
```javascript
server: {
  port: 3000, // Change to desired port
}
```

### API Connection Issues

1. Verify backend is running on port 8000
2. Check CORS settings in backend
3. Verify `VITE_API_BASE_URL` in `.env`

### Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

## Production Build

```bash
# Build for production
npm run build

# Files will be in dist/ directory
# Deploy dist/ to your hosting service
```

### Deployment Options

- **Vercel** - `vercel deploy`
- **Netlify** - Drag and drop `dist/` folder
- **GitHub Pages** - Use `gh-pages` package
- **Docker** - See root README for Docker setup

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT