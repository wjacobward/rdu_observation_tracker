import { useEffect, useState } from 'react'
import { flightLabel, formatCountdown, formatTime } from '../utils/formatters'
import StatusBadge from './StatusBadge'

export default function NextFlight({ flight }) {
  const [, tick] = useState(0)
  useEffect(() => {
    const t = setInterval(() => tick(n => n + 1), 15_000)
    return () => clearInterval(t)
  }, [])

  if (!flight) {
    return (
      <div className="bg-card rounded-2xl p-6 text-center text-gray-500">
        No upcoming flights
      </div>
    )
  }

  const isArrival = flight.direction === 'arrival'
  const accentColor = isArrival ? 'text-emerald-400' : 'text-amber-400'
  const borderColor = isArrival ? 'border-emerald-400' : 'border-amber-400'
  const bgGlow = isArrival
    ? 'bg-gradient-to-br from-emerald-950/60 to-card'
    : 'bg-gradient-to-br from-amber-950/60 to-card'

  const displayTime = flight.actual_time || flight.estimated_time || flight.scheduled_time
  const isDelayed = flight.delay_minutes > 0 && flight.status !== 'landed' && flight.status !== 'departed'
  const countdown = formatCountdown(displayTime)

  return (
    <div className={`rounded-2xl border ${borderColor} ${bgGlow} p-5 space-y-3`}>
      {/* Direction label */}
      <div className="flex items-center justify-between">
        <span className={`text-xs font-bold uppercase tracking-[0.2em] ${accentColor}`}>
          {isArrival ? '▼ Arriving' : '▲ Departing'}
        </span>
        <StatusBadge status={flight.status} delayMinutes={flight.delay_minutes} />
      </div>

      {/* Airline + flight number */}
      <div className="text-3xl font-bold tracking-tight text-white leading-tight">
        {flightLabel(flight.flight_number, flight.airline_iata, flight.airline)}
      </div>

      {/* Origin / destination */}
      <div className="flex items-center gap-2 text-lg font-semibold text-white">
        <span>{isArrival ? 'from' : 'to'}</span>
        <span className={accentColor}>{flight.other_airport_city}</span>
        <span className="text-gray-500 text-sm font-normal">({flight.other_airport_iata})</span>
      </div>

      {/* Times */}
      <div className="flex items-center gap-3 text-sm">
        <span className="text-white font-semibold text-lg">{formatTime(displayTime)}</span>
        {isDelayed && (
          <>
            <span className="text-gray-500 line-through">{formatTime(flight.scheduled_time)}</span>
            <span className="text-yellow-500 text-xs">+{flight.delay_minutes}m</span>
          </>
        )}
      </div>

      {/* Countdown */}
      <div className={`text-2xl font-bold ${accentColor}`}>{countdown}</div>

      {/* Aircraft type + visibility */}
      <div className="flex items-center justify-between">
        {flight.aircraft_type && (
          <span className="text-xs text-gray-500 uppercase tracking-widest">
            {flight.aircraft_type}
          </span>
        )}
        <VisibilityBadge visible={flight.deck_visible} />
      </div>
    </div>
  )
}

function VisibilityBadge({ visible }) {
  if (visible === true)
    return <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-900/60 text-emerald-300">Visible from deck</span>
  if (visible === false)
    return <span className="text-xs px-2 py-0.5 rounded-full bg-gray-800 text-gray-500">Other runway</span>
  return null
}
