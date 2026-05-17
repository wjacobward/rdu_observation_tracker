import { flightLabel, formatCountdown, formatTime } from '../utils/formatters'
import StatusBadge from './StatusBadge'

export default function FlightCard({ flight }) {
  const isArrival = flight.direction === 'arrival'
  const accentColor = isArrival ? 'text-emerald-400' : 'text-amber-400'
  const displayTime = flight.actual_time || flight.estimated_time || flight.scheduled_time
  const isDelayed = flight.delay_minutes > 0 && flight.status !== 'landed' && flight.status !== 'departed'
  const notVisible = flight.deck_visible === false

  return (
    <div className={`bg-card rounded-xl p-4 space-y-1.5 ${notVisible ? 'opacity-40' : ''}`}>
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
        <span className="text-xs text-gray-500">
          {flight.aircraft_type || flight.aircraft_code || ''}
        </span>
        <div className="flex items-center gap-2">
          {flight.deck_visible === true && (
            <span className="text-xs text-emerald-600">visible</span>
          )}
          <span className="text-xs text-gray-500">{formatCountdown(displayTime)}</span>
        </div>
      </div>
    </div>
  )
}
