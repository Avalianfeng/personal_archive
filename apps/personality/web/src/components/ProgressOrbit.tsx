interface ProgressOrbitProps {
  current: number;
  total: number;
}

export default function ProgressOrbit({ current, total }: ProgressOrbitProps) {
  const progress = total > 0 ? current / total : 0;
  const circumference = 2 * Math.PI * 14;
  const offset = circumference * (1 - progress);

  return (
    <div className="flex items-center gap-2">
      <svg width="32" height="32" viewBox="0 0 32 32" className="rotate-[-90deg]">
        <circle
          cx="16"
          cy="16"
          r="14"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-white/10"
        />
        <circle
          cx="16"
          cy="16"
          r="14"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          className="text-accent-glow transition-all duration-500"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <span className="text-xs text-star-dim tabular-nums">
        {current}/{total}
      </span>
    </div>
  );
}
