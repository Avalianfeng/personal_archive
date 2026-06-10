import { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useSessionStore } from '../store/useSessionStore';
import { useUiStore } from '../store/useUiStore';
import OptionCard from '../components/OptionCard';
import { api } from '../api/client';
import { motion as motionConfig } from '../design/motion';

const LETTERS = ['A', 'B', 'C', 'D'] as const;

export default function QuestionPage() {
  const navigate = useNavigate();
  const {
    sessionId,
    questions,
    currentIndex,
    answers,
    addAnswer,
    nextQuestion,
    setResult,
  } = useSessionStore();
  const { reducedMotion } = useUiStore();

  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [textValue, setTextValue] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const disableTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const currentQuestion = questions[currentIndex];
  const isLast = currentIndex >= questions.length - 1;

  const currentAnswer = answers.find((a) => a.questionId === currentQuestion?.id);

  const handleSelect = useCallback(
    (key: string) => {
      if (isSubmitting) return;
      setSelectedOption(key);
      setSubmitError(null);

      // 防连点
      disableTimerRef.current = setTimeout(() => {
        const answer = { questionId: currentQuestion.id, optionKey: key };
        addAnswer(answer);

        // 提交到 API
        if (sessionId) {
          api.submitAnswer(sessionId, currentQuestion.id, key).catch(() => {});
        }

        if (isLast) {
          handleComplete();
        } else {
          setSelectedOption(null);
          nextQuestion();
        }
      }, motionConfig.disabledAfterSelectMs);
    },
    [currentQuestion, sessionId, isLast, isSubmitting],
  );

  const handleTextSubmit = useCallback(() => {
    if (isSubmitting || !textValue.trim()) return;
    setIsSubmitting(true);

    const answer = { questionId: currentQuestion.id, textAnswer: textValue.trim() };
    addAnswer(answer);

    if (sessionId) {
      api.submitAnswer(sessionId, currentQuestion.id, undefined, textValue.trim()).catch(() => {});
    }

    if (isLast) {
      handleComplete();
    } else {
      setTextValue('');
      setSelectedOption(null);
      setIsSubmitting(false);
      nextQuestion();
    }
  }, [textValue, currentQuestion, sessionId, isLast, isSubmitting]);

  const handleComplete = async () => {
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      if (sessionId) {
        const result = await api.completeSession(sessionId);
        setResult(result.vector, result.report);
      } else {
        // Mock fallback
        const { mockVector, mockReport } = await import('../mocks/session.mock');
        setResult(mockVector(), mockReport());
      }
      navigate('/result');
    } catch (err) {
      setSubmitError('分析生成中，请稍后...');
      // 超时后仍导航（向量已计算）
      setTimeout(() => navigate('/result'), 2000);
    }
  };

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (currentQuestion.type === 'choice' && currentQuestion.options) {
        const idx = parseInt(e.key) - 1;
        if (idx >= 0 && idx < Math.min(currentQuestion.options.length, 4)) {
          handleSelect(currentQuestion.options[idx].key);
        }
      }
      if (e.key === 'Enter' && currentQuestion.type === 'text') {
        handleTextSubmit();
      }
    },
    [currentQuestion, handleSelect, handleTextSubmit],
  );

  if (!currentQuestion) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-star-dim">加载中...</p>
      </div>
    );
  }

  const anim = reducedMotion
    ? {}
    : {
        initial: { opacity: 0, x: 40 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: -40 },
        transition: { duration: motionConfig.pageEnter.duration, ease: motionConfig.pageEnter.ease },
      };

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={currentQuestion.id}
        {...anim}
        className="flex flex-col min-h-[60vh]"
        onKeyDown={handleKeyDown}
        tabIndex={0}
        ref={(el) => el?.focus()}
      >
        {/* 题干 */}
        <div className="mb-8 mt-2">
          <p className="text-xl md:text-2xl leading-snug text-star-bright">
            {currentQuestion.question}
          </p>
          {currentQuestion.type === 'text' && (
            <p className="text-xs text-star-dim/50 mt-2">
              最多 {currentQuestion.maxLength || 120} 字
            </p>
          )}
        </div>

        {/* 选择题 */}
        {currentQuestion.type === 'choice' && currentQuestion.options && (
          <div className="flex flex-col gap-3 flex-1">
            {currentQuestion.options.map((opt, i) => (
              <OptionCard
                key={opt.key}
                letter={LETTERS[i] || opt.key}
                label={opt.label}
                selected={selectedOption === opt.key || currentAnswer?.optionKey === opt.key}
                onSelect={() => handleSelect(opt.key)}
                disabled={isSubmitting}
              />
            ))}
          </div>
        )}

        {/* 简答题 */}
        {currentQuestion.type === 'text' && (
          <div className="flex flex-col gap-4 flex-1">
            <textarea
              value={textValue}
              onChange={(e) => {
                const maxLen = currentQuestion.maxLength || 120;
                if (e.target.value.length <= maxLen) {
                  setTextValue(e.target.value);
                }
              }}
              placeholder={currentQuestion.placeholder}
              className="w-full h-40 p-4 rounded-xl bg-space-deep/60 border border-white/10
                         text-star-bright placeholder:text-star-dim/40 text-base
                         focus:outline-none focus:border-accent-glow/50 focus:ring-1 focus:ring-accent-glow/20
                         resize-none transition-colors"
            />
            <div className="flex justify-between items-center">
              <span className="text-xs text-star-dim/50">
                {textValue.length}/{currentQuestion.maxLength || 120}
              </span>
              <motion.button
                onClick={handleTextSubmit}
                disabled={!textValue.trim() || isSubmitting}
                className="px-6 py-2 rounded-lg bg-accent-glow/15 border border-accent-glow/30 text-accent-glow text-sm font-medium
                           hover:bg-accent-glow/25 disabled:opacity-30 disabled:cursor-not-allowed
                           transition-all duration-200"
                whileTap={{ scale: 0.97 }}
              >
                {isLast ? '完成' : '继续'}
              </motion.button>
            </div>
          </div>
        )}

        {/* 错误提示 */}
        {submitError && (
          <motion.p
            className="text-danger-soft text-sm mt-4 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {submitError}
          </motion.p>
        )}

        {/* 底部进度提示 */}
        <div className="mt-auto pt-8 text-center">
          <p className="text-star-dim/40 text-xs">
            第 {currentIndex + 1} 颗星
          </p>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
