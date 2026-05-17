/**
 * "AA4458" + "AA" → "American Airlines 4458"
 */
export function flightLabel(flightNumber, airlineIata, airlineName) {
  const digits = airlineIata
    ? flightNumber.replace(new RegExp(`^${airlineIata}`, 'i'), '').trim()
    : flightNumber
  return `${airlineName} ${digits}`
}

/**
 * Format a UTC ISO string to local time, e.g. "3:47 PM"
 */
export function formatTime(isoString) {
  if (!isoString) return '—'
  const d = new Date(isoString)
  return d.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  })
}

/**
 * Returns a human-readable countdown string, e.g. "in 12 min" or "4 min ago"
 */
export function formatCountdown(isoString) {
  if (!isoString) return ''
  const diff = Math.round((new Date(isoString) - Date.now()) / 1000)
  const abs = Math.abs(diff)

  if (abs < 60) return diff >= 0 ? 'now' : 'just now'
  const mins = Math.floor(abs / 60)
  if (abs < 3600) return diff >= 0 ? `in ${mins} min` : `${mins} min ago`
  const hrs = Math.floor(abs / 3600)
  const rem = Math.floor((abs % 3600) / 60)
  const label = rem > 0 ? `${hrs}h ${rem}m` : `${hrs}h`
  return diff >= 0 ? `in ${label}` : `${label} ago`
}

export function statusLabel(status, delayMin) {
  switch (status) {
    case 'cancelled': return 'Cancelled'
    case 'landed':    return 'Landed'
    case 'departed':  return 'Departed'
    case 'en_route':  return 'En Route'
    case 'delayed':   return `Delayed ${delayMin ? `+${delayMin}m` : ''}`
    case 'scheduled': return 'On Time'
    default:          return status.replace('_', ' ')
  }
}

export function statusColor(status) {
  switch (status) {
    case 'cancelled': return 'text-red-400'
    case 'delayed':   return 'text-yellow-400'
    case 'landed':
    case 'departed':  return 'text-gray-400'
    case 'en_route':  return 'text-blue-400'
    default:          return 'text-emerald-400'
  }
}
