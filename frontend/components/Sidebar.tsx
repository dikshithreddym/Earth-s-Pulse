'use client'

import { useState, useEffect } from 'react'
import TrendChart from './TrendChart'
import { MoodPoint } from '@/types/mood'

interface SidebarProps {
  summary: string
  moods: MoodPoint[]
  lastUpdate: Date
  loading: boolean
  onClose?: () => void
}

export default function Sidebar({ summary, moods, lastUpdate, loading, onClose }: SidebarProps) {
  // Calculate statistics
  const totalPoints = moods.length
  const positiveCount = moods.filter(m => m.score > 0.3).length
  const negativeCount = moods.filter(m => m.score < -0.3).length
  const neutralCount = moods.filter(m => m.score >= -0.3 && m.score <= 0.3).length
  
  const avgScore = moods.length > 0
    ? moods.reduce((sum, m) => sum + m.score, 0) / moods.length
    : 0

  // Client-side only time formatting to avoid hydration mismatch
  const [displayTime, setDisplayTime] = useState<string>('')

  useEffect(() => {
    // Only format time on client side
    const formatTime = (date: Date) => {
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      })
    }
    setDisplayTime(formatTime(lastUpdate))
  }, [lastUpdate])

  return (
    <div
      className="w-full h-full bg-gray-900/95 backdrop-blur-xl text-white overflow-y-auto shadow-2xl flex-shrink-0 border-r border-gray-800/50"
      style={{ position: 'relative', zIndex: 10 }}
    >
      <div className="p-4 sm:p-5 lg:p-6 space-y-4 sm:space-y-5 lg:space-y-6">
        {/* Header */}
        <div className="border-b border-gray-700/50 pb-3 lg:pb-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2 lg:gap-3 flex-1 min-w-0">
              <div className="w-10 h-10 lg:w-12 lg:h-12 rounded-lg lg:rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg flex-shrink-0">
                <span className="text-xl lg:text-2xl">🌍</span>
              </div>
              <div className="min-w-0 flex-1">
                <h2 className="text-xl lg:text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent truncate">
                  Global Mood
                </h2>
                <p className="text-xs text-gray-400 mt-0.5 truncate">
                  Real-time emotional insights
                </p>
              </div>
            </div>
            {/* Close button for mobile */}
            {onClose && (
              <button
                onClick={onClose}
                className="lg:hidden ml-2 p-2 hover:bg-gray-800 rounded-lg transition-colors flex-shrink-0"
                aria-label="Close sidebar"
              >
                <svg
                  className="w-5 h-5 text-gray-400"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          <div className="flex items-center gap-2 mt-2 lg:mt-3 text-xs text-gray-400">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse flex-shrink-0"></div>
            <span className="truncate">Last updated: {displayTime || '--:--:--'}</span>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-2 gap-3 sm:gap-4">
          <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 rounded-lg lg:rounded-xl p-3 lg:p-4 border border-blue-500/20 hover:border-blue-500/40 transition-all duration-300">
            <div className="flex items-center gap-1.5 lg:gap-2 mb-2">
              <div className="w-7 h-7 lg:w-8 lg:h-8 rounded-lg bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                <span className="text-base lg:text-lg">📍</span>
              </div>
              <p className="text-xs text-gray-400 uppercase tracking-wide truncate">Total Points</p>
            </div>
            <p className="text-2xl lg:text-3xl font-bold text-white">{totalPoints}</p>
          </div>
          <div className="bg-gradient-to-br from-purple-900/50 to-purple-800/30 rounded-lg lg:rounded-xl p-3 lg:p-4 border border-purple-500/20 hover:border-purple-500/40 transition-all duration-300">
            <div className="flex items-center gap-1.5 lg:gap-2 mb-2">
              <div className="w-7 h-7 lg:w-8 lg:h-8 rounded-lg bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                <span className="text-base lg:text-lg">📊</span>
              </div>
              <p className="text-xs text-gray-400 uppercase tracking-wide truncate">Avg Score</p>
            </div>
            <p className="text-2xl lg:text-3xl font-bold text-white">
              {avgScore >= 0 ? '+' : ''}{avgScore.toFixed(2)}
            </p>
          </div>
        </div>

        {/* Sentiment Distribution */}
        <div className="bg-gray-800/50 rounded-lg lg:rounded-xl p-3 lg:p-4 border border-gray-700/50">
          <h3 className="text-base lg:text-lg font-semibold mb-3 lg:mb-4 flex items-center gap-2">
            <span className="text-lg lg:text-xl">📈</span>
            <span className="truncate">Sentiment Distribution</span>
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500 shadow-lg shadow-green-500/50"></div>
                  <span className="text-sm font-medium">Positive</span>
                </div>
                <span className="font-bold text-green-400">{positiveCount}</span>
              </div>
              <div className="w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-green-500 to-green-400 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${totalPoints > 0 ? (positiveCount / totalPoints) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-yellow-500 shadow-lg shadow-yellow-500/50"></div>
                  <span className="text-sm font-medium">Neutral</span>
                </div>
                <span className="font-bold text-yellow-400">{neutralCount}</span>
              </div>
              <div className="w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-yellow-500 to-yellow-400 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${totalPoints > 0 ? (neutralCount / totalPoints) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500 shadow-lg shadow-red-500/50"></div>
                  <span className="text-sm font-medium">Negative</span>
                </div>
                <span className="font-bold text-red-400">{negativeCount}</span>
              </div>
              <div className="w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-red-500 to-red-400 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${totalPoints > 0 ? (negativeCount / totalPoints) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Trend Chart */}
        <div className="bg-gray-800/50 rounded-lg lg:rounded-xl p-3 lg:p-4 border border-gray-700/50">
          <h3 className="text-base lg:text-lg font-semibold mb-2 lg:mb-3 flex items-center gap-2">
            <span className="text-lg lg:text-xl">📉</span>
            <span className="truncate">Trend Analysis</span>
          </h3>
          <TrendChart moods={moods} />
        </div>

        {/* AI Summary */}
        <div className="bg-gradient-to-br from-blue-900/50 via-purple-900/50 to-pink-900/50 rounded-lg lg:rounded-xl p-4 lg:p-5 border border-blue-500/30 shadow-lg shadow-blue-500/10">
          <h3 className="text-base lg:text-lg font-semibold mb-2 lg:mb-3 flex items-center gap-2">
            <div className="w-7 h-7 lg:w-8 lg:h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
              <span className="text-base lg:text-lg">🤖</span>
            </div>
            <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent truncate">
              AI Summary
            </span>
          </h3>
          {loading ? (
            <div className="space-y-2">
              <div className="h-3 bg-gray-700/50 rounded animate-pulse"></div>
              <div className="h-3 bg-gray-700/50 rounded animate-pulse w-5/6"></div>
              <div className="h-3 bg-gray-700/50 rounded animate-pulse w-4/6"></div>
            </div>
          ) : (
            <p className="text-sm leading-relaxed text-gray-200">
              {summary || 'No summary available yet. Please wait for data to load.'}
            </p>
          )}
        </div>

        {/* Legend */}
        <div className="bg-gray-800/50 rounded-lg lg:rounded-xl p-3 lg:p-4 border border-gray-700/50">
          <h3 className="text-base lg:text-lg font-semibold mb-2 lg:mb-3 flex items-center gap-2">
            <span className="text-lg lg:text-xl">🗺️</span>
            <span className="truncate">Map Legend</span>
          </h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700/30 transition-colors">
              <div className="w-5 h-5 rounded-full bg-green-500 shadow-lg shadow-green-500/50 flex-shrink-0"></div>
              <span className="text-gray-300">Positive Sentiment (Score &gt; 0.3)</span>
            </div>
            <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700/30 transition-colors">
              <div className="w-5 h-5 rounded-full bg-yellow-500 shadow-lg shadow-yellow-500/50 flex-shrink-0"></div>
              <span className="text-gray-300">Neutral Sentiment (-0.3 to 0.3)</span>
            </div>
            <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700/30 transition-colors">
              <div className="w-5 h-5 rounded-full bg-red-500 shadow-lg shadow-red-500/50 flex-shrink-0"></div>
              <span className="text-gray-300">Negative Sentiment (Score &lt; -0.3)</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500 pt-3 lg:pt-4 border-t border-gray-700/50">
          <div className="flex items-center justify-center gap-2 mb-1.5 lg:mb-2">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse flex-shrink-0"></div>
            <p className="font-medium truncate">Earth's Pulse v1.0</p>
          </div>
          <p className="text-gray-600 text-xs truncate">Data updates every 30 seconds</p>
        </div>
      </div>
    </div>
  )
}

