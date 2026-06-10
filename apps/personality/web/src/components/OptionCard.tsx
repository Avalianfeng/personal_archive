import { motion } from 'framer-motion';

interface OptionCardProps {
  letter: string;
  label: string;
  selected: boolean;
  onSelect: () => void;
  disabled: boolean;
}

export default function OptionCard({ letter, label, selected, onSelect, disabled }: OptionCardProps) {
  return (
    <motion.button
      type="button"
      onClick={onSelect}
      disabled={disabled}
      className={`
        w-full text-left p-4 rounded-xl border transition-all duration-300
        flex items-center gap-4
        ${selected
          ? 'border-accent-glow/60 bg-accent-glow/10 shadow-[0_0_24px_rgba(167,139,250,0.2)]'
          : 'border-white/5 bg-space-deep/40 hover:border-white/10 hover:bg-space-deep/60'
        }
        ${disabled && !selected ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
      `}
      whileTap={selected ? {} : { scale: 0.98 }}
    >
      <span
        className={`
          flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium border
          ${selected
            ? 'border-accent-glow text-accent-glow bg-accent-glow/10'
            : 'border-white/10 text-star-dim'
          }
        `}
      >
        {letter}
      </span>
      <span className={`text-base ${selected ? 'text-star-bright' : 'text-star-dim'}`}>
        {label}
      </span>
    </motion.button>
  );
}
