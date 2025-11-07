'use client'

import { useEffect, useRef, useState } from 'react'
import { MoodPoint } from '@/types/mood'

interface GlobeComponentProps {
  moods: MoodPoint[]
  loading: boolean
}

export default function GlobeComponent({ moods, loading }: GlobeComponentProps) {
  const globeEl = useRef<HTMLDivElement>(null)
  const globeInstance = useRef<any>(null)
  const [globeLoaded, setGlobeLoaded] = useState(false)

  useEffect(() => {
    if (!globeEl.current || typeof window === 'undefined') return

    let resizeTimeout: NodeJS.Timeout | null = null
    let cleanupResize: (() => void) | null = null

    // Simple centering function - let the library handle sizing naturally
    const centerCanvas = () => {
      const canvas = globeEl.current?.querySelector('canvas')
      if (canvas) {
        // Simply center the canvas without interfering with library's sizing
        canvas.style.margin = '0 auto'
        canvas.style.display = 'block'
        canvas.style.position = 'absolute'
        canvas.style.top = '50%'
        canvas.style.left = '50%'
        canvas.style.transform = 'translate(-50%, -50%)'
      }
    }

    // Re-center on window resize
    const handleResize = () => {
      centerCanvas()
    }

    // Dynamically import and initialize globe
    import('globe.gl').then((GlobeModule) => {
      const Globe = GlobeModule.default
      const globe = new Globe(globeEl.current!)
      globeInstance.current = globe
      setGlobeLoaded(true)

      // Globe configuration with detailed world map
      // Using a high-resolution world map that shows countries clearly
      // Try alternative Earth texture URLs if the first one doesn't load
      const earthTextureUrl = 'https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg'
      
      globe
        .globeImageUrl(earthTextureUrl)
        .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
        .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
        .showAtmosphere(true)
        .showGraticules(false)
        .enablePointerInteraction(true)

      // Point of view - closer to see the Earth map better
      globe.pointOfView({ lat: 0, lng: 0, altitude: 2.0 })

      // Center and size the canvas element created by globe.gl after initialization
      // Use multiple timeouts to ensure the canvas is fully initialized
      setTimeout(() => {
        centerCanvas()
      }, 100)
      
      setTimeout(() => {
        centerCanvas() // Second attempt after library fully initializes
      }, 500)
      
      // Add resize listener with debouncing for better performance
      const debouncedResize = () => {
        if (resizeTimeout) clearTimeout(resizeTimeout)
        resizeTimeout = setTimeout(() => {
          handleResize()
        }, 150)
      }
      
      window.addEventListener('resize', debouncedResize)
      
      // Store cleanup function
      cleanupResize = () => {
        if (resizeTimeout) clearTimeout(resizeTimeout)
        window.removeEventListener('resize', debouncedResize)
      }
      
      // Force refresh the globe texture after a delay to ensure it loads
      setTimeout(() => {
        if (globeInstance.current) {
          // Re-apply the globe image to ensure it loads
          globeInstance.current.globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
          // Re-center and resize after texture loads
          centerCanvas()
        }
      }, 1000)
    }).catch((error) => {
      console.error('Error loading globe:', error)
    })

    // Cleanup
    return () => {
      if (cleanupResize) cleanupResize()
      if (globeInstance.current) {
        globeInstance.current._destructor?.()
      }
    }
  }, [])

  // Update globe - removed all points and rings to show clean Earth map
  useEffect(() => {
    if (!globeInstance.current || loading || !globeLoaded) return

    // Remove all points and rings - just show the Earth map
    globeInstance.current
      .pointsData([])
      .ringsData([])

  }, [moods, loading, globeLoaded])

  return (
    <div 
      ref={globeEl} 
      className="w-full h-full min-h-0 globe-container"
      style={{ 
        background: 'radial-gradient(ellipse at center, #1a1a2e 0%, #000000 100%)',
        position: 'relative',
        margin: '0 auto',
        overflow: 'hidden',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    />
  )
}

// Helper function to get color based on sentiment score
function getColorForSentiment(score: number): string {
  if (score > 0.3) {
    return '#22c55e' // Green for positive
  } else if (score < -0.3) {
    return '#ef4444' // Red for negative
  } else {
    return '#eab308' // Yellow for neutral
  }
}

