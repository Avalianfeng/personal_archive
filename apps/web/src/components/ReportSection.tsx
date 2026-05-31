import { motion } from 'framer-motion';

interface ReportSectionProps {
  icon: string;
  title: string;
  content: string | string[];
  delay?: number;
}

export default function ReportSection({ icon, title, content, delay = 0 }: ReportSectionProps) {
  const items = Array.isArray(content) ? content : [content];

  return (
    <motion.div
      className="glass-card p-5 mb-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{icon}</span>
        <h3 className="text-sm font-semibold text-accent-glow tracking-wide">{title}</h3>
      </div>
      {items.map((item, i) => (
        <p key={i} className="text-star-dim text-sm leading-relaxed mb-1 last:mb-0">
          {items.length > 1 && '· '}{item}
        </p>
      ))}
    </motion.div>
  );
}
