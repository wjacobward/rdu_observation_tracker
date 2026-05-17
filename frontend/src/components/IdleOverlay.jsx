export default function IdleOverlay({ paused, onDismiss }) {
  return (
    <div
      className="fixed inset-0 bg-black/75 flex items-center justify-center z-50 px-8"
      onClick={onDismiss}
    >
      <div className="bg-card border border-gray-700 rounded-2xl p-8 text-center space-y-4 w-full max-w-sm">
        <p className="text-2xl font-bold text-white">
          {paused ? 'Updates paused' : 'Still watching?'}
        </p>
        <p className="text-sm text-gray-400">
          {paused
            ? 'Live updates stopped to save API quota. Tap anywhere to resume.'
            : 'Tap to keep live flight updates running.'}
        </p>
        <button
          className="mt-2 w-full py-3 rounded-xl bg-gray-700 text-white font-semibold active:bg-gray-600 transition-colors"
          onClick={onDismiss}
        >
          {paused ? 'Resume' : "I'm here"}
        </button>
      </div>
    </div>
  )
}
