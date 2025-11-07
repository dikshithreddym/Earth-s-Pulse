"use client"

import { useEffect } from 'react'

export default function ClientSideEffects() {
  useEffect(() => {
    if (typeof document === 'undefined' || !document?.body) return

    // Remove server-injected attributes that cause hydration warnings.
    // These attribute names were observed in the console warnings.
    try {
      document.body.removeAttribute('__processed_c30512ed-2685-49c0-b188-f2fa19c74bbd__')
      document.body.removeAttribute('bis_register')
    } catch (e) {
      // ignore errors silently
    }
  }, [])

  return null
}
