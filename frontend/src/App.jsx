import FlightList from './components/FlightList'
import IdleOverlay from './components/IdleOverlay'
import NextFlight from './components/NextFlight'
import { useFlights } from './hooks/useFlights'

function formatUpdated(date) {
  if (!date) return ''
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit', hour12: true })
}

export default function App() {
  const { data, error, lastUpdated, refresh, showPrompt, paused, activate } = useFlights()

  return (
    <div className="min-h-screen bg-surface px-4 pb-8 pt-safe">
      {(showPrompt || paused) && <IdleOverlay paused={paused} onDismiss={activate} />}
      {/* Header */}
      <header className="flex items-center justify-between py-4 mb-1">
        <div>
          <h1 className="text-sm font-bold tracking-[0.3em] uppercase text-gray-400">RDU</h1>
          <p className="text-xs text-gray-600">Observation Deck</p>
        </div>
        <button
          onClick={refresh}
          className="text-xs active:text-gray-300 transition-colors px-2 py-1"
          aria-label="Refresh"
        >
          {paused
            ? <span className="text-yellow-600">paused — tap to resume</span>
            : <span className="text-gray-600">↻ {lastUpdated ? formatUpdated(lastUpdated) : 'loading…'}</span>
          }
        </button>
      </header>

      {/* Error banner */}
      {error && (
        <div className="bg-red-950 border border-red-800 rounded-xl px-4 py-3 mb-4 text-sm text-red-300">
          Unable to load flight data — showing last known information
        </div>
      )}

      {/* Loading state */}
      {!data && !error && (
        <div className="flex items-center justify-center h-48 text-gray-600 text-sm">
          Loading flights…
        </div>
      )}

      {data && (
        <>
          {/* Next flight — prominent */}
          <section className="mb-5">
            <p className="text-xs text-gray-600 uppercase tracking-widest mb-2">Next Up</p>
            <NextFlight flight={data.next_flight} />
          </section>

          {/* Upcoming list */}
          <section>
            <p className="text-xs text-gray-600 uppercase tracking-widest mb-2">
              Upcoming — {data.upcoming.length} flight{data.upcoming.length !== 1 ? 's' : ''}
            </p>
            <FlightList flights={data.upcoming} />
          </section>
        </>
      )}
    </div>
  )
}
