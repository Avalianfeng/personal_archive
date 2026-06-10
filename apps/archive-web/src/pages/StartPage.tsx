import { useNavigate } from 'react-router-dom';
import { useArchiveStore } from '../store/useArchiveStore';

export default function StartPage() {
  const navigate = useNavigate();
  const { startNew, resumeOrStart, answers, archive } = useArchiveStore();

  const hasDraft = answers.length > 0 && !archive;

  const handleStart = () => {
    startNew();
    navigate('/form');
  };

  const handleContinue = () => {
    resumeOrStart();
    navigate('/form');
  };

  const handleViewReport = () => {
    navigate('/report');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="max-w-lg w-full text-center">
        <p className="text-sm text-ink-muted mb-2 tracking-wide">个人档案</p>
        <h1 className="text-3xl font-semibold text-ink mb-4">建立你的档案</h1>
        <p className="text-ink-muted leading-relaxed mb-10">
          整页填写，每题可选可补充说明，也可跳过。完成后生成 Markdown 档案报告。
        </p>

        <div className="flex flex-col gap-3">
          {hasDraft ? (
            <>
              <button
                onClick={handleContinue}
                className="w-full py-3 px-6 rounded-lg bg-accent text-white font-medium
                           hover:bg-accent-hover transition-colors"
              >
                继续填写
              </button>
              <button
                onClick={handleStart}
                className="w-full py-3 px-6 rounded-lg border border-border text-ink-muted
                           hover:border-ink-faint hover:text-ink transition-colors"
              >
                重新开始
              </button>
            </>
          ) : (
            <button
              onClick={handleStart}
              className="w-full py-3 px-6 rounded-lg bg-accent text-white font-medium
                         hover:bg-accent-hover transition-colors"
            >
              开始填写档案
            </button>
          )}

          {archive && (
            <button
              onClick={handleViewReport}
              className="w-full py-3 px-6 rounded-lg border border-border text-ink
                         hover:border-accent hover:text-accent transition-colors"
            >
              查看已有报告
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
