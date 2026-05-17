import FlightCard from './FlightCard'

export default function FlightList({ flights }) {
  if (!flights || flights.length === 0) {
    return (
      <p className="text-center text-gray-600 text-sm py-6">
        No further flights in the next 6 hours
      </p>
    )
  }

  return (
    <div className="space-y-2">
      {flights.map((flight) => (
        <FlightCard key={`${flight.flight_number}-${flight.scheduled_time}`} flight={flight} />
      ))}
    </div>
  )
}
