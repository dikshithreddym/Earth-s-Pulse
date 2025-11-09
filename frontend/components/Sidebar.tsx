'use client'

import React, { useEffect, useMemo, useRef, useState } from "react";
import TrendChart from './TrendChart'
import { MoodPoint } from '@/types/mood'
import CityPostsModal from './CityPostsModal'

interface SidebarProps {
  summary: string
  moods: MoodPoint[]
  lastUpdate: Date
  loading: boolean
  onClose?: () => void
}

export default function Sidebar(props: any) {
  const { summary, moods, lastUpdate, loading, onClose } = props
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

  // TTS playback state
  const [ttsLoading, setTtsLoading] = useState(false)
  const [ttsError, setTtsError] = useState<string | null>(null)
  const [audioSrc, setAudioSrc] = useState<string | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const audioElementId = 'summary-audio-player'

  const backendBase = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

  const handlePlaySummaryAudio = async () => {
    // Re-fetch audio each time to reflect updated summary
    setTtsError(null)
    setTtsLoading(true)
    try {
      const resp = await fetch(`${backendBase}/api/summary/audio?format=base64`)
      if (!resp.ok) {
        throw new Error(`TTS request failed (${resp.status})`)
      }
      const data = await resp.json()
      if (!data.audio_base64) {
        throw new Error('No audio returned')
      }
      const src = `data:${data.mime || 'audio/mpeg'};base64,${data.audio_base64}`
      setAudioSrc(src)
      // Play immediately
      setTimeout(() => {
        const el = document.getElementById(audioElementId) as HTMLAudioElement | null
        if (el) {
          el.play().then(() => setIsPlaying(true)).catch(err => setTtsError(err.message))
        }
      }, 50)
    } catch (e: any) {
      setTtsError(e.message || 'Failed to generate audio')
    } finally {
      setTtsLoading(false)
    }
  }

  const handleTogglePlayback = () => {
    const el = document.getElementById(audioElementId) as HTMLAudioElement | null
    if (!el) return
    if (el.paused) {
      el.play().then(() => setIsPlaying(true)).catch(err => setTtsError(err.message))
    } else {
      el.pause()
      setIsPlaying(false)
    }
  }

  const [audioLoading, setAudioLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const objectUrlRef = useRef<string | null>(null);

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  const [postsOpen, setPostsOpen] = useState(false);
  const [postsCity, setPostsCity] = useState<string | undefined>(undefined);
  const [posts, setPosts] = useState<any[]>([]);

  const generateAudio = async () => {
    setAudioLoading(true);
    try {
      // Pause and cleanup old audio
      if (audioRef.current) {
        try { audioRef.current.pause(); } catch {}
        audioRef.current.src = "";
      }
      if (objectUrlRef.current) {
        URL.revokeObjectURL(objectUrlRef.current);
        objectUrlRef.current = null;
      }

      // Add cache buster to ensure fresh response from any proxy
      const url = `${backendUrl}/api/summary/audio?format=base64&ts=${Date.now()}`;
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error(`Audio gen failed ${res.status}`);
      const json = await res.json();
      if (!json.audio_base64) throw new Error("No audio_base64 in response");

      // Build a Blob + object URL (more reliable than raw data: URLs for reloading)
      const byteChars = atob(json.audio_base64);
      const byteNums = new Array(byteChars.length);
      for (let i = 0; i < byteChars.length; i++) byteNums[i] = byteChars.charCodeAt(i);
      const blob = new Blob([new Uint8Array(byteNums)], { type: "audio/mpeg" });
      const objUrl = URL.createObjectURL(blob);
      objectUrlRef.current = objUrl;

      // Create a fresh Audio element each time
      const a = new Audio();
      a.preload = "auto";
      a.src = objUrl + `#v=${Date.now()}`; // extra bust for some browsers
      audioRef.current = a;

      // Optionally autoplay the fresh audio
      // await a.play();
    } catch (e) {
      console.error(e);
    } finally {
      setAudioLoading(false);
    }
  };

  const onPlay = async () => {
    if (!audioRef.current) return;
    try {
      // Ensure we load the new src before playing
      audioRef.current.currentTime = 0;
      await audioRef.current.play();
    } catch (e) {
      console.error(e);
    }
  };

  const onPause = () => {
    if (!audioRef.current) return;
    try { audioRef.current.pause(); } catch {}
  };

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      try { audioRef.current?.pause(); } catch {}
      if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
    };
  }, []);

  const openCityPosts = async (city: string) => {
    const res = await fetch(`${backendUrl}/api/posts?city=${encodeURIComponent(city)}&limit=50`, { cache: "no-store" });
    const json = await res.json();
    setPosts(json.posts || []);
    setPostsCity(city);
    setPostsOpen(true);
  };

  return (
    <>
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
            <div className="flex items-center justify-between mb-2 lg:mb-3">
              <h3 className="text-base lg:text-lg font-semibold flex items-center gap-2">
                <div className="w-7 h-7 lg:w-8 lg:h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                  <span className="text-base lg:text-lg">🤖</span>
                </div>
                <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent truncate">
                  AI Summary
                </span>
              </h3>
              <div className="flex items-center gap-2">
                <button
                  disabled={loading || ttsLoading}
                  onClick={handlePlaySummaryAudio}
                  className="px-2 py-1 text-xs rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  aria-label="Generate summary audio"
                >
                  {ttsLoading ? 'Generating…' : '🔊 Generate'}
                </button>
                {audioSrc && (
                  <button
                    onClick={handleTogglePlayback}
                    className="px-2 py-1 text-xs rounded-md bg-purple-600 hover:bg-purple-500 transition-colors"
                    aria-label={isPlaying ? 'Pause audio' : 'Play audio'}
                  >
                    {isPlaying ? '⏸ Pause' : '▶ Play'}
                  </button>
                )}
              </div>
            </div>
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
            {ttsError && (
              <p className="mt-2 text-xs text-red-400">{ttsError}</p>
            )}
            {audioSrc && (
              <audio
                id={audioElementId}
                src={audioSrc}
                className="mt-3 w-full"
                onEnded={() => setIsPlaying(false)}
                preload="auto"
              />
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
      <CityPostsModal open={postsOpen} city={postsCity} posts={posts} onClose={() => setPostsOpen(false)} />
    </>
  )
}

