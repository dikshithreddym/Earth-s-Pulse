# 🌍 Earth's Pulse — Real-Time Global Sentiment Visualizer



> **HackTrent 2025 Submission**  
> A real-time AI-powered platform that visualizes the emotional pulse of our planet using Reddit sentiment analysis.

---

## 📚 Table of Contents

- [🎯 Project Vision](#-project-vision)
- [🏆 HackTrent 2025 Prize Categories](#-hacktrent-2025-prize-categories)
- [🎯 The Problem](#-the-problem)
- [🌟 Key Features](#-key-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [💡 Our Solution](#-our-solution)
- [🚀 Quick Start Guide](#-quick-start-guide)
- [📡 API Reference](#-api-reference)
- [🎨 How It Works](#-how-it-works)
- [🌍 Geographic Coverage](#-geographic-coverage)
- [🏆 HackTrent 2025 Alignment](#-hacktrent-2025-alignment)
- [🚧 Challenges & Solutions](#-challenges--solutions)
- [🔮 Future Enhancements](#-future-enhancements)
- [👥 Team](#-team)
- [📚 Documentation](#-documentation)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📞 Contact](#-contact)

---

## 🎯 Project Vision

**Earth's Pulse** transforms social media into a living, breathing emotional map of our planet.

By combining:
- real-time **Reddit data**
- **AI sentiment analysis**
- **3D globe visualization**

…we give users a way to explore how communities across the world are feeling — *right now*.

---

## 🏆 HackTrent 2025 Prize Categories

This project competes for:

- ✨ **Best Use of AI (Reach Capital)**  
  Advanced sentiment analysis using Hugging Face transformers and OpenRouter LLMs.

- 🎤 **Best Use of ElevenLabs**  
  Natural AI-powered voice narration of city sentiment summaries.

- 🚀 **General Category**  
  Full-stack innovation with real-world impact.

- 🤖 **Best Use of OpenRouter AI**  
  Multi-model LLM integration for smart, contextual narratives.

---

## 🎯 The Problem

We live in a hyper-connected world, but we still struggle to answer simple questions like:

- *How is the world feeling right now?*  
- *Which cities are hopeful, anxious, or joyful?*  
- *How do global events impact people emotionally across regions?*

Existing tools focus on raw numbers (likes, shares, counts), not emotional climate.  
**Earth’s Pulse** changes that by turning social media sentiment into an **interactive, real-time emotional map.**

---

## 🌟 Key Features

### 🔍 Real-Time Sentiment Analysis

- **Live Reddit Data** — Posts from **200+ cities** worldwide via Reddit API  
- **AI-Powered Sentiment** — Cardiff NLP RoBERTa model for robust classification  
- **Emotion Labels** — Joyful (positive), Anxious (negative), Neutral

### 🌐 Interactive 3D Globe

- **WebGL / Three.js Globe** with realistic Earth textures and borders  
- **Color-Coded Mood Points** –  
  - 🟢 Positive  
  - 🟡 Neutral  
  - 🔴 Negative  
- **City-Level Detail** for 200+ major cities across 6 continents  
- **Smooth Animations** with clickable cities and zoom

### 🤖 AI-Generated City Summaries

- **OpenRouter LLMs** (Qwen, Gemma, Mistral, LLaMA models)  
- **Human-Readable Narratives** that describe the emotional climate of each city  
- **Smart Caching** (45-second TTL) to balance freshness and performance

### 🎙️ Text-to-Speech Narration

- **ElevenLabs Integration** for natural, human-like voices  
- **Multiple Output Modes**: Base64, streaming audio, or URL  
- **Optimized TTS Settings** (stability, clarity, style, speaker boost)

### 📊 Data Intelligence Layer

- **MongoDB + Motor** async storage for mood data points  
- **Background Refresh** every 5 minutes (configurable)  
- **Historical Tracking** via timestamps for trend analysis

### 🎨 Modern User Experience

- **Next.js + TailwindCSS** mobile-first UI  
- **Dark Theme** with glassmorphism and gradients  
- **Interactive Popups & Live Stats**  
- **Keyboard & Screen-Reader Friendly**

---

## 🛠️ Technology Stack

### Backend (FastAPI + AI/ML)

- **FastAPI** – Async Python web framework  
- **PRAW** – Reddit API client  
- **Hugging Face Transformers** – `cardiffnlp/twitter-roberta-base-sentiment-latest`  
- **Motor + MongoDB** – Async document store  
- **OpenRouter API** – LLM-powered summaries  
- **ElevenLabs API** – Text-to-Speech  
- **httpx** – Async HTTP client

### Frontend (Next.js + 3D Globe)

- **Next.js 14** – App Router, SSR/SSG  
- **React 18 + TypeScript 5**  
- **TailwindCSS 3** – Utility-first styling  
- **Globe.gl + Three.js** – 3D globe visualization  
- **Framer Motion** – Animations  
- **Axios** – API communication

### DevOps & Infra

- **Docker** – Multi-stage container builds  
- **Docker Compose** – Backend + Frontend + MongoDB orchestration  
- **Vercel** – Frontend hosting  
- **Environment-based Config** – secure API key loading

---

## 💡 Our Solution

**Earth's Pulse** is a full-stack AI platform that:

1. **Collects**  
   Real-time Reddit data across 200+ cities.

2. **Analyzes**  
   Each post with Hugging Face Transformers for sentiment.

3. **Visualizes**  
   Global emotions on an interactive 3D globe.

4. **Summarizes**  
   City-level emotional climates using OpenRouter LLMs.

5. **Narrates**  
   Summaries using ElevenLabs Text-to-Speech for an immersive audio experience.

---

## 🚀 Quick Start Guide

### ✅ Prerequisites

- **Python** 3.9+  
- **Node.js** 18+  
- **MongoDB** (local or Atlas)  
- API keys for:
  - Reddit
  - OpenRouter
  - ElevenLabs

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dikshithreddym/Earth-s-Pulse.git
cd Earth-s-Pulse
```

### 2️⃣ Backend Setup


```bash

cd backend---



# Install Python dependencies

pip install -r requirements.txt

## 🛠️ Tech Stack## 🏆 HackTrent 2025 Prize Categories```

# Create environment file

cp env.example .env



# Edit .env with your API keys:### Frontendearth-pulse/

# nano .env  (Linux/Mac)

# notepad .env  (Windows)

```

- **Next.js 14** – React framework with server-side renderingThis project qualifies for:├── frontend/          # Next.js React application

**Required Environment Variables:**

```env- **TypeScript** – Type-safe code

# MongoDB

MONGODB_URL=mongodb://localhost:27017- **globe.gl** – 3D Earth visualization (Three.js based)├── backend/           # FastAPI Python application

DATABASE_NAME=earth_pulse

- **Tailwind CSS** – Modern, responsive styling

# Reddit API (Required for live data)

REDDIT_CLIENT_ID=your_reddit_client_id- **Framer Motion** – Smooth animations### 🥇 General Category├── docker-compose.yml # Docker orchestration

REDDIT_CLIENT_SECRET=your_reddit_secret

REDDIT_USER_AGENT=EarthPulse/1.0- **Plotly.js** – Interactive sentiment charts



# OpenRouter API (Required for AI summaries)└── README.md

OPENROUTER_API_KEY=your_openrouter_api_key

OPENROUTER_MODEL=qwen/qwen-2-7b-instruct:free### Backend



# ElevenLabs API (Required for voice synthesis)Full-stack application with innovative 3D visualization and real-time data processing```

ELEVENLABS_API_KEY=your_elevenlabs_api_key

ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM- **FastAPI** – High-performance Python API



# Optional Settings- **PRAW** – Reddit API integration

ENABLE_BACKGROUND_REFRESH=true

REFRESH_INTERVAL_MINUTES=5- **Transformers (Hugging Face)** – Sentiment analysis (`cardiffnlp/twitter-roberta-base-sentiment-latest`)

ENVIRONMENT=development

```- **OpenRouter API** – LLM-powered summaries (LLaMA 3.1 8B Instruct)### 🤖 Best Use of AI powered by Reach Capital## 🛠️ Setup Instructions



**Start Backend Server:**- **ElevenLabs API** – Text-to-Speech narration

```bash

uvicorn main:app --reload --host 0.0.0.0 --port 8000- **MongoDB** – Data persistence with Motor (async driver)

```

- **httpx** – Async HTTP client

API will be available at: `http://localhost:8000`  

Interactive docs at: `http://localhost:8000/docs`- Transforms how we understand global emotional well-being### Prerequisites



### 3️⃣ Frontend Setup### DevOps & Deployment



```bash- Uses AI to provide actionable insights for mental health and social research

cd frontend

- **Docker** – Containerization for both frontend and backend

# Install Node dependencies

npm install- **Vercel** – Frontend deployment- Impacts learning (sentiment analysis education) and health (emotional climate awareness)- Node.js 18+ and npm/yarn



# Create environment file- **Railway/Render** – Backend deployment options

echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local

- Python 3.9+

# Start development server

npm run dev---

```

### 🎵 Best Use of ElevenLabs- Docker (optional, for containerized deployment)

App will be available at: `http://localhost:3000`

## 🚀 Quick Start


# Create .env.local file with:

#### `GET /api/city/summary`

Generate AI summary for specific city# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000- **MongoDB** – Data persistence with Motor (async driver)cp .env.example .env

```typescript

Query Parameters:

  - city: string           // City name (required)

  - limit?: number         // Max posts to analyze (default: 50)# Run frontend- **httpx** – Async HTTP client```



Response:npm run dev

{

  city: string,```

  summary: string,         // AI narrative about city mood

  statistics: {

    total_posts: number,

    positive: number,**Frontend runs at:** `http://localhost:3000`### DevOps & Deployment5. Fill in your API credentials in `.env`:

    neutral: number,

    negative: number,

    average_score: number```

  },### 4️⃣ Docker (Full Stack)

  sample_posts: Array<Post>,

  timestamp: string,

  data_source: 'reddit_api',

  ai_model: 'openrouter'```bash- **Docker** – Containerization for both frontend and backendREDDIT_CLIENT_ID=your_reddit_client_id

}

```docker-compose up --build



#### `GET /api/city/summary/audio````- **Vercel** – Frontend deploymentREDDIT_CLIENT_SECRET=your_reddit_secret

Convert city summary to speech

```typescript

Query Parameters:

  - city: string           // City name (required)---- **Railway/Render** – Backend deployment (production-ready)REDDIT_USER_AGENT=your_app_name/1.0

  - format?: 'base64' | 'url' | 'stream'

  - voice_id?: string      // ElevenLabs voice ID

  - model?: string         // TTS model override

## 🔑 API Keys Required- **GitHub Actions** – CI/CD pipeline (optional)TWITTER_BEARER_TOKEN=your_twitter_token

Response (base64):

{

  audio_base64: string,

  mime: 'audio/mpeg',Create a `backend/.env` file:MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/earthpulse

  summary: string,

  city: string,

  statistics: object,

  timestamp: string```env---OPENROUTER_API_KEY=your_openrouter_key

}

```# Reddit API (Required)



---REDDIT_CLIENT_ID=your_client_id```



## 🎨 How It WorksREDDIT_CLIENT_SECRET=your_client_secret



### 1. Data Collection PipelineREDDIT_USER_AGENT=EarthPulse/1.0## 🚀 Quick Start

```python

Reddit API → City-Specific Queries → 200+ Cities

├── Search: "{city}" (feeling OR mood OR today OR life...)

├── Filter: Last 24 hours, min 20 characters# OpenRouter API (Required for AI summaries)6. Run the backend:

├── Rate Limiting: Smart batching and caching

└── Output: Raw post text + metadataOPENROUTER_API_KEY=sk-or-v1-your-key-here

```

OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free### Prerequisites```bash

### 2. Sentiment Analysis Engine

```python

Cardiff NLP RoBERTa Model

├── Input: Cleaned post text# ElevenLabs API (Required for audio)uvicorn main:app --reload --host 0.0.0.0 --port 8000

├── Processing: Transformer neural network

├── Output: Label + Confidence ScoreELEVENLABS_API_KEY=sk_your-key-here

└── Mapping:

    ├── positive → joyful (0.3 to 1.0)ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM- Node.js 18+```

    ├── negative → anxious (-1.0 to -0.3)

    └── neutral → neutral (-0.3 to 0.3)

```

# MongoDB (Optional - uses in-memory if not provided)- Python 3.9+

### 3. AI Summary Generation

```pythonMONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/earthpulse

OpenRouter LLM Pipeline

├── Model: Qwen-2-7B-Instruct (primary)```- Docker (optional)Or with Docker:

├── Fallbacks: Gemma, Mistral, Llama

├── Prompt Engineering:

│   └── "Analyze {N} Reddit posts from {city}..."

│       "Write human-readable narrative..."### How to Get API Keys```bash

│       "Focus on lived experiences..."

├── Parameters:

│   ├── Temperature: 0.8 (creative)

│   ├── Max Tokens: 3001. **Reddit API** (Free)### 1️⃣ Clone the Repositorydocker build -t earth-pulse-backend .

│   └── Stop Sequences: [</s>, [/INST]]

└── Output: 4-6 sentence narrative   - Go to https://www.reddit.com/prefs/apps

```

   - Create app → "script" typedocker run -p 8000:8000 --env-file .env earth-pulse-backend

### 4. Voice Synthesis

```python   - Copy client_id and client_secret

ElevenLabs TTS Pipeline

├── Model: eleven_multilingual_v2```bash```

├── Voice Settings:

│   ├── Stability: 0.62. **OpenRouter API** (Free $10 credit from MLH!)

│   ├── Similarity Boost: 0.7

│   ├── Style: 0.3   - Go to https://openrouter.ai/git clone https://github.com/dikshithreddym/Earth-s-Pulse.git

│   └── Speaker Boost: True

├── Input: AI-generated summary text   - Sign up and generate API key

└── Output: MP3 audio stream (Base64/URL/Stream)

  - Use MLH promo code for $10 creditcd Earth-s-Pulse### Frontend Setup

``` 

### 5. 3D Visualization

```typescript

Globe.gl + Three.js Rendering3. **ElevenLabs API** (Free tier: 10k chars/month)```

├── Earth Texture: High-res day imagery

├── Country Borders: GeoJSON polygons   - Go to https://elevenlabs.io/

├── Mood Points:

│   ├── Color: Sentiment-based (Green/Yellow/Red)   - Sign up for free account1. Navigate to frontend directory:

│   ├── Size: Proportional to score strength

│   └── Animation: Smooth transitions   - Generate API key from Profile → API Keys

└── Interaction:

    ├── Click: Show city popup### 2️⃣ Backend Setup```bash

    ├── Hover: Highlight point

    └── Zoom: Auto-focus on selection4. **MongoDB** (Free)

```

   - Go to https://www.mongodb.com/cloud/atlascd frontend

---

   - Create free cluster

## 🌍 Geographic Coverage

   - Get connection string```bash```

**200+ Cities Tracked Worldwide:**



| Region | Cities | Examples |


| 🇺🇸 North America | 50 | New York, Los Angeles, Toronto, Mexico City |

| 🇧🇷 South America | 25 | São Paulo, Buenos Aires, Lima, Bogotá |

| 🇬🇧 Europe | 50 | London, Paris, Berlin, Madrid, Rome |

| 🇯🇵 Asia | 50 | Tokyo, Beijing, Mumbai, Seoul, Bangkok |## 📡 API Endpoints2. Install dependencies:

| 🇿🇦 Africa | 15 | Cairo, Lagos, Nairobi, Cape Town |

| 🇦🇺 Oceania | 10 | Sydney, Melbourne, Auckland, Brisbane |



**Selection Criteria:**### `GET /api/moods`# Create virtual environment```bash

- Population > 1M residents

- Active Reddit communities

- Geographic diversity

- Cultural significanceReturns real-time sentiment data pointspython -m venv venvnpm install



---



## 🏆 HackTrent 2025 Alignment```json# On Windows PowerShell:# or



### Innovation & Creativity (25%)[

✅ **Unique Concept** - First real-time global emotional map using Reddit data  

✅ **3D Visualization** - Stunning WebGL globe with interactive mood points    {venv\Scripts\Activate.ps1yarn install

✅ **AI Integration** - Multi-model LLM summaries + TTS narration  

✅ **Cross-Domain** - Combines NLP, computer vision, and web technologies    "lat": 43.6532,



### Technical Complexity (25%)    "lng": -79.3832,# On Linux/Mac:```

✅ **Full-Stack** - FastAPI backend + Next.js frontend + MongoDB  

✅ **AI/ML Pipeline** - Hugging Face transformers + OpenRouter LLMs      "label": "joy",

✅ **Real-Time Data** - Reddit API integration with background refresh  

✅ **3D Graphics** - Three.js + Globe.gl for complex visualizations      "score": 0.85,source venv/bin/activate

✅ **API Integrations** - Reddit, OpenRouter, ElevenLabs, MongoDB Atlas


### Functionality & UX (20%)

✅ **Intuitive Interface** - Click any city for instant sentiment details      "source": "reddit",3. Run the development server:

✅ **Responsive Design** - Mobile-first approach with TailwindCSS  

✅ **Real-Time Updates** - Live data refresh every 30 seconds      "timestamp": "2025-11-09T12:34:56Z"

✅ **Accessibility** - Screen reader friendly, keyboard navigation  

✅ **Error Handling** - Graceful fallbacks for API failures  }# Install dependencies```bash



### Impact & Relevance (20%)]

✅ **Social Good** - Mental health awareness through sentiment tracking  

✅ **Real-World Use** - Disaster response, public health monitoring  ```pip install -r requirements.txtnpm run dev

✅ **Educational** - Teaches data science, NLP, and visualization  

✅ **Scalable** - Can expand to millions of users and cities



### Presentation & Communication (10%)### `GET /api/city/summary?city={city}&limit={limit}`# or

✅ **Clear Documentation** - Comprehensive README with examples  

✅ **Demo Video** - 3-minute walkthrough showcasing features  

✅ **Code Quality** - TypeScript, type hints, clean architecture  

✅ **Live Demo** - Deployed on Vercel for judgesAI-powered city sentiment analysis# Configure environment variablesyarn dev



### Bonus: Sponsor Tech Integration

🏆 **Google Gemini API** - Alternative LLM for summaries (Gemma-7b-it)  

🏆 **ElevenLabs** - Text-to-speech with voice synthesis  ```jsoncp env.example .env```

🏆 **OpenRouter** - Unified access to multiple AI models  

🏆 **Reach Capital AI** - Sentiment analysis with Hugging Face{

## 🎯 Real-World Use Cases  "summary": "Toronto's Reddit community shows a generally positive emotional climate...",

### 🏛️ Government & Policy Makers  "statistics": {4. Open [http://localhost:3000](http://localhost:3000) in your browser

- Monitor public sentiment on policies and legislation

- Identify regions requiring social support programs    "total_posts": 50,

- Track emotional impact of government decisions

- Emergency response during natural disasters    "positive": 30,# Run backend



### 🧠 Mental Health Researchers    "neutral": 15

- Study global emotional patterns and seasonal trends

- Identify cities with concerning sentiment trajectories    "negative": 5,uvicorn main:app --reload### Docker Compose (Full Stack)

- Correlate emotions with world events and news

- Develop intervention strategies based on data    "average_score": 0.42



### 📰 Journalists & Media

- Visualize public reaction to breaking news

- Create data-driven emotional climate reports  "sample_posts": [...],

- Identify emerging social movements and trends

- Compare sentiment across different regions  "data_source": "reddit_api",Run both frontend and backend together:



### 🎓 Educational Institutions  "ai_model": "openrouter"

- Teach sentiment analysis and NLP concepts

- Demonstrate real-world AI applications}**Backend runs at:** `http://localhost:8000`

- Showcase data visualization best practices

- Research projects on social media analysis```



### 🏢 Social Good Organizations

- Target outreach to cities with negative sentiment

- Measure impact of community initiatives### `GET /api/city/summary/audio?city={city}&format=base64`

- Understand emotional well-being of communities

- Coordinate global mental health campaigns### 3️⃣ Frontend Setupdocker-compose up --build






## 🐳 Docker Deployment



### Using Docker Compose (Recommended)



```bash{```bash

# Build and start all services



 - Services started:  "mime": "audio/mpeg",cd frontend## 📡 API Endpoints

 - MongoDB: localhost:27017

 - Backend: localhost:8000  "summary": "...",

 - Frontend: localhost:3000


## 📊 Performance & Statistics---# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000    "lat": 40.7128,



- **200+ Cities** tracked globally

- **50+ Posts** analyzed per city per refresh

- **< 1 second** sentiment analysis per post## 🎨 How It Works    "lng": -74.0060,

- **< 2 seconds** AI summary generation

- **5 minutes** background refresh interval

- **Real-time** 3D globe visualization

- **30 seconds** frontend auto-refresh### 1. Data Collection# Run frontend    "label": "anxious",



**Optimizations:**

- Async I/O with FastAPI + Motor

- Connection pooling for MongoDB- Reddit API fetches posts from 200+ cities worldwidenpm run dev    "score": -0.6,

- 45-second TTL cache for AI summaries

- Debounced resize handlers (150ms)- Posts are filtered by location, recency, and relevance

- Code splitting for globe.gl

- Smart city deduplication- Real-time updates every 30 seconds```    "source": "reddit",







## 🚧 Challenges & Solutions### 2. Sentiment Analysis    "timestamp": "2024-01-15T10:30:00Z"



### ⚡ Challenge 1: Reddit API Rate Limits

**Problem:** Reddit limits requests to 60/minute  

**Solution:** - Each post is analyzed using Hugging Face Transformers**Frontend runs at:** `http://localhost:3000`  }

- Implemented intelligent request batching

- City-level deduplication (one post per city)- Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`

- Background refresh instead of real-time polling

- Smart caching with MongoDB- Returns emotion label and confidence score (-1 to 1)]



### 🗺️ Challenge 2: Accurate Location Mapping

**Problem:** Reddit posts don't include geolocation  

**Solution:**### 3. AI Summary Generation### 4️⃣ Docker (Full Stack)```

- Curated list of 200 cities with verified coordinates

- City-specific search queries (e.g., "Toronto + mood")

- Manual validation of major urban centers

- Geographic diversity in city selection- OpenRouter LLaMA 3.1 model generates natural language summaries



### ⚡ Challenge 3: Real-Time Performance- City-specific prompts for contextual analysis

**Problem:** Heavy AI processing could block the UI  

**Solution:**- Narrative style focusing on lived experiences```bash### `GET /api/summary`

- Async processing with FastAPI

- Background tasks for data refresh

- Client-side caching

- Progressive loading with skeleton screens### 4. Voice Narrationdocker-compose up --buildReturns global emotional summary:



### 🎨 Challenge 4: Three.js Compatibility

**Problem:** Globe.gl had missing module dependencies  

**Solution:**- ElevenLabs TTS converts summaries to speech``````json

- Created custom patches for webgpu/tsl modules

- Implemented stub modules for missing dependencies- High-quality, natural-sounding voices

- Canvas size control for responsive rendering

- Multiple initialization attempts with timeouts- Auto-play with replay functionality{



### 🤖 Challenge 5: Consistent AI Summaries

**Problem:** LLM outputs can be unpredictable  

**Solution:**### 5. Visualization---  "summary": "Today, South America is joyful while North America feels tense...",

- Detailed prompt engineering

- Multiple fallback models (Qwen → Gemma → Mistral)

- Stop sequences to prevent artifacts

- Post-processing to clean model tokens- globe.gl renders 3D Earth with Three.js  "timestamp": "2024-01-15T10:30:00Z"



---- Color-coded sentiment points (green/yellow/red)



## 🔮 Future Enhancements- Interactive tooltips and city modals## 🔑 API Keys Required}



- [ ] **Historical Trends** - Track sentiment changes over time with charts- Real-time statistics dashboard

- [ ] **Comparison Mode** - Side-by-side city emotion comparison

- [ ] **Twitter/X Integration** - Combine Reddit + Twitter for richer data```

- [ ] **Custom Date Ranges** - User-selectable time periods

- [ ] **Emotion Heatmap** - Gradient intensity-based visualization---

- [ ] **Multi-language Support** - Analyze and translate non-English posts

- [ ] **Real-time Notifications** - Alert users for major sentiment shiftsCreate a `backend/.env` file:

- [ ] **Mobile App** - Native iOS/Android apps with push notifications

- [ ] **User Accounts** - Save favorite cities, custom alerts## 🎯 Use Cases

- [ ] **Export Reports** - Download PDF/CSV sentiment reports


## 🧑‍💻 Development Team



**Developer:** Dikshith Reddy M, Dev Patel Karan Majotra

**University:** Trent University  

**Event:** HackTrent 2025  OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free```

**Timeline:** Built in 24 hours  

### 🎓 Education

---



## 🙏 Acknowledgments

- Teach sentiment analysis and NLP concepts

### HackTrent 2025 Sponsors

- **Reach Capital** - For promoting AI innovation in education, health, and work- Demonstrate real-world AI applications# ElevenLabs API (Required for audio)### Frontend Tests

- **ElevenLabs** - For providing natural voice synthesis capabilities

- **Google Gemini** - For access to cutting-edge AI models- Showcase data visualization techniques

- **OpenRouter** - For unified LLM API access

- **Major League Hacking (MLH)** - For organizing this incredible hackathonELEVENLABS_API_KEY=sk_your-key-here```bash



### Open Source Libraries### 🏢 Social Good Organizations

- **Hugging Face** - Cardiff NLP RoBERTa sentiment model

- **Three.js Community** - 3D graphics rendering engineELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAMcd frontend

- **Globe.gl** - Interactive globe visualization library

- **FastAPI** - Modern Python web framework- Target outreach to cities with negative sentiment

- **Next.js Team** - React framework excellence

- **Vercel** - Seamless deployment platform- Measure impact of initiatives on public moodnpm test



### Data Sources- Understand community emotional well-being

- **Reddit** - API access to community discussions

- **Natural Earth** - GeoJSON country boundary data# MongoDB (Optional - uses in-memory if not provided)```

- **NASA Visible Earth** - Earth texture imagery

## Links

**GitHub Repository:** https://github.com/dikshithreddym/Earth-s-Pulse  

**API Documentation:** http://localhost:8000/docs *(when running locally)*

