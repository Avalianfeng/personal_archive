import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useSessionStore } from '../store/useSessionStore';
import { useUiStore } from '../store/useUiStore';
import { api } from '../api/client';

export default function StartPage() {
  const navigate = useNavigate();
  const setSession = useSessionStore((s) => s.setSession);
  const unlockAudio = useUiStore((s) => s.unlockAudio);

  const handleStart = async () => {
    unlockAudio();

    try {
      const data = await api.createSession();
      setSession(data.sessionId, data.questions);
      navigate('/question');
    } catch {
      // API 失败时使用 mock 数据
      const { mockSessionData } = await import('../mocks/session.mock');
      const mock = mockSessionData();
      setSession(mock.sessionId, mock.questions);
      navigate('/question');
    }
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-[70vh] text-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      {/* 星环 Logo */}
      <motion.div
        className="relative w-32 h-32 mb-8"
        animate={{ scale: [1, 1.04, 1] }}
        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
      >
        <div className="absolute inset-0 rounded-full border border-accent-glow/20 animate-ping opacity-20" />
        <div className="absolute inset-2 rounded-full border border-accent-glow/30" />
        <div className="absolute inset-4 rounded-full border border-accent-glow/40" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-3 h-3 rounded-full bg-accent-glow shadow-[0_0_20px_rgba(167,139,250,0.5)]" />
        </div>
      </motion.div>

      {/* 标题 */}
      <h1 className="font-serif text-4xl md:text-5xl font-bold mb-3 tracking-wide text-glow">
        人格深潜
      </h1>
      <p className="text-star-dim mb-10 text-sm leading-relaxed max-w-xs">
        向意识深处，遇见真实的自己
      </p>

      {/* CTA */}
      <motion.button
        onClick={handleStart}
        className="px-8 py-3 rounded-xl bg-accent-glow/15 border border-accent-glow/30 text-accent-glow font-medium text-base
                   hover:bg-accent-glow/25 hover:border-accent-glow/50 hover:shadow-[0_0_30px_rgba(167,139,250,0.3)]
                   transition-all duration-300"
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
      >
        开始探索
      </motion.button>

      {/* 底部说明 */}
      <div className="mt-12 text-xs text-star-dim/60 space-y-1">
        <p>预计 15 分钟 · 非心理测试 · 可随时退出</p>
        <p>你的回答仅保存在本地，不会被分享</p>
      </div>
    </motion.div>
  );
}
