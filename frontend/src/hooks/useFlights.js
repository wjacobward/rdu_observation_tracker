import { useCallback, useEffect, useRef, useState } from 'react'

const POLL_INTERVAL_MS = 30_000
const IDLE_TIMEOUT_MS = 60 * 60 * 1000   // show prompt after 1 hour
const PROMPT_TIMEOUT_MS = 5 * 60 * 1000  // auto-pause if prompt ignored for 5 min

export function useFlights() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [showPrompt, setShowPrompt] = useState(false)
  const [paused, setPaused] = useState(false)

  // Refs so timer callbacks always see current values
  const pausedRef = useRef(false)
  const pollRef = useRef(null)
  const idleRef = useRef(null)
  const promptRef = useRef(null)

  const fetchFlights = useCallback(async () => {
    try {
      const res = await fetch('/api/flights')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      setData(await res.json())
      setLastUpdated(new Date())
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }, [])

  const startIdleTimer = useCallback(() => {
    clearTimeout(idleRef.current)
    clearTimeout(promptRef.current)
    idleRef.current = setTimeout(() => {
      setShowPrompt(true)
      promptRef.current = setTimeout(() => {
        pausedRef.current = true
        setPaused(true)
        setShowPrompt(false)
      }, PROMPT_TIMEOUT_MS)
    }, IDLE_TIMEOUT_MS)
  }, [])

  // Called when user confirms they're still there, or taps while paused
  const activate = useCallback(() => {
    pausedRef.current = false
    setPaused(false)
    setShowPrompt(false)
    startIdleTimer()
    fetchFlights()
  }, [startIdleTimer, fetchFlights])

  useEffect(() => {
    fetchFlights()
    startIdleTimer()

    pollRef.current = setInterval(() => {
      if (!document.hidden && !pausedRef.current) {
        fetchFlights()
      }
    }, POLL_INTERVAL_MS)

    const onVisibility = () => {
      if (document.hidden) {
        // Screen off / app backgrounded — freeze the idle clock
        clearTimeout(idleRef.current)
        clearTimeout(promptRef.current)
        setShowPrompt(false)
      } else if (!pausedRef.current) {
        // Returned to the app — restart idle clock and fetch immediately
        startIdleTimer()
        fetchFlights()
      }
    }

    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      clearInterval(pollRef.current)
      clearTimeout(idleRef.current)
      clearTimeout(promptRef.current)
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [fetchFlights, startIdleTimer])

  return { data, error, lastUpdated, showPrompt, paused, activate, refresh: activate }
}
