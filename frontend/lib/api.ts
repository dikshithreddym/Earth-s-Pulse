export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export async function fetchWithTimeout(input: RequestInfo, init: RequestInit = {}, timeout = 6000) {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeout)
  try {
    const response = await fetch(input, { signal: controller.signal, ...init })
    clearTimeout(id)
    return response
  } catch (err) {
    clearTimeout(id)
    throw err
  }
}

/**
 * Helper to fetch JSON with retries and timeout.
 * - url: string
 * - options: RequestInit
 * - attempts: number of retries (default 2)
 * - timeout: per-request timeout in ms
 */
export async function fetchJson(url: string, options: RequestInit = {}, attempts = 2, timeout = 6000) {
  let lastError: any = null
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await fetchWithTimeout(url, options, timeout)
      if (!res.ok) {
        const text = await res.text().catch(() => '')
        const err = new Error(`HTTP ${res.status}: ${text || res.statusText}`)
        ;(err as any).status = res.status
        throw err
      }
      const data = await res.json().catch(() => null)
      return data
    } catch (err) {
      lastError = err
      // small backoff
      await new Promise((r) => setTimeout(r, 250 * (i + 1)))
    }
  }
  throw lastError
}
