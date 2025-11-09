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
  const [selectedPoint, setSelectedPoint] = useState<any>(null)

  useEffect(() => {
    if (!globeEl.current || typeof window === 'undefined') return

    let resizeTimeout: NodeJS.Timeout | null = null
    let cleanupResize: (() => void) | null = null

    // Ensure globe container and canvas are properly sized
    const setupGlobeSize = () => {
      const container = globeEl.current
      const canvas = container?.querySelector('canvas')
      
      if (container && canvas && globeInstance.current) {
        // Ensure container takes full available space
        const containerWidth = container.clientWidth || window.innerWidth
        const containerHeight = container.clientHeight || window.innerHeight
        
        // Calculate appropriate globe size (80% of smallest dimension, max 1000px)
        const globeSize = Math.min(containerWidth, containerHeight) * 0.8
        const finalSize = Math.min(globeSize, 1000)
        
        // Set canvas size directly - globe.gl should respect this
        canvas.width = finalSize
        canvas.height = finalSize
        
        // Center the canvas
        canvas.style.position = 'absolute'
        canvas.style.top = '50%'
        canvas.style.left = '50%'
        canvas.style.transform = 'translate(-50%, -50%)'
        canvas.style.display = 'block'
        
        // Force Three.js renderer to update size
        try {
          const renderer = (globeInstance.current as any).renderer?.()
          if (renderer) {
            renderer.setSize(finalSize, finalSize, false)
          }
        } catch (e) {
          console.log('Could not update renderer size:', e)
        }
      }
    }

    // Re-size and center on window resize
    const handleResize = () => {
      setupGlobeSize()
    }

    // Dynamically import and initialize globe
    import('globe.gl').then((GlobeModule) => {
      const Globe = GlobeModule.default
      const globe = new Globe(globeEl.current!)
      globeInstance.current = globe
      setGlobeLoaded(true)

      // Globe configuration with detailed world map
      // Using a texture that shows countries clearly
      // Try earth-day.jpg or earth-blue-marble.jpg - both show countries
      const earthTextureUrl = 'https://unpkg.com/three-globe/example/img/earth-day.jpg'
      
      // Configure globe safely - guard each method since different
      // builds (mjs/cjs) or multiple three instances can make methods undefined.
      try {
        if (typeof globe.globeImageUrl === 'function') globe.globeImageUrl(earthTextureUrl)
        if (typeof globe.bumpImageUrl === 'function') globe.bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
        if (typeof globe.backgroundImageUrl === 'function') globe.backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
        if (typeof globe.showAtmosphere === 'function') globe.showAtmosphere(false)
        if (typeof globe.showGraticules === 'function') {
          globe.showGraticules(true)
          if (typeof (globe as any).graticuleDashLength === 'function') (globe as any).graticuleDashLength(0.4)
          if (typeof (globe as any).graticuleDashGap === 'function') (globe as any).graticuleDashGap(0.1)
          if (typeof (globe as any).graticuleDashAnimateTime === 'function') (globe as any).graticuleDashAnimateTime(4000)
        }
        if (typeof globe.enablePointerInteraction === 'function') globe.enablePointerInteraction(true)
        if (typeof globe.onGlobeClick === 'function') globe.onGlobeClick(() => setSelectedPoint(null))
      } catch (e) {
        console.warn('Globe configuration guarded calls failed:', e)
      }

      // Point of view - centered on Americas to show North and South American cities
      // Delay pointOfView to ensure globe is fully initialized
      setTimeout(() => {
        if (globeInstance.current) {
          globeInstance.current.pointOfView({ lat: 15, lng: -90, altitude: 2.0 })
        }
      }, 100)
      
      // Try to load country borders for better visibility
      // Using a direct GeoJSON source (simpler than TopoJSON)
      fetch('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson')
        .then(res => res.json())
        .then((geoData) => {
          if (geoData && geoData.features && globeInstance.current) {
            try {
              const g = globeInstance.current
              if (typeof g.polygonsData === 'function') g.polygonsData(geoData.features)
              if (typeof g.polygonCapColor === 'function') g.polygonCapColor(() => 'rgba(0, 0, 0, 0)')
              if (typeof g.polygonSideColor === 'function') g.polygonSideColor(() => 'rgba(0, 0, 0, 0)')
              if (typeof g.polygonStrokeColor === 'function') g.polygonStrokeColor(() => 'rgba(255, 255, 255, 0.4)')
              if (typeof g.polygonAltitude === 'function') g.polygonAltitude(0)
              if (typeof g.polygonStrokeWidth === 'function') g.polygonStrokeWidth(0.5)
            } catch (e) {
              console.log('Could not set polygon data safely:', e)
            }
          }
        })
        .catch((error) => {
          console.log('Could not fetch country borders, using texture only:', error)
        })

      // Setup globe size and center after initialization
      // Use multiple timeouts to ensure the canvas is fully initialized
      setTimeout(() => {
        setupGlobeSize()
      }, 100)
      
      setTimeout(() => {
        setupGlobeSize() // Second attempt after library fully initializes
      }, 500)
      
      setTimeout(() => {
        setupGlobeSize() // Third attempt to ensure it's properly sized
      }, 1000)
      
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
          try {
            if (typeof globeInstance.current.globeImageUrl === 'function') {
              globeInstance.current.globeImageUrl('https://unpkg.com/three-globe/example/img/earth-day.jpg')
            }
          } catch (e) {
            console.log('Could not re-apply globe image safely:', e)
          }
          // Re-size and center after texture loads
          setupGlobeSize()
        }
      }, 1500)
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

  // Update globe with mood-based coloring using points
  useEffect(() => {
    if (!globeInstance.current || loading || !globeLoaded) return

    if (moods.length === 0) {
      // Clear all data if no moods - guard each call
      try {
        const g = globeInstance.current
        if (g) {
          if (typeof g.pointsData === 'function') g.pointsData([])
          if (typeof g.polygonsData === 'function') g.polygonsData([])
          if (typeof g.arcsData === 'function') g.arcsData([])
        }
      } catch (e) {
        console.log('Could not clear globe data safely:', e)
      }
      return
    }

    // Helper function to calculate distance between two coordinates
    const calculateDistance = (lat1: number, lng1: number, lat2: number, lng2: number): number => {
      const R = 6371 // Earth's radius in km
      const dLat = (lat2 - lat1) * Math.PI / 180
      const dLng = (lng2 - lng1) * Math.PI / 180
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLng / 2) * Math.sin(dLng / 2)
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
      return R * c
    }

    // Group moods by city for aggregation and gradient coloring
    const cityMoods: { [key: string]: any[] } = {}
    moods.forEach(mood => {
      const cityKey = mood.city_name || `${mood.lat.toFixed(2)},${mood.lng.toFixed(2)}`
      if (!cityMoods[cityKey]) {
        cityMoods[cityKey] = []
      }
      cityMoods[cityKey].push(mood)
    })

    // Calculate average sentiment per city for gradient effect
    // We'll use larger, more visible points to show the gradient
    const cityAverages: { [key: string]: number } = {}
    Object.entries(cityMoods).forEach(([cityKey, cityMoodPoints]) => {
      const avgScore = cityMoodPoints.reduce((sum, m) => sum + m.score, 0) / cityMoodPoints.length
      cityAverages[cityKey] = avgScore
    })

    // Create colored points based on mood sentiment - use city_name from backend
    // Use average city sentiment for gradient effect (larger size for stronger sentiment)
    const moodPoints = moods.map(mood => {
      const cityKey = mood.city_name || `${mood.lat.toFixed(2)},${mood.lng.toFixed(2)}`
      const avgCityScore = cityAverages[cityKey] || mood.score
      const color = getColorForSentiment(avgCityScore) // Use average for gradient
      const size = 1.5 + Math.abs(avgCityScore) * 1.5 // Larger size for stronger sentiment
      
      return {
        lat: mood.lat,
        lng: mood.lng,
        size: size,
        color: color,
        score: mood.score,
        label: mood.label,
        source: mood.source,
        text: mood.text || '',
        cityName: mood.city_name || 'Unknown Location',
        avgCityScore: avgCityScore
      }
    })
    
    // Store point data globally for click detection
    ;(window as any).__globePointData = moodPoints

    // Create HTML labels for selected points
    const htmlLabels = selectedPoint ? [{
      lat: selectedPoint.lat,
      lng: selectedPoint.lng,
      text: selectedPoint.cityName || 'Location',
      size: 1.2,
      color: selectedPoint.color
    }] : []

    // Update globe with points, polygons for gradient, and HTML labels
    try {
      // Add click handler for points
      globeInstance.current
        .pointsData(moodPoints)
        .pointColor('color')
        .pointRadius('size')
        .pointAltitude(0.01)
        .pointResolution(3)
        .onPointClick((point: any) => {
          if (!point) return
          
          // Set selected point
          setSelectedPoint(point)
          
          // Rotate globe to focus on the clicked point
          if (globeInstance.current) {
            try {
              // Ensure globe is fully initialized before calling pointOfView
              const currentGlobe = globeInstance.current
              if (currentGlobe && typeof currentGlobe.pointOfView === 'function') {
                currentGlobe.pointOfView(
                  { 
                    lat: point.lat, 
                    lng: point.lng, 
                    altitude: 1.5
                  },
                  1000
                )
              }
            } catch (error) {
              console.log('Error rotating globe to point:', error)
            }
          }
        })
        .pointLabel(() => '') // Disable default point labels

      // Clear rings to avoid errors (user doesn't want spikes/rings)
      // Don't clear polygons - we need country borders to stay visible
      globeInstance.current.ringsData([])

      // Add HTML labels for selected points
      globeInstance.current
        .htmlElementsData(htmlLabels)
        .htmlElement((d: any) => {
          if (!d || !selectedPoint) return null
          
          const sentimentColor = selectedPoint.color || getColorForSentiment(selectedPoint.score || 0)
          const sentimentLabel = selectedPoint.score > 0.3 ? 'Positive' : selectedPoint.score < -0.3 ? 'Negative' : 'Neutral'
          
          const el = document.createElement('div')
          el.innerHTML = `
            <div style="
              background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.95));
              backdrop-filter: blur(10px);
              color: white;
              padding: 12px 16px;
              border-radius: 8px;
              font-size: 12px;
              border: 2px solid ${sentimentColor};
              max-width: 280px;
              box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
              position: relative;
              pointer-events: auto;
            ">
              <div style="
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid ${sentimentColor};
              "></div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: ${sentimentColor}; box-shadow: 0 0 8px ${sentimentColor};"></div>
                <strong style="font-size: 14px; color: ${sentimentColor};">${selectedPoint.cityName || 'Location'}</strong>
              </div>
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">
                Sentiment: <span style="color: ${sentimentColor}; font-weight: 600;">${sentimentLabel}</span>
              </div>
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">
                Emotion: <span style="color: ${sentimentColor}; font-weight: 600;">${selectedPoint.label || 'neutral'}</span>
              </div>
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">
                Score: <span style="color: ${sentimentColor}; font-weight: 600;">${(selectedPoint.score || 0) >= 0 ? '+' : ''}${(selectedPoint.score || 0).toFixed(2)}</span>
              </div>
              <div style="font-size: 10px; color: #64748b; margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                Source: ${selectedPoint.source || 'unknown'}
              </div>
            </div>
          `
          el.style.pointerEvents = 'auto'
          return el
        })

      // Clear arcs
      globeInstance.current.arcsData([])
    } catch (error) {
      console.error('Error updating globe data:', error)
    }

  }, [moods, loading, globeLoaded, selectedPoint])

  // Helper function to get region from coordinates
  function getRegionFromCoordinates(lat: number, lng: number): string {
    // Simplified region mapping - you can expand this with actual country boundaries
    if (lat >= 24 && lat <= 71 && lng >= -180 && lng <= -30) return 'North America'
    if (lat >= -56 && lat <= 12 && lng >= -90 && lng <= -30) return 'South America'
    if (lat >= 35 && lat <= 71 && lng >= -10 && lng <= 40) return 'Europe'
    if (lat >= -10 && lat <= 55 && lng >= 60 && lng <= 150) return 'Asia'
    if (lat >= -40 && lat <= -10 && lng >= 110 && lng <= 155) return 'Australia'
    if (lat >= -35 && lat <= 37 && lng >= -20 && lng <= 50) return 'Africa'
    return 'Other'
  }

  // Helper function to get region center coordinates
  function getRegionCenter(region: string): { lat: number; lng: number } | null {
    const centers: { [key: string]: { lat: number; lng: number } } = {
      'North America': { lat: 45, lng: -100 },
      'South America': { lat: -20, lng: -60 },
      'Europe': { lat: 54, lng: 15 },
      'Asia': { lat: 30, lng: 100 },
      'Australia': { lat: -25, lng: 133 },
      'Africa': { lat: 0, lng: 20 },
      'Other': { lat: 0, lng: 0 }
    }
    return centers[region] || null
  }

  // Helper function to get region polygon coordinates
  function getRegionPolygon(region: string): any | null {
    // Simplified polygon boundaries - in production, use actual country/region GeoJSON
    const polygons: { [key: string]: any } = {
      'North America': {
        name: 'North America',
        coordinates: [
          [[-180, 24], [-180, 71], [-30, 71], [-30, 24], [-180, 24]]
        ]
      },
      'South America': {
        name: 'South America',
        coordinates: [
          [[-90, -56], [-90, 12], [-30, 12], [-30, -56], [-90, -56]]
        ]
      },
      'Europe': {
        name: 'Europe',
        coordinates: [
          [[-10, 35], [-10, 71], [40, 71], [40, 35], [-10, 35]]
        ]
      },
      'Asia': {
        name: 'Asia',
        coordinates: [
          [[60, -10], [60, 55], [150, 55], [150, -10], [60, -10]]
        ]
      },
      'Australia': {
        name: 'Australia',
        coordinates: [
          [[110, -40], [110, -10], [155, -10], [155, -40], [110, -40]]
        ]
      },
      'Africa': {
        name: 'Africa',
        coordinates: [
          [[-20, -35], [-20, 37], [50, 37], [50, -35], [-20, -35]]
        ]
      }
    }
    return polygons[region] || null
  }

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

