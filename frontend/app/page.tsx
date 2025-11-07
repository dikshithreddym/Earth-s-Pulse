'use client'

import { useEffect, useState } from 'react'
import GlobeComponent from '@/components/Globe'
import Sidebar from '@/components/Sidebar'
import { MoodPoint } from '@/types/mood'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [moods, setMoods] = useState<MoodPoint[]>([])
  const [summary, setSummary] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // Fetch moods from backend
  const fetchMoods = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/moods?limit=200`)
      if (response.ok) {
        const data = await response.json()
        setMoods(data)
        setLastUpdate(new Date())
      }
    } catch (error) {
      console.error('Error fetching moods:', error)
    } finally {
      setLoading(false)
    }
  }

  // Fetch summary from backend
  const fetchSummary = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/summary`)
      if (response.ok) {
        const data = await response.json()
        setSummary(data.summary || 'No summary available')
      }
    } catch (error) {
      console.error('Error fetching summary:', error)
    }
  }

  // Initial fetch
  useEffect(() => {
    fetchMoods()
    fetchSummary()
  }, [])

  // Auto-refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchMoods()
      fetchSummary()
    }, 30000) // 30 seconds

    return () => clearInterval(interval)
  }, [])

  return (
    <main className="flex flex-col lg:flex-row h-screen w-screen overflow-hidden relative">
      {/* Mobile Menu Toggle Button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-gray-900/90 backdrop-blur-xl rounded-xl p-3 border border-gray-700/50 shadow-2xl hover:bg-gray-800/90 transition-all"
        aria-label="Toggle sidebar"
      >
        <svg
          className="w-6 h-6 text-white"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          {sidebarOpen ? (
            <path d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Sidebar */}
      <div
        className={`
          fixed lg:static
          inset-y-0 left-0
          w-80 sm:w-96
          transform transition-transform duration-300 ease-in-out z-40
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        <Sidebar 
          summary={summary}
          moods={moods}
          lastUpdate={lastUpdate}
          loading={loading}
          onClose={() => setSidebarOpen(false)}
        />
      </div>

      {/* Overlay for mobile when sidebar is open */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Globe Container */}
      <div className="flex-1 relative flex items-center justify-center overflow-hidden min-w-0 w-full">
        <div className="absolute inset-0 flex items-center justify-center">
          <GlobeComponent moods={moods} loading={loading} />
        </div>
        
        {/* Header Overlay - Responsive */}
        <div className="absolute top-4 left-4 right-4 lg:top-6 lg:left-6 lg:right-auto z-10">
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-xl lg:rounded-2xl px-4 py-3 lg:px-6 lg:py-4 border border-gray-700/50 shadow-2xl max-w-full">
            <div className="flex items-center gap-2 lg:gap-3 mb-1">
              <div className="w-8 h-8 lg:w-10 lg:h-10 rounded-lg lg:rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg flex-shrink-0">
                <span className="text-xl lg:text-2xl">🌍</span>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent truncate">
                  Earth's Pulse
                </h1>
                <p className="text-xs lg:text-sm text-gray-400 mt-0.5 truncate">
                  Real-Time Emotional Map of the Planet
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Loading Indicator */}
        {loading && (
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-20">
            <div className="bg-gray-900/90 backdrop-blur-xl rounded-xl lg:rounded-2xl px-6 py-5 lg:px-8 lg:py-6 border border-gray-700/50 shadow-2xl mx-4">
              <div className="flex flex-col items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 lg:w-12 lg:h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
                  <div className="absolute top-0 left-0 w-10 h-10 lg:w-12 lg:h-12 border-4 border-transparent border-t-purple-500 rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
                </div>
                <p className="text-white font-medium text-sm lg:text-base">Loading emotional data...</p>
                <p className="text-xs text-gray-400">Analyzing global sentiment</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}

