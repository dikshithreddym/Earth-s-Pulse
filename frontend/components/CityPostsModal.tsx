import React from 'react'

interface Post {
  platform?: string
  text: string
  url?: string
  author?: string
  score: number
  label: string
  timestamp?: string
}

export default function CityPostsModal({
  open,
  city,
  posts,
  onClose
}: {
  open: boolean
  city?: string
  posts: Post[]
  onClose: () => void
}) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-gray-900 w-full max-w-2xl rounded-lg p-4 border border-gray-700 shadow-xl">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-lg text-white truncate">
            Posts for {city}
          </h3>
          <button
            onClick={onClose}
            className="px-2 py-1 text-sm rounded bg-gray-700 hover:bg-gray-600"
          >
            Close
          </button>
        </div>
        <div className="max-h-[65vh] overflow-y-auto space-y-3 pr-1">
          {posts.length === 0 && (
            <div className="text-sm text-gray-400">No posts captured.</div>
          )}
          {posts.map((p, i) => (
            <div key={i} className="border border-gray-700 rounded p-2 bg-gray-800/50">
              <div className="text-xs text-gray-400 mb-1 flex flex-wrap gap-2">
                <span>{p.platform || 'unknown'}</span>
                <span>{p.label}</span>
                <span>{p.score.toFixed(3)}</span>
                {p.author && <span>by {p.author}</span>}
                {p.timestamp && <span>{new Date(p.timestamp).toLocaleTimeString()}</span>}
              </div>
              <p className="text-sm text-gray-200 whitespace-pre-wrap">{p.text}</p>
              {p.url && (
                <a
                  href={p.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-blue-400 hover:underline mt-1 inline-block"
                >
                  Open source
                </a>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}