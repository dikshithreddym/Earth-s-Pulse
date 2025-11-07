'use client'

import { useMemo, useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { MoodPoint } from '@/types/mood'

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { 
  ssr: false,
  loading: () => <div className="w-full h-48 flex items-center justify-center text-gray-400 text-sm">Loading chart...</div>
})

interface TrendChartProps {
  moods: MoodPoint[]
}

export default function TrendChart({ moods }: TrendChartProps) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])
  const chartData = useMemo(() => {
    if (moods.length === 0) {
      return {
        labels: [],
        positive: [],
        neutral: [],
        negative: []
      }
    }

    // Group by time buckets (last 24 hours, 1-hour intervals)
    const now = new Date()
    const buckets: { [key: string]: MoodPoint[] } = {}
    
    moods.forEach(mood => {
      const moodTime = mood.timestamp ? new Date(mood.timestamp) : now
      const hoursAgo = Math.floor((now.getTime() - moodTime.getTime()) / (1000 * 60 * 60))
      const bucket = Math.min(23, Math.max(0, hoursAgo))
      const key = `${bucket}h`
      
      if (!buckets[key]) {
        buckets[key] = []
      }
      buckets[key].push(mood)
    })

    // Create labels (hours ago)
    const labels = Array.from({ length: 24 }, (_, i) => `${23 - i}h`)
    
    // Count sentiments per bucket
    const positive = labels.map(label => {
      const bucketMoods = buckets[label] || []
      return bucketMoods.filter(m => m.score > 0.3).length
    })
    
    const neutral = labels.map(label => {
      const bucketMoods = buckets[label] || []
      return bucketMoods.filter(m => m.score >= -0.3 && m.score <= 0.3).length
    })
    
    const negative = labels.map(label => {
      const bucketMoods = buckets[label] || []
      return bucketMoods.filter(m => m.score < -0.3).length
    })

    return { labels, positive, neutral, negative }
  }, [moods])

  const plotData = [
    {
      x: chartData.labels,
      y: chartData.positive,
      name: 'Positive',
      type: 'scatter' as const,
      mode: 'lines+markers' as const,
      line: { color: '#22c55e', width: 2.5, shape: 'spline' },
      marker: { color: '#22c55e', size: 5, line: { color: '#16a34a', width: 1 } }
    },
    {
      x: chartData.labels,
      y: chartData.neutral,
      name: 'Neutral',
      type: 'scatter' as const,
      mode: 'lines+markers' as const,
      line: { color: '#eab308', width: 2.5, shape: 'spline' },
      marker: { color: '#eab308', size: 5, line: { color: '#ca8a04', width: 1 } }
    },
    {
      x: chartData.labels,
      y: chartData.negative,
      name: 'Negative',
      type: 'scatter' as const,
      mode: 'lines+markers' as const,
      line: { color: '#ef4444', width: 2.5, shape: 'spline' },
      marker: { color: '#ef4444', size: 5, line: { color: '#dc2626', width: 1 } }
    }
  ]

  const layout = useMemo(() => ({
    autosize: true,
    height: isMobile ? 180 : 220,
    margin: { 
      l: isMobile ? 35 : 45, 
      r: isMobile ? 15 : 25, 
      t: isMobile ? 15 : 25, 
      b: isMobile ? 35 : 45 
    },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { 
      color: '#9ca3af', 
      size: isMobile ? 9 : 11, 
      family: 'Inter, system-ui, sans-serif' 
    },
    xaxis: {
      title: {
        text: 'Time (hours ago)',
        font: { 
          size: isMobile ? 9 : 11, 
          color: '#9ca3af' 
        }
      },
      gridcolor: 'rgba(255,255,255,0.08)',
      linecolor: 'rgba(255,255,255,0.2)',
      tickfont: { 
        size: isMobile ? 8 : 10, 
        color: '#6b7280' 
      }
    },
    yaxis: {
      title: {
        text: 'Count',
        font: { 
          size: isMobile ? 9 : 11, 
          color: '#9ca3af' 
        }
      },
      gridcolor: 'rgba(255,255,255,0.08)',
      linecolor: 'rgba(255,255,255,0.2)',
      tickfont: { 
        size: isMobile ? 8 : 10, 
        color: '#6b7280' 
      }
    },
    legend: {
      orientation: 'h' as const,
      y: isMobile ? -0.3 : -0.25,
      x: 0.5,
      xanchor: 'center',
      font: { 
        size: isMobile ? 8 : 10, 
        color: '#9ca3af' 
      },
      bgcolor: 'rgba(0,0,0,0)',
      bordercolor: 'rgba(255,255,255,0.1)',
      borderwidth: 1
    },
    hovermode: 'x unified' as const,
    hoverlabel: {
      bgcolor: 'rgba(17, 24, 39, 0.95)',
      bordercolor: 'rgba(148, 163, 184, 0.3)',
      font: { 
        size: isMobile ? 9 : 11, 
        color: '#fff' 
      }
    }
  }), [isMobile])

  const config = {
    displayModeBar: false,
    responsive: true
  }

  return (
    <div className="w-full overflow-hidden">
      <Plot
        data={plotData}
        layout={layout}
        config={config}
        style={{ width: '100%', height: isMobile ? '160px' : '200px', maxWidth: '100%' }}
        useResizeHandler={true}
      />
    </div>
  )
}

