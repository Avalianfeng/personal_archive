import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useSessionStore } from '../store/useSessionStore';
import ReportSection from '../components/ReportSection';
import PersonalityRadar from '../components/PersonalityRadar';
import ShimmerBlock from '../components/ShimmerBlock';

export default function ResultPage() {
  const navigate = useNavigate();
  const { vector, report, reset } = useSessionStore();
  const [feedback, setFeedback] = useState<number | null>(null);
  const [feedbackText, setFeedbackText] = useState('');
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleRestart = () => {
    reset();
    navigate('/');
  };

  const handleFeedback = (score: number) => {
    setFeedback(score);
    setFeedbackSent(true);
  };

  if (!vector) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <p className="text-star-dim mb-4">正在生成分析报告...</p>
        <ShimmerBlock lines={2} />
        <ShimmerBlock lines={3} />
      </div>
    );
  }

  return (
    <motion.div
      className="pb-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* 标题 */}
      <div className="text-center mb-6">
        <motion.h1
          className="font-serif text-3xl font-bold text-star-bright mb-2"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          你的深潜纪录
        </motion.h1>
        <motion.p
          className="text-star-dim text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          这是系统观察到的人格星图
        </motion.p>
      </div>

      {/* 雷达图 */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <PersonalityRadar vector={vector} />
      </motion.div>

      {/* 分析报告 */}
      {report ? (
        <>
          <ReportSection icon="🧠" title="认知风格" content={report.cognitiveStyle} delay={0.5} />
          <ReportSection icon="💙" title="情绪模式" content={report.emotionalPattern} delay={0.7} />
          <ReportSection icon="🌐" title="社交模式" content={report.socialPattern} delay={0.9} />
          <ReportSection icon="⭐" title="观察到的优势" content={report.strengths} delay={1.1} />
          <ReportSection icon="🔍" title="潜在盲区" content={report.blindSpots} delay={1.3} />
          <ReportSection icon="🌱" title="成长建议" content={report.growthSuggestions} delay={1.5} />
        </>
      ) : (
        <div className="mt-6">
          <ShimmerBlock lines={3} />
          <ShimmerBlock lines={3} />
          <ShimmerBlock lines={2} />
        </div>
      )}

      {/* 免责声明 */}
      <motion.p
        className="text-star-dim/30 text-xs text-center mt-8 mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.7 }}
      >
        * 本分析仅供自我探索参考，非心理诊断或医学建议
      </motion.p>

      {/* 反馈 */}
      <motion.div
        className="glass-card p-5 mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.9 }}
      >
        <p className="text-sm text-star-dim text-center mb-3">
          这像你的程度
        </p>
        {!feedbackSent ? (
          <div className="flex justify-center gap-3 mb-3">
            {[1, 2, 3, 4, 5].map((score) => (
              <button
                key={score}
                onClick={() => handleFeedback(score)}
                className={`w-10 h-10 rounded-full border text-sm font-medium transition-all
                  ${feedback === score
                    ? 'border-accent-glow bg-accent-glow/20 text-accent-glow'
                    : 'border-white/10 text-star-dim hover:border-white/20'
                  }`}
              >
                {score}
              </button>
            ))}
          </div>
        ) : (
          <p className="text-center text-star-dim/60 text-sm mb-3">感谢你的反馈</p>
        )}
        <textarea
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
          placeholder="还有什么想分享的？(可选)"
          className="w-full p-3 rounded-lg bg-space-void/50 border border-white/5 text-star-dim text-sm
                     placeholder:text-star-dim/30 focus:outline-none focus:border-accent-glow/30
                     resize-none h-16"
        />
      </motion.div>

      {/* 重新探索 */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.1 }}
      >
        <button
          onClick={handleRestart}
          className="px-6 py-2 rounded-lg border border-white/10 text-star-dim text-sm
                     hover:border-white/20 hover:text-star-bright transition-all duration-200"
        >
          重新探索
        </button>
      </motion.div>
    </motion.div>
  );
}
