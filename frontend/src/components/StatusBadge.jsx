import { statusColor, statusLabel } from '../utils/formatters'

export default function StatusBadge({ status, delayMinutes }) {
  return (
    <span className={`text-xs font-bold uppercase tracking-widest ${statusColor(status)}`}>
      {statusLabel(status, delayMinutes)}
    </span>
  )
}
