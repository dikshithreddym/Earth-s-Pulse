# 🌍 Earth's Pulse – Real-Time Emotional Map of the Planet

A full-stack web application that visualizes real-time emotional sentiment from social media posts on an interactive 3D globe.

## 🚀 Features

- **3D Interactive Globe**: Rotatable, zoomable Earth visualization using globe.gl
- **Real-Time Sentiment Analysis**: Live emotional data from Reddit and Twitter
- **Color-Coded Emotions**: Green (positive), Yellow (neutral), Red (negative)
- **Global Mood Summary**: AI-generated emotional insights using OpenRouter
- **Trend Visualization**: Sentiment distribution charts over time
- **Auto-Refresh**: Map updates every 30 seconds

## 📁 Project Structure

```
earth-pulse/
├── frontend/          # Next.js React application
├── backend/           # FastAPI Python application
├── docker-compose.yml # Docker orchestration
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- Docker (optional, for containerized deployment)
- MongoDB Atlas account (or local MongoDB)
- Reddit API credentials (PRAW)
- Twitter/X API credentials (Tweepy) - Optional
- OpenRouter API key - Optional

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Fill in your API credentials in `.env`:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_app_name/1.0
TWITTER_BEARER_TOKEN=your_twitter_token
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/earthpulse
OPENROUTER_API_KEY=your_openrouter_key
```

6. Run the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or with Docker:
```bash
docker build -t earth-pulse-backend .
docker run -p 8000:8000 --env-file .env earth-pulse-backend
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Docker Compose (Full Stack)

Run both frontend and backend together:

```bash
docker-compose up --build
```

## 📡 API Endpoints

### `GET /api/moods`
Returns array of sentiment data points:
```json
[
  {
    "lat": 40.7128,
    "lng": -74.0060,
    "label": "anxious",
    "score": -0.6,
    "source": "reddit",
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

### `GET /api/summary`
Returns global emotional summary:
```json
{
  "summary": "Today, South America is joyful while North America feels tense...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### `GET /api/health`
Health check endpoint

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🎨 Tech Stack

**Frontend:**
- Next.js 14
- React 18
- globe.gl (Three.js)
- Tailwind CSS
- Framer Motion
- Plotly.js

**Backend:**
- FastAPI
- PRAW (Reddit API)
- Tweepy (Twitter API)
- Hugging Face Transformers
- spaCy + NLTK
- MongoDB/PostgreSQL
- OpenRouter API

## 📝 License

MIT License - Feel free to use for your hackathon project!

## 🤝 Contributing

This is a hackathon project. Contributions and improvements welcome!

