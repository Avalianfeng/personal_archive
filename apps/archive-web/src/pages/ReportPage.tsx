import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useArchiveStore } from '../store/useArchiveStore';

function downloadMarkdown(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ReportPage() {
  const navigate = useNavigate();
  const { report, archive, reset } = useArchiveStore();

  useEffect(() => {
    if (!report || !archive) {
      navigate('/');
    }
  }, [report, archive, navigate]);

  if (!report || !archive) {
    return null;
  }

  const dateStr = new Date(report.generatedAt).toISOString().slice(0, 10);
  const filename = `archive-report-${dateStr}.md`;

  const handleDownload = () => {
    downloadMarkdown(report.markdown, filename);
  };

  const handleRestart = () => {
    reset();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="px-6 py-4 flex items-center justify-between border-b border-border bg-white">
        <div>
          <h1 className="text-lg font-semibold text-ink">档案报告</h1>
          <p className="text-xs text-ink-muted mt-0.5">
            完整度 {Math.round(report.completeness * 100)}%
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleDownload}
            className="px-4 py-2 text-sm rounded-lg bg-accent text-white
                       hover:bg-accent-hover transition-colors"
          >
            下载 MD
          </button>
          <button
            onClick={handleRestart}
            className="px-4 py-2 text-sm rounded-lg border border-border text-ink-muted
                       hover:border-ink-faint hover:text-ink transition-colors"
          >
            重新填写
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-auto px-6 py-8">
        <pre className="max-w-3xl mx-auto p-6 rounded-xl border border-border bg-white
                        font-mono text-sm text-ink leading-relaxed whitespace-pre-wrap
                        overflow-x-auto">
          {report.markdown}
        </pre>
      </main>
    </div>
  );
}
