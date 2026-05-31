export default function ShimmerBlock({ lines = 4 }: { lines?: number }) {
  return (
    <div className="glass-card p-5 mb-4 animate-pulse">
      <div className="h-4 w-1/3 bg-white/5 rounded mb-3" />
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-3 bg-white/5 rounded mb-2"
          style={{ width: `${75 + Math.random() * 25}%` }}
        />
      ))}
    </div>
  );
}
