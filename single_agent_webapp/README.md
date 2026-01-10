# LLM-for-SE Web Application

A ChatGPT-like web interface for the LLM-for-SE code generation agent. Built with FastAPI (Python) backend and Next.js (TypeScript) frontend.

## 🚀 Features

- **Real-time Streaming**: Watch the agent work through its cognitive steps in real-time
- **ChatGPT-like Interface**: Intuitive chat interface for interacting with the agent
- **Code Generation**: Generate Python functions from natural language descriptions
- **Quality Metrics**: View code quality metrics including complexity and maintainability
- **Syntax Highlighting**: Beautiful code highlighting for generated Python code
- **Multi-step Processing**: Agent analyzes, plans, generates, reviews, and refines code

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+ and npm/yarn
- OpenAI API key (or other LLM provider configured in your project)

## 🛠️ Installation

### Option 1: Quick Start (Recommended)

Use the provided startup scripts:

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Docker (Easiest)

1. Make sure Docker and Docker Compose are installed
2. Create a `.env` file in the `webapp` directory:
```bash
cd webapp
cp backend/.env.example .env
```

3. Edit `.env` and add your OpenAI API key

4. Run with Docker Compose:
```bash
docker-compose up
```

Both frontend and backend will start automatically!

### Option 3: Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd webapp/backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install main project dependencies (from project root):
```bash
cd ../..
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cd webapp/backend
cp .env.example .env
```

5. Edit `.env` and add your configuration:
```env
OPENAI_API_KEY=your_actual_api_key_here
MODEL_NAME=gpt-4
PORT=8000
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd webapp/frontend
```

2. Install Node.js dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env.local` file (copy from `.env.local.example`):
```bash
cp .env.local.example .env.local
```

4. The default configuration should work:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏃 Running the Application

### Start the Backend

From the project root directory:

```bash
cd webapp/backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

### Start the Frontend

In a new terminal, from the project root directory:

```bash
cd webapp/frontend
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns the health status and model configuration.

### Process Query (Non-streaming)
```
POST /api/query
Content-Type: application/json

{
  "query": "Write a function that counts vowels in a string",
  "show_node_info": true
}
```

### Stream Query (Real-time updates)
```
POST /api/stream
Content-Type: application/json

{
  "query": "Write a function that reverses a list",
  "show_node_info": true
}
```
Returns Server-Sent Events (SSE) stream.

### Process Structured Task
```
POST /api/task
Content-Type: application/json

{
  "task_id": "count_vowels",
  "signature": "def count_vowels(s: str) -> int:",
  "docstring": "Count vowels in a string",
  "examples": [
    {"input": "'hello'", "output": "2"}
  ],
  "show_node_info": true
}
```

## 💡 Usage Examples

### Example 1: Simple Function
```
User: Write a function that checks if a number is prime
```

The agent will:
1. Analyze the task
2. Create a plan
3. Generate the code
4. Review and test it
5. Refine if needed
6. Return the final code with quality metrics

### Example 2: String Manipulation
```
User: Create a function that removes duplicate characters from a string while preserving order
```

### Example 3: Data Structure Task
```
User: Write a function that finds the most frequent element in a list
```

## 🎨 Features of the UI

- **Message Display**: Clean, ChatGPT-style message bubbles
- **Code Highlighting**: Syntax-highlighted Python code with copy button
- **Quality Metrics**: Display of code quality metrics in an organized panel
- **Real-time Streaming**: See the agent's progress as it works
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Easy-on-the-eyes dark theme

## 🔧 Customization

### Backend Customization

Edit [main.py](webapp/backend/main.py) to:
- Add new endpoints
- Modify CORS settings
- Change streaming behavior
- Add authentication

### Frontend Customization

- **Colors**: Edit [tailwind.config.js](webapp/frontend/tailwind.config.js)
- **Components**: Modify files in [src/components/](webapp/frontend/src/components/)
- **API Configuration**: Update [src/utils/api.ts](webapp/frontend/src/utils/api.ts)

## 📁 Project Structure

```
webapp/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
└── frontend/
    ├── src/
    │   ├── components/        # React components
    │   │   ├── ChatInterface.tsx
    │   │   ├── MessageList.tsx
    │   │   ├── MessageItem.tsx
    │   │   ├── InputArea.tsx
    │   │   └── Header.tsx
    │   ├── pages/            # Next.js pages
    │   │   ├── index.tsx
    │   │   ├── _app.tsx
    │   │   └── _document.tsx
    │   ├── types/            # TypeScript types
    │   │   └── index.ts
    │   ├── utils/            # Utility functions
    │   │   └── api.ts
    │   └── styles/           # Global styles
    │       └── globals.css
    ├── package.json          # Node.js dependencies
    ├── tsconfig.json         # TypeScript configuration
    ├── tailwind.config.js    # Tailwind CSS configuration
    └── next.config.js        # Next.js configuration
```

## 🐛 Troubleshooting

### Backend Issues

**CORS Errors**: Make sure the frontend URL is in the `allow_origins` list in `main.py`

**Import Errors**: Ensure you're running from the project root or that `PROJECT_ROOT` is correctly set

**OpenAI API Errors**: Check your API key in `.env` and ensure you have credits

### Frontend Issues

**Connection Refused**: Ensure the backend is running on port 8000

**Build Errors**: Try deleting `node_modules` and `.next` folders, then reinstall:
```bash
rm -rf node_modules .next
npm install
```

**TypeScript Errors**: Ensure all dependencies are installed correctly

## 🚀 Production Deployment

### Backend Deployment

1. Use a production WSGI server:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Set up environment variables on your server
3. Consider using Docker for deployment

### Frontend Deployment

1. Build the production bundle:
```bash
npm run build
npm start
```

2. Deploy to Vercel, Netlify, or your preferred hosting platform

3. Update `NEXT_PUBLIC_API_URL` to point to your production backend

## 📝 License

This project is part of the LLM-for-SE research project.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📧 Support

For questions and support, please refer to the main project documentation.
