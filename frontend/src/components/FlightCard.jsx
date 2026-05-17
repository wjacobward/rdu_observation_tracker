import { useState } from 'react'
import { flightLabel, formatCountdown, formatTime } from '../utils/formatters'
import StatusBadge from './StatusBadge'

export default function FlightCard({ flight }) {
  const [expanded, setExpanded] = useState(false)
  const isArrival = flight.direction === 'arrival'
  const accentColor = isArrival ? 'text-emerald-400' : 'text-amber-400'
  const displayTime = flight.actual_time || flight.estimated_time || flight.scheduled_time
  const isDelayed = flight.delay_minutes > 0 && flight.status !== 'landed' && flight.status !== 'departed'
  const notVisible = flight.deck_visible === false

  return (
    <div
      className={`bg-card rounded-xl p-4 space-y-1.5 ${notVisible ? 'opacity-40' : ''} ${flight.photo_url ? 'cursor-pointer' : ''}`}
      onClick={() => flight.photo_url && setExpanded(e => !e)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={`text-xs font-bold ${accentColor}`}>
            {isArrival ? '▼' : '▲'}
          </span>
          <span className="text-sm font-bold text-white">
            {flightLabel(flight.flight_number, flight.airline_iata, flight.airline)}
          </span>
        </div>
        <StatusBadge status={flight.status} delayMinutes={flight.delay_minutes} />
      </div>

      <div className="flex items-center justify-between">
        <div>
          <span className="text-xs text-gray-400">{isArrival ? 'from ' : 'to '}</span>
          <span className="text-sm text-gray-200">
            {flight.other_airport_city}
            <span className="text-gray-500 ml-1">({flight.other_airport_iata})</span>
          </span>
        </div>
        <div className="text-right">
          <div className="text-sm font-semibold text-white">{formatTime(displayTime)}</div>
          {isDelayed && (
            <div className="text-xs text-gray-500 line-through">{formatTime(flight.scheduled_time)}</div>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-500 flex items-center gap-1">
          {flight.aircraft_type || flight.aircraft_code || ''}
          {flight.photo_url && (
            <svg className="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
            </svg>
          )}
        </span>
        <div className="flex items-center gap-2">
          {flight.deck_visible === true && (
            <span className="text-xs text-emerald-600">visible</span>
          )}
          <span className="text-xs text-gray-500">{formatCountdown(displayTime)}</span>
        </div>
      </div>

      {expanded && flight.photo_url && (
        <div className="pt-2 space-y-1" onClick={e => e.stopPropagation()}>
          <a href={flight.photo_link} target="_blank" rel="noopener noreferrer">
            <img
              src={flight.photo_url}
              alt={`${flight.airline} aircraft`}
              className="w-full rounded-lg object-cover aspect-[3/2]"
            />
          </a>
          <p className="text-[10px] text-gray-500">
            {'© '}
            <a
              href={flight.photo_link}
              target="_blank"
              rel="noopener noreferrer"
              className="underline"
            >
              {flight.photo_photographer}
            </a>
            {' / Planespotters.net'}
          </p>
        </div>
      )}
    </div>
  )
}
