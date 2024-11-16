export function PendingComponent() {
  return (
    <div className="flex grow flex-col items-center justify-center">
      <img className="h-auto w-[320px]" src="/dodo-loading-src.gif" />
      <span className="animate-pulse text-xl font-semibold opacity-75">
        Loading...
      </span>
    </div>
  )
}
